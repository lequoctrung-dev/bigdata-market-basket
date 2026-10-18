"""Final read-only M5 repository/data/lifecycle check; never repairs historical data."""
import ast
from datetime import datetime
import json
from pathlib import Path
import re
import subprocess
import sys
import psutil
from bson.int64 import Int64
from pymongo import MongoClient
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'pipeline'))
from m2_source import ROOT, URI, DATABASE, SOURCE_HASH, check, save
from m2_runtime import verify_owned_mongo, writer_lock
from m3_prepare import now, file_hash
from m5_common import OUT, frozen_inputs, check_protected, verify_run, COLLECTIONS

FINAL='04c940db-313d-4a05-a039-90163e33f070'
BASELINE=OUT/'preflight-2026-10-18T142049.896081+0000.json'


def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT,text=True,encoding='utf-8').strip()


def main():
    report=dict(status='RUNNING',started_at_utc=now(),checks=[])
    target=OUT/('repository-final-'+now().replace(':','')+'.json')
    try:
        baseline=json.loads(BASELINE.read_text(encoding='utf-8'))
        verify_owned_mongo()
        with writer_lock(),MongoClient(URI) as client:
            db=client[DATABASE];frozen_inputs(db);check_protected(db,baseline['protected'])
            report['final_postcheck']=verify_run(db,FINAL)
            p=db.publication.find_one({'_id':'active'})
            check(p['run_id']==FINAL and p['version']==3 and isinstance(p['version'],Int64),'FINAL_ACTIVE_BSON_LONG')
            check(set(db.list_collection_names())=={'datasets','source_rows','baskets','runs','items','frequent_itemsets','association_rules','summaries','publication'},'NINE_COLLECTIONS')
            check(db.source_rows.count_documents({'dataset_id':SOURCE_HASH,'sheet_index':{'$type':'long'},'source_row':{'$type':'long'}})==1067371,'SOURCE_POSITIONS_BSON_LONG')
            check(db.baskets.count_documents({'basket_set_id':p['basket_set_id'],'retained_line_count':{'$type':'long'}})==39516,'BASKET_COUNTS_BSON_LONG')
            # Historical protected snapshots exclude test items; after first exposure
            # the FINAL receipt and local replay preserve content/mask evidence.
            report.update(publication=p,protected_ready_run_ids=list(baseline['protected']['runs']),
                protected_file_count=len(baseline['protected_files']))
            for name,expected in baseline['protected_files'].items():
                check(file_hash(ROOT/name)==expected,'PROTECTED_FILE_CHANGED_'+name)
            report['checks']+=['source/freeze/preparation/core code hashes','old READY manifests/outputs and M2/source/summaries unchanged',
                'FINAL file/Mongo/checksums/all-prediction replay','nine collections/BSON long/source counts']
        check(git('rev-parse','HEAD')==baseline['git_head'],'UNAUTHORIZED_COMMIT')
        check(not git('diff','--cached','--name-only'),'STAGED_CHANGES')
        subprocess.run(['git','diff','--check'],cwd=ROOT,check=True,capture_output=True)
        docs=['README.md','STATE.md','requirements-review/07_CONFIRMED_SCOPE.md','requirements-review/12_TECHNICAL_DESIGN.md',
              'requirements-review/13_MASTER_IMPLEMENTATION_PLAN.md','requirements-review/14_MILESTONE_CHECKLIST.md',
              'reports/M5_INTEGRATION_FINAL_EVALUATION_NOTES.md','web/README.md']
        links=[]
        for name in docs:
            path=ROOT/name
            for match in re.finditer(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
                ref=match.group(1).split('#',1)[0].strip('<>')
                if not ref or re.match(r'[a-zA-Z]+://',ref):continue
                check((path.parent/ref).exists(),'BROKEN_LINK_'+name+'_'+ref);links.append([name,ref])
        previous=git('show','HEAD:requirements-review/07_CONFIRMED_SCOPE.md')
        current=(ROOT/'requirements-review/07_CONFIRMED_SCOPE.md').read_text(encoding='utf-8')
        old_u=[line for line in previous.splitlines() if re.match(r'^\| U-\d+ \|',line)]
        check(all(line in current for line in old_u),'OLD_USER_DECISION_CHANGED')
        for name in ('01_REQUIREMENT_MATRIX.md','15_REQUIREMENT_MILESTONE_MAP.md'):
            ids=re.findall(r'^\|\s*([A-Z]+-[A-Z]+\d+)\s*\|',(ROOT/'requirements-review'/name).read_text(encoding='utf-8'),re.M)
            check(len(ids)==len(set(ids))==282,'REQUIREMENT_IDS_'+name)
        for name in ('artifacts/m5/review-20261018.json','data/raw/online-retail-ii/online_retail_II.xlsx',
                     '.venv/Scripts/python.exe','web/target/market-basket-m1-0.0.1-SNAPSHOT.jar','tmp/maven-repository'):
            check(subprocess.run(['git','check-ignore','-q',name],cwd=ROOT).returncode==0,'RUNTIME_NOT_IGNORED_'+name)
        python=(OUT/'python-final-regression-outside.log').read_text(encoding='utf-8')
        java=(OUT/'java-final-parity.log').read_text(encoding='utf-8')
        check('Ran 21 tests' in python and python.rstrip().endswith('OK'),'PYTHON_TEST_RECEIPT')
        check('Tests run: 11, Failures: 0, Errors: 0, Skipped: 0' in java and 'BUILD SUCCESS' in java,'JAVA_TEST_RECEIPT')
        for name in ('http-2026-10-18T143314.679489+0000.json','http-2026-10-18T151500.472862+0000.json',
            'browser-2026-10-18T151207.025Z.json','transition-2026-10-18T150804.813724+0000.json',
            'failure-campaign-3e9159d0-52a6-4a60-9807-e2c486afd44e/receipt.json'):
            check(json.loads((OUT/name).read_text(encoding='utf-8'))['status']=='PASS','RUNTIME_RECEIPT_'+name)
        review=json.loads((OUT/'review-20261018.json').read_text(encoding='utf-8'))
        check(review['decision_id']=='U-48' and review['run_id']==FINAL and
            review['runtime_receipt_sha256']==file_hash(OUT/FINAL/'receipt.json'),'USER_REVIEW_RECEIPT')
        saved=json.loads((OUT/'web-process.json').read_text(encoding='utf-8'))
        web=psutil.Process(saved['process_id'])
        check(abs(web.create_time()-datetime.fromisoformat(saved['started_at_utc'].replace('Z','+00:00')).timestamp())<.01
            and web.exe().lower()==saved['executable'].lower(),'WEB_PROCESS_IDENTITY')
        check(saved['identity_path'] in web.cmdline() and file_hash(Path(saved['identity_path'])).lower()==saved['jar_sha256'].lower()
            and file_hash(Path(saved['executable'])).lower()==saved['executable_sha256'].lower(),'WEB_ARGS_BINARY_JAR')
        check(any(c.status==psutil.CONN_LISTEN and c.laddr.ip=='127.0.0.1' and c.laddr.port==8081 for c in web.net_connections(kind='tcp')),'WEB_LOOPBACK_LISTENER')
        processes=[]
        for proc in psutil.process_iter(['pid','name','cmdline']):
            command=' '.join(proc.info['cmdline'] or [])
            if str(ROOT).lower() in command.lower() and proc.info['name'] in ('java.exe','chrome.exe'):
                processes.append(proc.info)
        check(all(x['pid']==web.pid for x in processes),'PROJECT_SPARK_OR_BROWSER_LEFT_RUNNING')
        code={}
        for folder,pattern in [('pipeline','m5_*.py'),('pipeline','test_m5*.py'),('scripts','*m5*'),('web/src','*')]:
            for path in (ROOT/folder).rglob(pattern):
                if path.is_file() and path.suffix in ('.py','.ps1','.mjs','.java','.html','.js','.css','.properties'):
                    code[path.relative_to(ROOT).as_posix()]=file_hash(path)
                    if path.suffix=='.py':ast.parse(path.read_text(encoding='utf-8'))
        report.update(status='PASS',linked_files_checked=len(links),old_user_rows_preserved=len(old_u),
            code_sha256=code,screenshot_sha256={p.name:file_hash(p) for p in sorted(OUT.glob('*.png'))},
            git_head=git('rev-parse','HEAD'),git_status=git('status','--short').splitlines(),
            lifecycle=dict(web_process_id=web.pid,web_jar_sha256=saved['jar_sha256'],
                mongo_process_id=json.loads((ROOT/'artifacts/m2/mongo-process.json').read_text(encoding='utf-8-sig'))['process_id'],
                project_java_chrome=processes,kept='Owned M5 web/Mongo retained for approved review/demo; Spark/Chrome stopped; unrelated27017 untouched'),
            human_review='ACCEPTED_U48; user-reported both members review/TV2 sample, no TV2 runtime claim')
        report['checks']+=['protected source/Word/RTM/map/pipeline/scripts unchanged','282 IDs/old U rows/links/diff/ignore/no staged/no commit',
            '21 Python/11 Java/runtime receipts/U48','current owned loopback identity/JAR; Spark/browser absent']
    except Exception as exc:report.update(status='FAIL',error=str(exc),error_type=type(exc).__name__);raise
    finally:
        report['finished_at_utc']=now();save(target,report)
        print(json.dumps(dict(status=report['status'],receipt=str(target.relative_to(ROOT)))))


if __name__=='__main__':main()
