"""Validated explicit run + CAS; durable intent allows read-only recovery after crash.

Fault flags exit only this dedicated publisher process; never stop Mongo/web.
"""
import argparse
import json
import os
from pathlib import Path
import sys
import uuid
from bson.int64 import Int64
from pymongo import MongoClient
from pymongo.errors import PyMongoError
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'pipeline'))
from m2_source import ROOT, URI, DATABASE, SCHEMA, check, save
from m2_runtime import verify_owned_mongo, writer_lock
from m3_prepare import now, file_hash
from m5_common import OUT, frozen_inputs, verify_run


def recover(db, intent):
    current=db.publication.find_one({'_id':'active'})
    if current==intent['target']: status='APPLIED'
    elif current==intent['before']: status='NOT_APPLIED'
    else: status='CONFLICT'
    return dict(status=status,current=current,intent_id=intent['intent_id'],recovered_at_utc=now(),mutation=False)


def main(args):
    verify_owned_mongo()
    with writer_lock(), MongoClient(URI) as client:
        db=client[DATABASE]
        if args.recover:
            intent=json.loads(args.recover.read_text(encoding='utf-8'))
            result=recover(db,intent)
            target=OUT/('recovery-'+str(uuid.uuid4())+'.json');save(target,result)
            check(result['status']!='CONFLICT','RECOVERY_CONFLICT_REQUIRES_REVIEW')
            print(json.dumps(dict(result,receipt=str(target.relative_to(ROOT)))));return
        check(args.run_id and args.expected_run and args.expected_version is not None,'EXPLICIT_TARGET_AND_EXPECTED_REQUIRED')
        frozen_inputs(db)
        verification=verify_run(db,args.run_id)
        run=db.runs.find_one({'_id':args.run_id})
        previous=db.publication.find_one({'_id':'active'})
        check(previous and previous['run_id']==args.expected_run and previous['version']==args.expected_version,'PUBLICATION_CAS_CONFLICT')
        target=dict(_id='active',run_id=args.run_id,basket_set_id=run['basket_set_id'],schema_version=SCHEMA,
            version=Int64(args.expected_version+1),published_at_utc=now())
        intent=dict(intent_id=str(uuid.uuid4()),before=previous,target=target,verification=verification,
            created_at_utc=now(),publisher_sha256=file_hash(Path(__file__)))
        path=OUT/('publication-intent-'+intent['intent_id']+'.json');save(path,intent)
        print(json.dumps({'intent':str(path.relative_to(ROOT))}),flush=True)
        if args.crash=='before': os._exit(91)
        try:
            changed=db.publication.replace_one({'_id':'active','run_id':args.expected_run,'version':Int64(args.expected_version)},target)
            check(changed.matched_count==1,'PUBLICATION_CAS_CONFLICT')
            if args.crash=='after': os._exit(92)
            if args.simulate_timeout_after:
                # Deterministic driver-fault injection AFTER an acknowledged real
                # write. This is labelled injection, not a real server timeout.
                raise PyMongoError('M5_INJECTED_DRIVER_TIMEOUT_AFTER_REAL_WRITE')
        except PyMongoError:
            result=recover(db,intent)
            save(path.with_name('publication-error-readback-'+intent['intent_id']+'.json'),result)
            if result['status']!='APPLIED': raise
        result=recover(db,intent)
        check(result['status']=='APPLIED','PUBLICATION_READBACK')
        result.update(status='PASS',run_id=args.run_id,before=previous,after=target,mutation=True,verification=verification,
                      injected_timeout_after_real_write=args.simulate_timeout_after)
        save(path.with_name('publication-complete-'+intent['intent_id']+'.json'),result)
        print(json.dumps({'status':'PASS','run_id':args.run_id,'version':target['version']}))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--run-id');p.add_argument('--expected-run');p.add_argument('--expected-version',type=int)
    p.add_argument('--crash',choices=['before','after'])
    p.add_argument('--simulate-timeout-after',action='store_true')
    p.add_argument('--recover',type=Path)
    main(p.parse_args())
