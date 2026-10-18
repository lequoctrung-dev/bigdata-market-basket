"""Real Mongo/HTTP/crash probes in U-37 namespace; active never points to synthetic data."""
import argparse
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request,urlopen
from pymongo import MongoClient
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'pipeline'))
from m2_source import ROOT, URI, DATABASE, check, save, digest, immutable_batch, canonical
from m2_runtime import verify_owned_mongo, writer_lock, bson_counts
from m3_prepare import now, file_hash
from m3_trial import output_docs, write_readback
from m5_common import OUT, validate_outputs, protected_snapshot, check_protected
from verify_m4 import HTML


def probe_outputs(rid):
    return output_docs(rid,[dict(stock_code='A',display_name='M5 synthetic A',train_basket_count=3),
        dict(stock_code='B',display_name='M5 synthetic B',train_basket_count=2)],{},[],5)


def worker(rid,resume=False):
    verify_owned_mongo()
    with writer_lock(),MongoClient(URI) as client:
        db=client[DATABASE];outputs=probe_outputs(rid);identity=digest(outputs)
        if not resume:
            db.runs.insert_one(dict(_id=rid,run_id=rid,stage='M5_PROBE',mode='SYNTHETIC',status='WRITING',
                probe=True,provenance='M5 controlled crash/retry, never publish',payload_sha256=identity))
            immutable_batch(db.items,[bson_counts(outputs['items'][0])])
            os._exit(93)
        run=db.runs.find_one({'_id':rid})
        check(run['status']=='FAILED' and run['payload_sha256']==identity,'PROBE_RETRY_IDENTITY')
        check(db.runs.update_one({'_id':rid,'status':'FAILED'},{'$set':{'status':'WRITING'}}).matched_count==1,'PROBE_RETRY_CAS')
        validation=write_readback(db,outputs,rid)
        check(write_readback(db,outputs,rid)==validation,'SAME_PAYLOAD_RETRY')
        changed=dict(outputs['items'][0],display_name='changed payload')
        try: immutable_batch(db.items,[bson_counts(changed)])
        except RuntimeError as exc: check(str(exc)=='SOURCE_PAYLOAD_CONFLICT','CONFLICT_REASON')
        else: raise RuntimeError('CHANGED_PAYLOAD_ACCEPTED')
        check(db.items.find_one({'_id':changed['_id']})==bson_counts(outputs['items'][0]),'CONFLICT_PRESERVES_PAYLOAD')
        receipt=dict(counts=dict(train_baskets=5,train_items=2,itemsets=0,rules=0),split=dict(train=dict(baskets=5)),output_validation=validation)
        validate_outputs(db,rid,receipt) # 0 itemsets/0 rules valid and explicitly counted
        save(OUT/'probes'/f'{rid}.json',dict(status='PASS',receipt=receipt,outputs=outputs,changed_payload_rejected=True))
        db.runs.update_one({'_id':rid,'status':'WRITING'},{'$set':{'status':'FAILED','probe_complete':True,'reason':'TEST_ONLY_NOT_A_PRODUCT_RUN'}})


def campaign(rid):
    verify_owned_mongo(); path=OUT/('failure-campaign-'+str(uuid.uuid4()));path.mkdir(parents=True,exist_ok=False)
    report=dict(status='RUNNING',started_at_utc=now(),run_id=rid,steps=[])
    def child(label,command,expected):
        with (path/(label+'.stdout.log')).open('w',encoding='utf-8') as stdout,(path/(label+'.stderr.log')).open('w',encoding='utf-8') as stderr:
            process=subprocess.Popen(command,cwd=ROOT,stdout=stdout,stderr=stderr)
            result=process.wait(timeout=180)
        report['steps'].append(dict(label=label,command=command,pid=process.pid,exit_code=result,writer_exited=True))
        check(result==expected,'CHILD_EXIT_'+label+'_'+str(result));return result
    def http(pointer,fields=None,status=200):
        paths=['/','/patterns','/basket'] if fields is None else ['/recommend']
        for route in paths:
            req=Request('http://127.0.0.1:8081'+route,data=urlencode(fields).encode() if fields is not None else None)
            if fields is not None:req.add_header('Content-Type','application/x-www-form-urlencoded')
            try:
                with urlopen(req,timeout=30) as response: code,body=response.status,response.read().decode('utf-8')
            except HTTPError as exc:code,body=exc.code,exc.read().decode('utf-8')
            check(code==status,'CAMPAIGN_HTTP_'+str(code))
            h=HTML(body);p=h.root.find(**{'class':'provenance'})[0].attrs
            check(p['data-run']==pointer['run_id'] and int(p['data-version'])==pointer['version'],'CAMPAIGN_HTTP_SNAPSHOT')
            if fields is not None:check(not h.recommendations(),'STALE_FORM_EMPTY')
            report['steps'].append(dict(label='HTTP',route=route,status=code,run_id=pointer['run_id'],version=pointer['version']))
    try:
        with MongoClient(URI) as client:
            db=client[DATABASE];old=db.publication.find_one({'_id':'active'});protected=protected_snapshot(db)
            check(old['run_id']!=rid,'CAMPAIGN_TARGET_MUST_BE_UNPUBLISHED_NEW_RUN')
            report['before']=old;http(old)
            probe=str(uuid.uuid4())
            child('partial-writer-crash',[sys.executable,'-X','utf8',__file__,'--worker',probe],93)
            check(db.items.count_documents({'run_id':probe})==1 and db.runs.find_one({'_id':probe})['status']=='WRITING','ACTUAL_PARTIAL_OUTPUT')
            check(db.publication.find_one({'_id':'active'})==old,'PARTIAL_KEEPS_POINTER');http(old)
            with writer_lock():
                db.runs.update_one({'_id':probe,'status':'WRITING'},{'$set':{'status':'FAILED','reason':'OWNED_WORKER_EXIT_93'}})
            child('retry-after-writer-exited',[sys.executable,'-X','utf8',__file__,'--worker',probe,'--resume'],0)
            check(db.items.count_documents({'run_id':probe})==2,'RETRY_NO_DUPLICATION')
            probe_receipt=json.loads((OUT/'probes'/f'{probe}.json').read_text(encoding='utf-8'))['receipt']
            for label,field,value in [('count','expected',3),('hash','checksum','0'*64)]:
                bad=copy.deepcopy(probe_receipt);bad['output_validation']['items'][field]=value
                try:validate_outputs(db,probe,bad)
                except RuntimeError as exc:report['steps'].append(dict(label='rejected-'+label,error=str(exc),probe_run_id=probe))
                else:raise RuntimeError('BAD_OUTPUT_ACCEPTED_'+label)
            # New probe only: preserve malformed BSON Int32 as evidence, never touch READY data.
            schema_probe=str(uuid.uuid4());outputs=probe_outputs(schema_probe)
            with writer_lock():
                validation=write_readback(db,outputs,schema_probe)
                db.items.update_one({'_id':outputs['items'][0]['_id']},{'$set':{'train_basket_count':3}})
                db.runs.insert_one(dict(_id=schema_probe,run_id=schema_probe,mode='SYNTHETIC',stage='M5_PROBE',status='FAILED',probe=True,reason='DELIBERATE_BSON_INT32'))
            bad=dict(probe_receipt,output_validation=validation)
            try:validate_outputs(db,schema_probe,bad)
            except RuntimeError as exc:report['steps'].append(dict(label='rejected-schema',error=str(exc),probe_run_id=schema_probe))
            else:raise RuntimeError('BAD_SCHEMA_ACCEPTED')
            check(db.publication.find_one({'_id':'active'})==old,'PROBES_KEEP_POINTER');http(old)
            common=[sys.executable,'-X','utf8','scripts/m5_publish.py','--run-id',rid,'--expected-run',old['run_id'],'--expected-version',str(old['version'])]
            existing=set(OUT.glob('publication-intent-*.json'))
            child('publisher-crash-before',common+['--crash','before'],91)
            intent_path=next(iter(set(OUT.glob('publication-intent-*.json'))-existing))
            check(db.publication.find_one({'_id':'active'})==old,'CRASH_BEFORE_KEEPS_POINTER');http(old)
            child('readback-not-applied',[sys.executable,'-X','utf8','scripts/m5_publish.py','--recover',str(intent_path)],0)
            existing=set(OUT.glob('publication-intent-*.json'))
            child('publisher-crash-after',common+['--crash','after'],92)
            intent_path=next(iter(set(OUT.glob('publication-intent-*.json'))-existing))
            new=db.publication.find_one({'_id':'active'})
            check(new['run_id']==rid and new['version']==old['version']+1,'CRASH_AFTER_ACTUALLY_APPLIED')
            child('readback-applied-no-retry',[sys.executable,'-X','utf8','scripts/m5_publish.py','--recover',str(intent_path)],0)
            check(db.publication.find_one({'_id':'active'})==new,'RECOVERY_DOES_NOT_INCREMENT_VERSION')
            http(new);http(new,[('runId',old['run_id']),('version',str(old['version'])),('items','21080')],409)
            with writer_lock():
                # Actual stale-CAS on active: replacement is the complete REAL run, never fixture.
                changed=db.publication.replace_one({'_id':'active','run_id':old['run_id'],'version':old['version']},new)
                check(changed.matched_count==0 and db.publication.find_one({'_id':'active'})==new,'ACTUAL_CAS_MATCHED_ZERO')
            child('stale-publisher-rejected',common,1)
            check(db.publication.find_one({'_id':'active'})==new,'STALE_PUBLISHER_NO_OVERWRITE')
            check_protected(db,protected)
            report.update(status='PASS',after=new,probe_run_ids=[probe,schema_probe],checks=[
                'real partial writer exit93/preserved active web','retry only after child exit; same payload no duplicates/changed payload rejected',
                'Mongo count/hash/BSON guards and valid zero-rule outputs','real publisher crash before/after atomic update',
                'readback NOT_APPLIED/APPLIED without blind retry','real active matched0 and stale publisher conflict',
                'old real form409; every page current snapshot; old READY unchanged'])
    except Exception as exc:report.update(status='FAIL',error=str(exc),error_type=type(exc).__name__);raise
    finally:
        report.update(finished_at_utc=now(),campaign_sha256=file_hash(Path(__file__)))
        save(path/'receipt.json',report);print(json.dumps(dict(status=report['status'],receipt=str((path/'receipt.json').relative_to(ROOT)))))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run-id');p.add_argument('--worker');p.add_argument('--resume',action='store_true');a=p.parse_args()
    if a.worker:worker(a.worker,a.resume)
    else:campaign(a.run_id)
