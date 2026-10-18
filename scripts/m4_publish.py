"""Publish the explicitly frozen DEVELOPMENT run; no fit or output mutation."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'pipeline'))
from bson.int64 import Int64
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from m2_source import ROOT, URI, DATABASE, SCHEMA, SOURCE, SOURCE_HASH, check, save
from m2_runtime import verify_owned_mongo, writer_lock
from m3_prepare import OUT, file_hash, now
from m3_verify import verify_run

FREEZE = OUT/'freeze-1a1f2ec6-331e-4b02-9aaf-18804793d4e9'
FREEZE_HASH = 'f7ee9c13432f0c99e7e5bcbf0363eed77eb4d5493b39e78fbb2e8e48557d053a'


def publish(db, run, previous):
    pointer = dict(_id='active', run_id=run['_id'], basket_set_id=run['basket_set_id'],
                   schema_version=SCHEMA, version=Int64(1 if previous is None else previous['version']+1),
                   published_at_utc=now())
    try:
        if previous is None:
            db.publication.insert_one(pointer)
        else:
            check(db.publication.replace_one({'_id':'active', 'run_id':previous['run_id'],
                'version':previous['version']}, pointer).matched_count == 1, 'PUBLICATION_CAS_CONFLICT')
    except PyMongoError:
        # A timeout does not prove that the write failed. Never retry blindly.
        if db.publication.find_one({'_id':'active'}) != pointer:
            raise
    check(db.publication.find_one({'_id':'active'}) == pointer, 'PUBLICATION_READBACK')
    return pointer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--publish', action='store_true', help='otherwise read-only preflight')
    args = parser.parse_args()
    target = ROOT/'artifacts/m4'/('publication-'+now().replace(':','')+'.json')
    report = dict(started_at_utc=now(), status='RUNNING', action='publish' if args.publish else 'inspect')
    try:
        verify_owned_mongo()
        check(file_hash(FREEZE/'freeze.json') == FREEZE_HASH, 'FROZEN_SELECTION_HASH')
        frozen = json.loads((FREEZE/'freeze.json').read_text(encoding='utf-8'))
        for name, expected in json.loads((FREEZE/'hashes.json').read_text()).items():
            check(file_hash(FREEZE/name) == expected, 'FREEZE_FILE_HASH_'+name)
        check(file_hash(SOURCE) == SOURCE_HASH == frozen['source_sha256'], 'SOURCE_HASH')
        run_id = frozen['selected_run_id']
        check(file_hash(OUT/run_id/'receipt.json') == frozen['selected_receipt_sha256'], 'FROZEN_RECEIPT_HASH')
        with writer_lock(), MongoClient(URI) as client:
            db = client[DATABASE]
            report['verification'] = verify_run(db, run_id)
            run = db.runs.find_one({'_id':run_id})
            check(run['config'] == frozen['config'] and run['manifest']['output_validation'] == frozen['output_validation'], 'FROZEN_OUTPUTS_CONFIG')
            previous = db.publication.find_one({'_id':'active'})
            report.update(before=previous, run_id=run_id, freeze_sha256=FREEZE_HASH,
                          dataset_id=SOURCE_HASH, basket_set_id=run['basket_set_id'])
            # An unexpected selection needs investigation, not automatic replacement.
            check(previous is None or (previous['run_id'] == run_id and previous['schema_version'] == SCHEMA
                  and previous['basket_set_id'] == run['basket_set_id']), 'UNEXPECTED_EXISTING_PUBLICATION')
            report['after'] = (publish(db, run, previous) if args.publish and previous is None else previous)
            report['mutation'] = bool(args.publish and previous is None)
            report['status'] = 'PASS'
    except Exception as exc:
        report.update(status='FAIL', error_type=type(exc).__name__, error=str(exc))
        raise
    finally:
        report.update(finished_at_utc=now(), publisher_sha256=file_hash(Path(__file__)))
        save(target, report)
        print(json.dumps({'status':report['status'], 'receipt':str(target.relative_to(ROOT))}))


if __name__ == '__main__':
    main()
