"""Read-only DEVELOPMENT postcheck. No M2 invalidation or publication mutation."""
import argparse
from collections import Counter
import json
from pathlib import Path

from bson.int64 import Int64
from pymongo import MongoClient
from m2_source import ROOT, URI, DATABASE, SCHEMA, SOURCE_HASH, canonical, check, digest, save
from m2_runtime import verify_owned_mongo
from m3_prepare import OUT, BASKET_SET, M2_RUN, file_hash, load_jsonl, now, verified_preparation
from m3_protocol import PROTOCOL, evaluate, logical_checksum, mask, split_name, validate_rule


def require_bson_longs(value):
    if isinstance(value, dict):
        for item in value.values():
            require_bson_longs(item)
    elif isinstance(value, list):
        for item in value:
            require_bson_longs(item)
    elif isinstance(value, int) and not isinstance(value, bool):
        check(isinstance(value, Int64), 'MANIFEST_BSON_INT32')


def verify_run(db, run_id):
    path = OUT/run_id
    receipt = json.loads((path/'receipt.json').read_text(encoding='utf-8'))
    run = db.runs.find_one({'_id': run_id})
    check(run and run['status'] == 'READY' and run['stage'] == 'MODEL_DEVELOPMENT'
          and run['schema_version'] == SCHEMA and run['basket_set_id'] == BASKET_SET
          and run['dataset_id'] == SOURCE_HASH and run['evaluation_stage'] == 'DEVELOPMENT'
          and receipt['status'] == 'PASS' and run['manifest'] == receipt, 'READY_MANIFEST')
    require_bson_longs(run)
    check(receipt['protocol'] == PROTOCOL and receipt['protocol_sha256'] == digest(PROTOCOL)
          and receipt['final_status'] == 'NOT_RUN', 'DEVELOPMENT_PROTOCOL')
    prep_path = ROOT/receipt['preparation']
    prep = verified_preparation(prep_path)
    check(file_hash(prep_path/'preparation.json') == receipt['preparation_sha256'], 'PREP_RECEIPT_HASH')
    for filename, expected in receipt['files_sha256'].items():
        check(file_hash(path/filename) == expected, 'MODEL_OUTPUT_FILE_HASH')
    metadata = load_jsonl(prep_path/'split-metadata.jsonl')
    check(len(metadata) == len({r['invoice'] for r in metadata}) == prep['split_coverage'], 'SPLIT_UNIQUE_COVERAGE')
    check(all(split_name(r['invoice_time_local']) == r['split'] for r in metadata), 'SPLIT_BOUNDARIES')
    # Input stage check deliberately permits model/publication collections now.
    m2 = db.runs.find_one({'_id': M2_RUN})
    check(m2['status'] == 'VALIDATED' and m2['basket_set_status'] == 'READY'
          and m2['manifest']['basket_set_id'] == BASKET_SET, 'M2_INPUT_UNCHANGED_STAGE')
    m2_receipt = ROOT/f'artifacts/m2/pipeline-{M2_RUN}.json'
    check(file_hash(m2_receipt) == prep['m2_receipt_sha256']
          and m2['manifest'] == json.loads(m2_receipt.read_text(encoding='utf-8')), 'M2_MANIFEST_UNCHANGED')
    check(db.datasets.find_one({'_id': SOURCE_HASH})['status'] == 'READY'
          and db.baskets.count_documents({'basket_set_id': BASKET_SET}) == prep['split_coverage'], 'M2_BASKET_SOURCE_READY')
    current_metadata = list(db.baskets.find({'basket_set_id': BASKET_SET},
        {'_id':0, 'invoice':1, 'invoice_time_local':1}).sort('invoice',1))
    check(current_metadata == sorted([{k:r[k] for k in ('invoice','invoice_time_local')}
                                     for r in metadata], key=lambda r:r['invoice']), 'M2_SPLIT_METADATA_UNCHANGED')
    for part, low, high in [('train', PROTOCOL['train_start'], PROTOCOL['dev_start']),
                            ('dev', PROTOCOL['dev_start'], PROTOCOL['test_start'])]:
        current = list(db.baskets.find({'basket_set_id': BASKET_SET,
            'invoice_time_local':{'$gte':low,'$lt':high}}, {'_id':0}).sort('invoice',1))
        check(current == load_jsonl(prep_path/f'{part}-baskets.jsonl'), 'M2_TRAIN_DEV_UNCHANGED_'+part)
    outputs = {}
    for name in ('items','frequent_itemsets','association_rules'):
        expected = sorted(load_jsonl(path/f'{name}.jsonl'), key=lambda r: r['_id'])
        actual = sorted(db[name].find({'run_id': run_id}), key=lambda r: r['_id'])
        check(actual == expected and len(actual) == receipt['output_validation'][name]['actual'], 'MONGO_READBACK_'+name)
        check(logical_checksum([{k:v for k,v in r.items() if k not in ('_id','run_id')} for r in actual])
              == receipt['output_validation'][name]['checksum'], 'LOGICAL_CHECKSUM_'+name)
        outputs[name] = actual
    train = load_jsonl(prep_path/'train-baskets.jsonl')
    dev = load_jsonl(prep_path/'dev-baskets.jsonl')
    queries = load_jsonl(prep_path/'dev-queries.jsonl')
    expected_queries = [dict(invoice=b['invoice'], query=mask(b['invoice'], b['items'])[0],
        target=mask(b['invoice'], b['items'])[1], invoice_time_local=b['invoice_time_local'])
        for b in dev if len(b['items']) >= 2]
    check(queries == expected_queries, 'DEV_MASK_REPRODUCIBLE_ALL_QUERIES')
    check(all(r['invoice'] in {b['invoice'] for b in train} for r in load_jsonl(prep_path/'train-lineage-examples.jsonl')), 'TRAIN_LINEAGE_SCOPE')
    frequencies = Counter(c for b in train for c in b['items'])
    check(frequencies == {r['stock_code']: r['train_basket_count'] for r in outputs['items']}, 'CATALOG_BASELINE_TRAIN_COUNTS')
    check(all(isinstance(r['train_basket_count'], Int64) for r in outputs['items']), 'ITEM_BSON_LONG')
    for r in outputs['frequent_itemsets']:
        check(isinstance(r['frequency'], Int64) and isinstance(r['train_basket_count'], Int64)
              and r['train_basket_count'] == len(train), 'ITEMSET_BSON_DENOMINATOR')
        check(r['items'] == sorted(set(r['items'])) and r['itemset_key'] == canonical(r['items'])
              and r['_id'] == canonical([run_id,digest(r['items'])]), 'ITEMSET_KEY')
    for r in outputs['association_rules']:
        validate_rule(r)
        check(r['rule_key'] == canonical([r['antecedent'],r['consequent']])
              and r['_id'] == canonical([run_id,digest([r['antecedent'],r['consequent']])]), 'RULE_KEY')
    predictions, development = evaluate(queries, outputs['association_rules'], outputs['items'], PROTOCOL['k'])
    check(predictions == load_jsonl(path/'dev-predictions.jsonl') and development == receipt['development'], 'ALL_DEV_PREDICTIONS_METRICS_REPLAY')
    # Separate arithmetic for the reviewer: count the first 10 rows directly,
    # with result lists present. Does not call metrics() to build the answer.
    sample = predictions[:10]
    sample_counts = {}
    for method in ('rules','baseline'):
        n = len(sample)
        hits = len([r for r in sample if r['target'] in r[method]])
        nonempty = len([r for r in sample if len(r[method]) > 0])
        sample_counts[method] = dict(n=n, hits=hits, with_recommendations=nonempty,
            recall_at_k=hits/n if n else None, recommendation_rate=nonempty/n if n else None)
    # Real train count witnesses, independent set inclusion over invoice baskets.
    rule_samples = []
    for r in outputs['association_rules'][:3]:
        a, c = set(r['antecedent']), r['consequent']
        count_a = sum(a <= set(b['items']) for b in train)
        count_c = sum(c in b['items'] for b in train)
        witnesses = [b['invoice'] for b in train if a | {c} <= set(b['items'])]
        rule_samples.append(dict(rule_key=r['rule_key'], antecedent_count=count_a, consequent_count=count_c,
            union_count=len(witnesses), train_baskets=len(train), support=len(witnesses)/len(train),
            confidence=len(witnesses)/count_a, lift=(len(witnesses)/count_a)/(count_c/len(train)),
            train_invoice_examples=witnesses[:3], basket_set_id=BASKET_SET))
    return dict(status='PASS', run_id=run_id, verified_at_utc=now(), final_status='NOT_RUN',
        checks=['READY stage/manifest equality','M2 receipt/manifest preserved; stage-aware read only',
                'all files and Mongo logical checksums','actual BSON Int64','train frequency/catalog',
                'split/mask replay; metadata-only test','all development predictions/metrics replay'],
        sample_metrics=sample_counts, sample_predictions=sample, real_train_rules=rule_samples,
        human_review='PENDING_TV2', verifier_sha256=file_hash(Path(__file__)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-id', required=True)
    args = parser.parse_args()
    verify_owned_mongo()
    with MongoClient(URI) as client:
        report = verify_run(client[DATABASE], args.run_id)
    target = OUT/args.run_id/('verification-'+now().replace(':','').replace('+','')+'.json')
    save(target, report)
    print(canonical({'status': report['status'], 'verification': str(target.relative_to(ROOT))}))
