"""M6 full-workbook import/READY retry into the explicitly approved isolated database."""
import argparse
import hashlib
from collections import Counter
import json
from pathlib import Path
import time
from bson.int64 import Int64
from pymongo import MongoClient
from m2_source import (SOURCE_HASH, SCHEMA, PARSER, HEADERS, SHEETS, COUNTS, verified_rows,
                       document, immutable_batch, canonical, check, save, audit)
from m2_runtime import verify_owned_mongo, writer_lock
from m6_common import DATABASE, URI, context

def import_source(session):
    context(session)
    started = time.monotonic()
    with MongoClient(URI) as client:
        db = client[DATABASE]
        metadata = db.datasets.find_one({'_id': SOURCE_HASH})
        ready = bool(metadata and metadata['status'] == 'READY')
        before_rows = db.source_rows.count_documents({'dataset_id': SOURCE_HASH})
        spec = {'_id': SOURCE_HASH, 'source_sha256': SOURCE_HASH, 'schema_version': SCHEMA,
                'parser_version': PARSER, 'source_url': 'https://archive.ics.uci.edu/dataset/502/online+retail+ii',
                'citation': 'Daqing Chen. Online Retail II. DOI 10.24432/C5CG6D. CC BY 4.0.',
                'sheets': [{'sheet_index': i, 'name': name, 'header': HEADERS, 'count': Int64(COUNTS[i])}
                           for i, name in enumerate(SHEETS)], 'expected_row_count': Int64(sum(COUNTS))}
        if metadata:
            check(all(metadata.get(k) == v for k, v in spec.items()), 'DATASET_METADATA_CONFLICT')
        else:
            db.datasets.insert_one(dict(spec, status='WRITING'))
        db.source_rows.create_index([('dataset_id', 1), ('sheet_index', 1), ('source_row', 1)], unique=True)
        seen, batch = Counter(), []
        expected_hash = hashlib.sha256()
        for index, row_num, values in verified_rows():
            doc = document(index, row_num, values)
            expected_hash.update((canonical(doc)+'\n').encode('utf-8'))
            batch.append(doc)
            seen[index] += 1
            if len(batch) == 1000:
                immutable_batch(db.source_rows, batch, ready)
                batch = []
                if sum(seen.values()) % 100000 == 0:
                    print(canonical({'import_verified_rows': sum(seen.values()), 'retry_ready': ready}), flush=True)
        if batch:
            immutable_batch(db.source_rows, batch, ready)
        for i, expected in enumerate(COUNTS):
            check(seen[i] == expected == db.source_rows.count_documents({'dataset_id': SOURCE_HASH, 'sheet_index': i}), 'IMPORT_COUNT')
        check(db.source_rows.count_documents({'dataset_id': SOURCE_HASH}) == sum(COUNTS), 'IMPORT_TOTAL')
        check(db.source_rows.count_documents({'dataset_id': SOURCE_HASH,
              'sheet_index': {'$type':'long'}, 'source_row': {'$type':'long'}}) == sum(COUNTS),
              'M6_SOURCE_POSITIONS_BSON_LONG')
        actual_hash = hashlib.sha256()
        for doc in db.source_rows.find({'dataset_id': SOURCE_HASH}).sort([('sheet_index',1),('source_row',1)]):
            actual_hash.update((canonical(doc)+'\n').encode('utf-8'))
        check(expected_hash.hexdigest() == actual_hash.hexdigest(), 'M6_SOURCE_FULL_PAYLOAD_READBACK')
        if not ready:
            check(db.datasets.update_one({'_id': SOURCE_HASH, 'status': 'WRITING'}, {'$set': {'status': 'READY'}}).modified_count == 1,
                  'IMPORT_STATE')
        sample = db.source_rows.find_one({'dataset_id': SOURCE_HASH})
        immutable_batch(db.source_rows, [sample], True)
        try:
            immutable_batch(db.source_rows, [dict(sample, tuple_key='deliberate-conflict')], True)
        except RuntimeError as exc:
            check(str(exc) == 'SOURCE_PAYLOAD_CONFLICT', 'CONFLICT_ERROR')
        else:
            raise RuntimeError('CONFLICT_NOT_REJECTED')
        report = {'milestone': 'M6', 'database': DATABASE, 'physical_insert_rows': db.source_rows.count_documents({'dataset_id': SOURCE_HASH}) - before_rows, 'status': 'PASS', 'source_sha256': SOURCE_HASH, 'row_count': sum(seen.values()),
                  'sheet_counts': dict(seen), 'source_payload_sha256': actual_hash.hexdigest(),
                  'full_payload_readback': True,
                  'full_ready_retry': ready, 'same_payload_retry': True, 'different_payload_rejected': True,
                  'elapsed_seconds': time.monotonic()-started}
        path = session / f'import-{time.time_ns()}.json'
        save(path, report)
        print(canonical(report), flush=True)



if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('action', choices=['audit','import'])
    p.add_argument('--session', type=Path, required=True)
    args=p.parse_args(); session=args.session.resolve()
    context(session)
    if args.action == 'audit':
        audit(session/'audit')
    else:
        verify_owned_mongo()
        with writer_lock():
            import_source(session)
