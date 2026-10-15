"""Real Mongo retry/conflict/partial probes; preserve isolated synthetic evidence."""
from datetime import datetime
import json
import time
import uuid
from decimal import Decimal

from bson.int64 import Int64
from pymongo import MongoClient

from m2_runtime import verify_owned_mongo, writer_lock, require_ready
from m2_source import (SOURCE_HASH, URI, DATABASE, OUT, canonical, check,
                       document, immutable_batch, save)


def main():
    verify_owned_mongo()
    with writer_lock(), MongoClient(URI) as client:
        db = client[DATABASE]
        require_ready(db, SOURCE_HASH)
        probe = 'm2-import-probe-'+str(uuid.uuid4())
        metadata = {'_id': probe, 'dataset_kind': 'SYNTHETIC_IMPORT_TEST', 'status': 'WRITING',
                    'expected_row_count': Int64(2), 'sheets': [{'sheet_index': 0, 'count': Int64(2)}]}
        db.datasets.insert_one(metadata)
        values = ('TEST-INVOICE', 'PADS', 'TEST ONLY', 2, datetime(2010,1,1), 1.234, None, 'SYNTHETIC')
        docs = []
        for row in (2, 3):
            doc = document(0, row, values)
            doc.update(_id=canonical([probe, 0, row]), dataset_id=probe)
            docs.append(doc)
        immutable_batch(db.source_rows, docs[:1])
        try:
            require_ready(db, probe)
        except RuntimeError as exc:
            check(str(exc) == 'SOURCE_NOT_READY', 'PARTIAL_GUARD_ERROR')
        else:
            raise RuntimeError('PARTIAL_IMPORT_ACCEPTED')
        immutable_batch(db.source_rows, docs)
        immutable_batch(db.source_rows, docs)
        check(db.source_rows.count_documents({'dataset_id': probe}) == 2, 'PROBE_RETRY_COUNT')
        db.datasets.update_one({'_id': probe, 'status': 'WRITING'}, {'$set': {'status': 'READY'}})
        require_ready(db, probe)
        try:
            immutable_batch(db.source_rows, [dict(docs[0], tuple_key='different-payload')], True)
        except RuntimeError as exc:
            check(str(exc) == 'SOURCE_PAYLOAD_CONFLICT', 'PROBE_CONFLICT_ERROR')
        else:
            raise RuntimeError('PROBE_CONFLICT_ACCEPTED')
        check(db.source_rows.find_one({'_id': docs[0]['_id']}) == docs[0], 'PROBE_CHANGED')
        # Retry 1,000 actual source rows from each sheet; no writes for existing rows.
        before = db.source_rows.count_documents({'dataset_id': SOURCE_HASH})
        retry_rows = []
        for sheet in (0, 1):
            retry_rows.extend(db.source_rows.find({'dataset_id': SOURCE_HASH, 'sheet_index': sheet}).sort('source_row', 1).limit(1000))
        immutable_batch(db.source_rows, retry_rows, True)
        check(db.source_rows.count_documents({'dataset_id': SOURCE_HASH}) == before == 1067371, 'SOURCE_RETRY_COUNT')
        spellings = []
        for row in db.source_rows.find({'dataset_id': SOURCE_HASH, 'source_cells.1.value': {'$in': ['47503J', '47503J ']}}):
            spellings.append({'sheet_index': row['sheet_index'], 'source_row': row['source_row'],
                'stock_code': row['source_cells'][1]['value'], 'description': row['source_cells'][2]['value']})
        save(OUT / 'stock-normalization-lineage.json', spellings)
        # Small invoice calculations from actual archived source, not Spark output.
        examples = json.loads((OUT / 'audit-source-v1/invoice-examples.json').read_text(encoding='utf-8'))
        hand_checks = {}
        for invoice, expected in examples.items():
            seen, items, lines, amount = set(), set(), [], Decimal(0)
            for row in db.source_rows.find({'dataset_id': SOURCE_HASH, 'source_cells.0.value': invoice}).sort([('sheet_index',1),('source_row',1)]):
                if row['tuple_key'] in seen:
                    continue
                seen.add(row['tuple_key'])
                cells = row['source_cells']
                code, q, p = cells[1]['value'].strip(), Decimal(cells[3]['value']), Decimal(cells[5]['value'])
                # These first three invoice examples contain merchandise only;
                # assert this rather than silently omitting other rows.
                from m2_source import excluded
                check(q > 0 and p > 0 and not excluded(code), 'HAND_EXAMPLE_POLICY')
                items.add(code)
                amount += q*p
                lines.append({'sheet_index': row['sheet_index'], 'source_row': row['source_row'],
                              'stock_code': code, 'quantity': str(q), 'price': str(p), 'line_value': str(q*p)})
            check(amount == Decimal(expected['line_value_gbp']) and len(lines) == expected['lines']
                  and sorted(items) == expected['items'], 'HAND_INVOICE_REFERENCE')
            hand_checks[invoice] = {'lines': lines, 'line_value_gbp': str(amount), 'items': sorted(items)}
        save(OUT / 'hand-invoices.json', hand_checks)
        report = {'status': 'PASS', 'partial_import_blocked': True, 'probe_dataset_id': probe,
                  'probe_retry_two_rows': True, 'probe_payload_conflict_rejected': True,
                  'source_ready_retry_rows': len(retry_rows), 'source_count_before_after': before,
                  'hand_invoice_count': len(hand_checks), 'no_publication': db.publication.count_documents({}) == 0}
        save(OUT / f'mongo-verification-{time.time_ns()}.json', report)
        print(canonical(report), flush=True)


if __name__ == '__main__':
    main()
