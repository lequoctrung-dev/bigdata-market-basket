"""Read-only M6 preprocessing validation; build fresh train/dev with frozen split."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import time
import uuid

from pymongo import MongoClient
from m2_source import ROOT, SOURCE, SOURCE_HASH, SCHEMA, POLICY, PARSER, canonical, check, digest, save
from m2_runtime import verify_owned_mongo, writer_lock, require_ready, STORAGE_VERSION
from m3_protocol import PROTOCOL, TRIALS, split_name, mask, logical_checksum, catalog_from_counts

from m3_prepare import file_hash, jsonl, load_jsonl, now, provenance, verified_preparation
from m6_common import URI, DATABASE, context

def prepare(session, preprocessing_run):
    state, (frozen, _, _) = context(session)
    OUT = M2_OUT = session
    M2_RUN = preprocessing_run
    receipt = json.loads((session/f'pipeline-{M2_RUN}.json').read_text(encoding='utf-8'))
    BASKET_SET = receipt['basket_set_id']
    verify_owned_mongo()
    with writer_lock(), MongoClient(URI) as client:
        db = client[DATABASE]
        start = time.monotonic()
        path = OUT / ('preparation-'+str(uuid.uuid4()))
        path.mkdir(parents=True, exist_ok=False)
        report = dict(milestone='M6', machine_role=state['machine_role'], machine_id=state['machine_id'], database=DATABASE, status='RUNNING', started_at_utc=now(), dataset_id=SOURCE_HASH,
                      basket_set_id=BASKET_SET, preprocessing_run_id=M2_RUN, protocol=PROTOCOL,
                      protocol_sha256=digest(PROTOCOL), frozen_config=frozen['config'], **provenance())
        save(path/'preparation.json', report)
        try:
            require_ready(db, SOURCE_HASH)
            m2 = db.runs.find_one({'_id': M2_RUN})
            check(m2 and m2['status'] == 'VALIDATED' and m2['basket_set_status'] == 'READY'
                  and m2['stage'] == 'PREPROCESSING' and m2['basket_set_id'] == BASKET_SET, 'M2_INPUT_STAGE')
            receipt_path = M2_OUT/f'pipeline-{M2_RUN}.json'
            receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
            check(m2['manifest'] == receipt and receipt['status'] == 'PASS'
                  and receipt['schema_version'] == SCHEMA and receipt['parser_version'] == PARSER
                  and receipt['storage_encoding_version'] == STORAGE_VERSION
                  and receipt['policy'] == POLICY and receipt['policy_hash'] == digest(POLICY), 'M2_RECEIPT_IDENTITY')
            postcheck = json.loads((M2_OUT/f'final-verification-{M2_RUN}.json').read_text(encoding='utf-8'))
            check(postcheck['status'] == 'PASS' and postcheck['run_id'] == M2_RUN
                  and postcheck['basket_set_id'] == BASKET_SET, 'M2_POSTCHECK_IDENTITY')
            check(file_hash(SOURCE) == SOURCE_HASH, 'SOURCE_HASH')
            lines_path = ROOT/receipt['output_directory']/'retained-lines.jsonl'
            check(file_hash(lines_path) == receipt['line_output']['sha256'], 'M2_LINES_HASH')
            # Never request items for final test. Splits depend ONLY on invoice local time.
            metadata = list(db.baskets.find({'basket_set_id': BASKET_SET},
                {'_id': 0, 'invoice': 1, 'invoice_time_local': 1}).sort('invoice', 1))
            check(len(metadata) == receipt['counts']['baskets'] and len({b['invoice'] for b in metadata}) == len(metadata), 'BASKET_COVERAGE_UNIQUE')
            parts = {s: [] for s in ('train','dev','test')}
            for b in metadata:
                check(datetime.fromisoformat(b['invoice_time_local']).tzinfo is None, 'LOCAL_TIME_REQUIRED')
                parts[split_name(b['invoice_time_local'])].append(b)
            ids = {s: {b['invoice'] for b in bs} for s, bs in parts.items()}
            check(all(parts.values()) and not(ids['train'] & ids['dev'] or ids['train'] & ids['test'] or ids['dev'] & ids['test']), 'SPLIT_EMPTY_OR_OVERLAP')
            report['split'] = {s: {'baskets': len(bs), 'min_time_local': min(b['invoice_time_local'] for b in bs),
                'max_time_local': max(b['invoice_time_local'] for b in bs), 'invoice_time_sha256': logical_checksum(bs)}
                for s, bs in parts.items()}
            report.update(invoice_overlap=0, split_coverage=len(metadata), m2_receipt_sha256=file_hash(receipt_path),
                          m2_line_sha256=receipt['line_output']['sha256'],
                          m2_basket_checksum_reference=receipt['basket_checksum'],
                          test_access='invoice/time metadata only; no test items, masks, predictions or metrics')
            jsonl(path/'split-metadata.jsonl', [dict(b, split=s) for s, bs in parts.items() for b in bs])
            baskets = {s: [] for s in ('train','dev')}
            # Time predicates ensure MongoDB never returns test items to this process.
            for s, low, high in [('train', PROTOCOL['train_start'], PROTOCOL['dev_start']),
                                  ('dev', PROTOCOL['dev_start'], PROTOCOL['test_start'])]:
                query = {'basket_set_id': BASKET_SET, 'invoice_time_local': {'$gte': low, '$lt': high}}
                for b in db.baskets.find(query, {'_id': 0}).sort('invoice', 1):
                    check(b['invoice'] in ids[s] and b['items'] == sorted(set(b['items'])) and b['items'], 'BASKET_ARRAY_IDENTITY')
                    baskets[s].append(b)
                check({b['invoice'] for b in baskets[s]} == ids[s], 'SPLIT_MEMBERSHIP')
                jsonl(path/f'{s}-baskets.jsonl', baskets[s])
                report['split'][s].update(single_item_baskets=sum(len(b['items']) == 1 for b in baskets[s]),
                    max_basket_size=max(len(b['items']) for b in baskets[s]),
                    basket_sha256=logical_checksum(baskets[s]))
            frequencies = Counter(c for b in baskets['train'] for c in b['items'])
            names = defaultdict(Counter)
            # Check train source lines against each Mongo basket as well as line count/time.
            actual_items, actual_lines, min_times = defaultdict(set), Counter(), {}
            example_lines = []
            example_invoices = {b['invoice'] for b in baskets['train'][:2]}
            retained_count = 0
            with lines_path.open(encoding='utf-8') as stream:
                for line in stream:
                    retained_count += 1
                    row = json.loads(line)
                    # Non-train values are not used to select catalog, names or parameters.
                    inv = row['invoice']
                    if inv not in ids['train'] or not row['positive_valid'] or row['p02_excluded']:
                        continue
                    c, name = row['stock_code'], row['description']
                    check(c in frequencies, 'TRAIN_LINE_UNKNOWN_ITEM')
                    actual_items[inv].add(c)
                    actual_lines[inv] += 1
                    min_times[inv] = min(min_times.get(inv, row['invoice_time_local']), row['invoice_time_local'])
                    if isinstance(name, str) and name.strip():
                        names[c][name.strip()] += 1
                    if inv in example_invoices:
                        example_lines.append({k: row[k] for k in ('invoice','stock_code','source_id','sheet_index','source_row','description')})
            check(retained_count == receipt['counts']['retained'], 'M2_LINES_COUNT')
            check(all(actual_items[b['invoice']] == set(b['items']) and actual_lines[b['invoice']] == b['retained_line_count']
                      and min_times[b['invoice']] == b['invoice_time_local'] for b in baskets['train']), 'TRAIN_LINES_BASKET_LINEAGE')
            catalog = catalog_from_counts(frequencies, names)
            queries = [dict(invoice=b['invoice'], query=mask(b['invoice'], b['items'])[0],
                            target=mask(b['invoice'], b['items'])[1], invoice_time_local=b['invoice_time_local'])
                       for b in baskets['dev'] if len(b['items']) >= 2]
            jsonl(path/'catalog.jsonl', catalog)
            jsonl(path/'dev-queries.jsonl', queries)
            jsonl(path/'train-lineage-examples.jsonl', example_lines)
            report.update(train_items=len(catalog), train_lines=sum(actual_lines.values()), eligible_dev_queries=len(queries),
                          schema_version=SCHEMA, parser_version=PARSER, policy=POLICY, policy_hash=digest(POLICY),
                          checks=['M2 READY identity/source/line hashes','invoice coverage/no overlap/half-open boundaries',
                                  'test items never queried','every train basket reconstructed from retained merchandise lines',
                                  'train-only names/frequency/catalog','single baskets preserved; deterministic mask'],
                          files_sha256={p.name: file_hash(p) for p in sorted(path.glob('*.jsonl'))},
                          status='PASS', finished_at_utc=now(), elapsed_seconds=time.monotonic()-start)
        except Exception as exc:
            report.update(status='FAIL', error=str(exc), error_type=type(exc).__name__, finished_at_utc=now())
            raise
        finally:
            save(path/'preparation.json', report)
            print(canonical({'preparation': str(path.relative_to(ROOT)), 'status': report['status']}), flush=True)



if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--session', required=True, type=Path)
    parser.add_argument('--preprocessing-run', required=True)
    args=parser.parse_args()
    prepare(args.session.resolve(), args.preprocessing_run)
