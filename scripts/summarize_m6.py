"""Close a technical FULL_RUN receipt; human acceptance remains a separate event."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from datetime import datetime
import psutil
from pymongo import MongoClient

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'pipeline'))
from m2_source import SOURCE, SOURCE_HASH, canonical, check, save
from m2_runtime import verify_owned_mongo, writer_lock
from m3_prepare import file_hash, now
from m6_common import URI, DATABASE, context, namespace_hashes, FREEZE_HASH, FINAL_HASH
from m6_verify import verify_run, owned_web


def main(a):
    session=a.session.resolve()
    state,_=context(session)
    target=session/('technical-full-run-'+now().replace(':','')+'.json')
    report=dict(status='RUNNING',milestone='M6',mode='FULL_RUN',session_id=state['session_id'],
        machine_role=state['machine_role'],machine_id=state['machine_id'],started_at_utc=now(),
        operator='AGENT_ASSISTED_TECHNICAL_EXECUTION',human_demo='PENDING_USER',
        tv2_runtime='ASSUMED_EQUIVALENT_BY_USER_NOT_MEASURED',checks=[])
    try:
        verify_owned_mongo()
        web=owned_web(session)
        with writer_lock(),MongoClient(URI) as client:
            db=client[DATABASE]
            postcheck=verify_run(db,a.final_run,session)
            run=db.runs.find_one({'_id':a.final_run});receipt=run['manifest']
            pointer=db.publication.find_one({'_id':'active'})
            check(pointer['run_id']==a.final_run,'M6_FINAL_ACTIVE')
            check(set(db.list_collection_names())=={'datasets','source_rows','baskets','runs','items',
                  'frequent_itemsets','association_rules','summaries','publication'},'M6_NINE_COLLECTIONS')
            imports=[]
            for path in session.glob('import-*.json'):
                value=json.loads(path.read_text(encoding='utf-8'))
                if value.get('row_count')==1067371 and value.get('full_payload_readback') is True:
                    imports.append((path,value))
            check(len(imports)==1 and imports[0][1]['status']=='PASS','M6_FULL_SOURCE_IMPORT_RECEIPT')
            actual_hash=hashlib.sha256()
            for doc in db.source_rows.find({'dataset_id':SOURCE_HASH}).sort([('sheet_index',1),('source_row',1)]):
                actual_hash.update((canonical(doc)+'\n').encode('utf-8'))
            check(actual_hash.hexdigest()==imports[0][1]['source_payload_sha256'],'M6_SOURCE_PAYLOAD_PRESERVED')
            before=json.loads((session/'protected-m2-before.json').read_text(encoding='utf-8'))
            after=namespace_hashes(client['bigdata_m2'])
            save(session/('protected-m2-after-'+now().replace(':','')+'.json'),after)
            check(before==after,'M6_HISTORICAL_M2_DATABASE_CHANGED')
            report.update(postcheck=postcheck,publication=pointer,preprocessing_run_id=receipt['preprocessing_run_id'],
                development_run_id=receipt['model_source_run_id'],final_run_id=a.final_run,
                stage_counts=receipt['stage_counts'],split=receipt['split'],config=receipt['config'],
                development=receipt['development'],final=receipt['final'],final_new_items=receipt['final_new_items'],
                output_validation=receipt['output_validation'],test_access=receipt['test_access'],
                source_payload_sha256=actual_hash.hexdigest(),historical_m2_database_unchanged=True,
                import_receipt=str(imports[0][0].relative_to(ROOT)),physical_insert_rows=imports[0][1]['physical_insert_rows'])
        http=json.loads(a.http.read_text(encoding='utf-8'))
        browser=json.loads(a.browser.read_text(encoding='utf-8'))
        check(http['status']=='PASS' and http['run_id']==a.final_run
              and http['version']==pointer['version'] and http['source_to_web_verified'],'M6_FINAL_HTTP_RECEIPT')
        check(browser['status']=='PASS' and browser['run_id']==a.final_run
              and browser['publication_version']==pointer['version'] and browser['browser_exit_code']==0,'M6_BROWSER_RECEIPT')
        java=a.java_log.read_text(encoding='utf-8');python=a.python_log.read_text(encoding='utf-8')
        check('Tests run: 11, Failures: 0, Errors: 0, Skipped: 0' in java and 'BUILD SUCCESS' in java,'M6_JAVA_PARITY')
        check('Ran 25 tests' in python and python.rstrip().endswith('OK'),'M6_PYTHON_TESTS')
        check(file_hash(SOURCE)==SOURCE_HASH,'M6_SOURCE_FINAL_HASH')
        original=ROOT/'artifacts/m3/freeze-1a1f2ec6-331e-4b02-9aaf-18804793d4e9/freeze.json'
        if original.exists():check(file_hash(original)==FREEZE_HASH,'M6_ORIGINAL_FREEZE_CHANGED')
        old_final=ROOT/'artifacts/m5/04c940db-313d-4a05-a039-90163e33f070/receipt.json'
        if old_final.exists():check(file_hash(old_final)==FINAL_HASH,'M6_ORIGINAL_FINAL_RECEIPT_CHANGED')
        resources=[]
        for path in sorted(session.glob('*.json')):
            value=json.loads(path.read_text(encoding='utf-8-sig'))
            if 'peak_sampled_rss_bytes' in value and 'command' in value:
                resources.append(dict(receipt=str(path.relative_to(ROOT)),label=path.name.split('-')[0],
                    status=value['status'],exit_code=value['exit_code'],started_at_utc=value['started_at_utc'],
                    finished_at_utc=value['finished_at_utc'],wall_seconds=value['elapsed_seconds'],
                    peak_sampled_rss_bytes=value['peak_sampled_rss_bytes'],disk_before_bytes=value['disk_before_bytes'],
                    disk_after_bytes=value['disk_after_bytes'],sha256=file_hash(path)))
        # These are separate measured steps with orchestration gaps, never an uninterrupted benchmark.
        check({'audit','import','preprocessing','prepare','model','final'} <= {r['label'] for r in resources if r['status']=='PASS'},
              'M6_MEASURED_STAGE_RECEIPTS')
        report.update(status='PASS',resources=resources,measurement_limits=
            '1s sampled RSS with shared pages/gaps, combined at each sample; logical disk snapshots; no exact peak or person-hours. Web group absent before M6 starts; M5 web not included.',
            http_receipt=str(a.http.relative_to(ROOT)),browser_receipt=str(a.browser.relative_to(ROOT)),
            validation_files_sha256={str(p.relative_to(ROOT)):file_hash(p) for p in (a.http,a.browser,a.java_log,a.python_log)},
            screenshots_sha256={str((ROOT/s['file']).relative_to(ROOT)):file_hash(ROOT/s['file']) for s in browser['screenshots']},
            web_process_id=web.pid,web_jar_sha256=file_hash(Path(json.loads((session/'web-process.json').read_text())['identity_path'])),
            audit_sha256=file_hash(session/'audit/audit.json'),script_sha256=file_hash(Path(__file__)),
            checks=['full workbook import/readback then fresh Spark preprocessing/preparation/train fit',
                    'frozen model/split/catalog/dev/final exact parity; no tuning',
                    'source payload/source bytes and entire historical M5 database preserved',
                    'M6 active/web identity; all HTTP and browser checks; Python/Java parity',
                    'runtime TV1 technical only; human review and TV2 assumption separately labelled'])
        incident_file=session/'runtime-incidents.json'
        if incident_file.exists():
            report['runtime_incidents']=json.loads(incident_file.read_text(encoding='utf-8'))
            report['runtime_incidents_sha256']=file_hash(incident_file)
    except Exception as exc:
        report.update(status='FAIL',error=str(exc),error_type=type(exc).__name__);raise
    finally:
        report['finished_at_utc']=now();save(target,report)
        print(json.dumps(dict(status=report['status'],receipt=str(target.relative_to(ROOT)))))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--session',required=True,type=Path);p.add_argument('--final-run',required=True)
    p.add_argument('--http',required=True,type=Path);p.add_argument('--browser',required=True,type=Path)
    p.add_argument('--java-log',required=True,type=Path);p.add_argument('--python-log',required=True,type=Path)
    a=p.parse_args()
    for name in ('http','browser','java_log','python_log'):setattr(a,name,getattr(a,name).resolve())
    main(a)
