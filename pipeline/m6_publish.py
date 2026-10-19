"""Publish an explicitly verified M6 run, preserving durable intent and CAS/readback."""
import argparse
import json
from pathlib import Path
import uuid
from bson.int64 import Int64
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from m2_source import ROOT, SCHEMA, check, save
from m2_runtime import verify_owned_mongo, writer_lock
from m3_prepare import now, file_hash
from m6_common import DATABASE, URI, context
from m6_verify import verify_run


def recover(db, intent):
    current = db.publication.find_one({'_id':'active'})
    status = 'APPLIED' if current == intent['target'] else 'NOT_APPLIED' if current == intent['before'] else 'CONFLICT'
    return dict(status=status, current=current, intent_id=intent['intent_id'], mutation=False, at_utc=now())


def publish(session, rid, initial=False, expected_run=None, expected_version=None, recovery=None):
    context(session)
    verify_owned_mongo()
    with writer_lock(), MongoClient(URI) as client:
        db = client[DATABASE]
        if recovery:
            check(recovery.resolve().parent == session, 'M6_RECOVERY_FROM_OTHER_SESSION')
            intent = json.loads(recovery.read_text(encoding='utf-8'))
            check(intent['database'] == DATABASE, 'M6_RECOVERY_DATABASE')
            result = recover(db,intent)
            save(session/('recovery-'+str(uuid.uuid4())+'.json'),result)
            check(result['status'] != 'CONFLICT','M6_RECOVERY_CONFLICT')
            print(json.dumps(result));return
        verification = verify_run(db,rid,session)
        previous = db.publication.find_one({'_id':'active'})
        if initial:
            check(previous is None and expected_run is None and expected_version is None, 'M6_INITIAL_POINTER_EXISTS')
        else:
            check(previous and previous['run_id'] == expected_run and previous['version'] == expected_version,
                  'M6_PUBLICATION_CAS_CONFLICT')
        run = db.runs.find_one({'_id':rid})
        target = dict(_id='active',run_id=rid,basket_set_id=run['basket_set_id'],schema_version=SCHEMA,
            version=Int64(1 if initial else expected_version+1),published_at_utc=now())
        intent = dict(intent_id=str(uuid.uuid4()),database=DATABASE,before=previous,target=target,
            created_at_utc=now(),verification=verification,publisher_sha256=file_hash(Path(__file__)))
        path = session/('publication-intent-'+intent['intent_id']+'.json')
        save(path,intent)
        try:
            if initial:
                db.publication.insert_one(target)
            else:
                changed = db.publication.replace_one({'_id':'active','run_id':expected_run,'version':Int64(expected_version)},target)
                check(changed.matched_count == 1, 'M6_PUBLICATION_CAS_CONFLICT')
        except PyMongoError:
            result = recover(db,intent)
            save(session/('publication-error-readback-'+intent['intent_id']+'.json'),result)
            if result['status'] != 'APPLIED': raise
        result = recover(db,intent)
        check(result['status'] == 'APPLIED','M6_PUBLICATION_READBACK')
        save(session/('publication-complete-'+intent['intent_id']+'.json'),
             dict(result,status='PASS',run_id=rid,before=previous,after=target,verification=verification))
        print(json.dumps(dict(status='PASS',run_id=rid,version=target['version'])))


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--session',required=True,type=Path);p.add_argument('--run-id')
    p.add_argument('--initial',action='store_true');p.add_argument('--expected-run');p.add_argument('--expected-version',type=int)
    p.add_argument('--recover',type=Path)
    a=p.parse_args()
    if not a.recover and not a.run_id: p.error('--run-id or --recover required')
    publish(a.session.resolve(),a.run_id,a.initial,a.expected_run,a.expected_version,a.recover)
