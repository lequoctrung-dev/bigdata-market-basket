"""Verify persisted final BSON/output and invalidate earlier nonconforming checkpoints."""
import argparse
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import subprocess

from bson.int64 import Int64
from pymongo import MongoClient
from m2_source import ROOT, OUT, SOURCE, SOURCE_HASH, URI, DATABASE, check, save
from m2_runtime import verify_owned_mongo, writer_lock, require_ready, STORAGE_VERSION


def main(run_id):
    verify_owned_mongo()
    with writer_lock(), MongoClient(URI) as client:
        db = client[DATABASE]
        require_ready(db, SOURCE_HASH)
        run = db.runs.find_one({'_id': run_id})
        check(run and run['status'] == 'VALIDATED' and run['basket_set_status'] == 'READY', 'FINAL_M2_STATE')
        manifest = run['manifest']
        check(manifest['status'] == 'PASS' and manifest['storage_encoding_version'] == STORAGE_VERSION,
              'FINAL_STORAGE_VERSION')
        counts, basket_set = manifest['counts'], manifest['basket_set_id']
        check(all(isinstance(v, Int64) for v in counts.values()), 'MANIFEST_COUNTS_NOT_INT64')
        check(db.source_rows.count_documents({'dataset_id': SOURCE_HASH,
              'sheet_index': {'$type': 'long'}, 'source_row': {'$type': 'long'}}) == 1067371,
              'SOURCE_POSITION_NOT_INT64')
        check(db.baskets.count_documents({'basket_set_id': basket_set,
              'retained_line_count': {'$type': 'long'}}) == counts['baskets'], 'BASKET_LONG_COUNTS')
        for kind, fields, expected in [('item', ['rows','quantity','baskets'], counts['items']),
                                      ('month', ['invoices','lines'], len(manifest['monthly'])),
                                      ('basket_size', ['baskets'], len(manifest['size_distribution']))]:
            query = {'basket_set_id': basket_set, 'summary_type': kind,
                     **{f'payload.{field}': {'$type': 'long'} for field in fields}}
            check(db.summaries.count_documents(query) == expected, 'SUMMARY_BSON_LONG_'+kind)
        check(db.publication.count_documents({}) == 0 and db.items.count_documents({}) == 0
              and db.frequent_itemsets.count_documents({}) == 0 and db.association_rules.count_documents({}) == 0,
              'UNEXPECTED_MODEL_PUBLICATION')
        line_path = ROOT / manifest['output_directory'] / 'retained-lines.jsonl'
        with line_path.open('rb') as stream:
            line_hash = hashlib.file_digest(stream, 'sha256').hexdigest()
        check(line_hash == manifest['line_output']['sha256'], 'PROCESSED_FILE_HASH')
        check(sum(1 for _ in line_path.open('rb')) == counts['retained'], 'PROCESSED_FILE_COUNT')
        with SOURCE.open('rb') as stream:
            check(hashlib.file_digest(stream, 'sha256').hexdigest() == SOURCE_HASH, 'SOURCE_FINAL_HASH')
        invalidated = []
        for old in db.runs.find({'dataset_id': SOURCE_HASH, 'stage': 'PREPROCESSING', 'status': 'VALIDATED',
                                '_id': {'$ne': run_id}}):
            if db.baskets.count_documents({'basket_set_id': old['basket_set_id'],
                                          'retained_line_count': {'$type': 'int'}}):
                changed = db.runs.update_one({'_id': old['_id'], 'status': 'VALIDATED'}, {'$set': {
                    'status': 'FAILED', 'basket_set_status': 'INCOMPLETE',
                    'error_code': 'POSTCHECK_BSON_INT32_COUNTS', 'superseded_by_m2_run': run_id}})
                check(changed.modified_count == 1, 'LEGACY_STATUS_CONFLICT')
                invalidated.append(old['_id'])
        report = {'status': 'PASS', 'machine_role': manifest['machine_role'], 'run_id': run_id,
                  'basket_set_id': basket_set, 'source_sha256': SOURCE_HASH,
                  'checks': ['full_source_bson_long_positions', 'manifest_basket_summary_bson_long_counts',
                             'processed_file_hash_and_rows', 'source_final_hash', 'no_model_no_publication'],
                  'legacy_checkpoints_invalidated': invalidated,
                  'legacy_receipts_and_outputs_preserved': True, 'human_review': 'PENDING_TV2',
                  'verified_at_utc': datetime.now(timezone.utc).isoformat(),
                  'verification_code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  'git_head': subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip()}
        save(OUT / f'final-verification-{run_id}.json', report)
        print(report)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--run-id', required=True)
    main(parser.parse_args().run_id)
