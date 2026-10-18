"""Concurrent real pages across publication of an explicitly validated FINAL run."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import subprocess
import sys
import threading
import time
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request,urlopen
from pymongo import MongoClient
from verify_m4 import HTML
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'pipeline'))
from m2_source import ROOT, URI, DATABASE, check, save
from m2_runtime import verify_owned_mongo
from m3_prepare import now, file_hash
from m5_common import OUT, verify_run


def main(rid):
    verify_owned_mongo()
    report=dict(status='RUNNING',started_at_utc=now(),run_id=rid,requests=[],errors=[])
    path=OUT/('transition-'+now().replace(':','')+'.json');stop=threading.Event();threads=[]
    try:
        with MongoClient(URI) as client:
            db=client[DATABASE];verify_run(db,rid)
            old=db.publication.find_one({'_id':'active'})
            check(db.runs.find_one({'_id':rid})['evaluation_stage']=='FINAL' and rid!=old['run_id'],'NEW_FINAL_REQUIRED')
            report['before']=old
            def reader(route):
                try:
                    while not stop.is_set():
                        start=now()
                        with urlopen('http://127.0.0.1:8081'+route,timeout=30) as response:body=response.read().decode('utf-8');status=response.status
                        end=now();html=HTML(body);p=html.root.find(**{'class':'provenance'})[0].attrs
                        actual=(p['data-run'],int(p['data-version']))
                        check(actual in ((old['run_id'],old['version']),(rid,old['version']+1)) and status==200,'TRANSITION_SNAPSHOT')
                        for node in html.root.find('input',name='runId'):check(node.attrs['value']==actual[0],'FORM_RUN_SNAPSHOT')
                        for node in html.root.find('input',name='version'):check(int(node.attrs['value'])==actual[1],'FORM_VERSION_SNAPSHOT')
                        report['requests'].append(dict(route=route,started_at_utc=start,finished_at_utc=end,run_id=actual[0],version=actual[1],status=status))
                except Exception as exc:report['errors'].append(str(exc));stop.set()
            for route in ('/patterns','/basket'):
                t=threading.Thread(target=reader,args=(route,),daemon=True);threads.append(t);t.start()
            command=[sys.executable,'-X','utf8','scripts/m5_publish.py','--run-id',rid,'--expected-run',old['run_id'],
                     '--expected-version',str(old['version']),'--simulate-timeout-after']
            result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',timeout=180)
            path.with_suffix('.stdout.log').write_text(result.stdout,encoding='utf-8');path.with_suffix('.stderr.log').write_text(result.stderr,encoding='utf-8')
            report.update(publisher_command=command,publisher_exit_code=result.returncode)
            check(result.returncode==0,'TRANSITION_PUBLISHER_FAILED')
            current=db.publication.find_one({'_id':'active'})
            check(current['run_id']==rid and current['version']==old['version']+1,'FINAL_POINTER')
            # Let each reader finish at least one response from the new pointer.
            deadline=time.monotonic()+15
            while time.monotonic()<deadline and not all(any(r['run_id']==rid and r['route']==route for r in report['requests']) for route in ('/patterns','/basket')):
                time.sleep(.05)
            stop.set()
            for t in threads:t.join(35)
            check(not any(t.is_alive() for t in threads) and not report['errors'],'CONCURRENT_READER_ERROR')
            check(all(any(r['run_id']==who for r in report['requests']) for who in (old['run_id'],rid)),'BOTH_REAL_RUNS_OBSERVED')
            payload=urlencode([('runId',old['run_id']),('version',old['version']),('items','21080')]).encode()
            try:
                with urlopen(Request('http://127.0.0.1:8081/recommend',data=payload,headers={'Content-Type':'application/x-www-form-urlencoded'}),timeout=30) as response:status=response.status;body=response.read().decode('utf-8')
            except HTTPError as exc:status=exc.code;body=exc.read().decode('utf-8')
            check(status==409 and not HTML(body).recommendations(),'REAL_PREVIOUS_FORM_REJECTED')
            instant=datetime.fromisoformat(current['published_at_utc'])
            overlaps=[r for r in report['requests'] if datetime.fromisoformat(r['started_at_utc'])<=instant<=datetime.fromisoformat(r['finished_at_utc'])]
            check(overlaps,'NO_HTTP_REQUEST_OVERLAPPED_PUBLICATION')
            report.update(status='PASS',after=current,overlapping_requests=overlaps,old_form_status=status,
                driver_timeout='deliberate PyMongoError injection after acknowledged real CAS; readback APPLIED, no retry/version increment',
                checks=['concurrent real GET responses span CAS','each page/form exactly one old or new run/version',
                        'actual old form409','real FINAL only; no fixture active','timeout branch readback; exactly one version increment'])
    except Exception as exc:report.update(status='FAIL',error=str(exc),error_type=type(exc).__name__);raise
    finally:
        stop.set()
        for t in threads:t.join(35)
        report.update(finished_at_utc=now(),script_sha256=file_hash(Path(__file__)));save(path,report)
        print(json.dumps(dict(status=report['status'],receipt=str(path.relative_to(ROOT)),requests=len(report['requests']))))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run-id',required=True);main(p.parse_args().run_id)
