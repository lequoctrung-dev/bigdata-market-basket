"""M5 real HTTP gate; manifest-driven dev/final, one snapshot on every response."""
import argparse
from decimal import Decimal, ROUND_HALF_UP
import json
from pathlib import Path
import sys
import threading
import time
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request,urlopen
import psutil
from pymongo import MongoClient
from verify_m4 import HTML
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'pipeline'))
from m2_source import ROOT, check, save
from m2_runtime import verify_owned_mongo
from m3_prepare import now, file_hash, load_jsonl
from m3_protocol import RuleIndex
from m6_common import URI, DATABASE, context
from m6_verify import verify_run, owned_web


def main(args):
    OUT=args.session.resolve()
    context(OUT)
    report=dict(status='RUNNING',started_at_utc=now(),requests=[],checks=[],resource_samples=[])
    path=OUT/('http-'+now().replace(':','')+'.json')
    stop=threading.Event();sampler=None
    try:
        verify_owned_mongo()
        with MongoClient(URI) as client:
            db=client[DATABASE];pointer=db.publication.find_one({'_id':'active'});rid=pointer['run_id']
            run=db.runs.find_one({'_id':rid});m=run['manifest'];stage=m['evaluation_stage']
            check(m['milestone']=='M6','M6_HTTP_TARGET_REQUIRED')
            report['postcheck']=verify_run(db,rid,OUT)
            report.update(run_id=rid,version=pointer['version'],evaluation_stage=stage,source=m['dataset_id'],config=m['config'])
            saved=json.loads((OUT/'web-process.json').read_text(encoding='utf-8'))
            web=owned_web(OUT)
            mongo=psutil.Process(json.loads((ROOT/'artifacts/m2/mongo-process.json').read_text(encoding='utf-8-sig'))['process_id'])
            def sampling():
                while not stop.is_set():
                    report['resource_samples'].append(dict(at_utc=now(),web_rss_bytes=web.memory_info().rss,
                        mongo_rss_bytes=mongo.memory_info().rss,python_rss_bytes=psutil.Process().memory_info().rss,
                        available_ram_bytes=psutil.virtual_memory().available))
                    stop.wait(1)
            sampler=threading.Thread(target=sampling,daemon=True);sampler.start()
            jvms=[]
            for proc in psutil.process_iter(['pid','name','cmdline']):
                if proc.info['name']=='java.exe' and str(ROOT).lower() in ' '.join(proc.info['cmdline'] or []).lower(): jvms.append(proc.info)
            check(all(saved['identity_path'].lower() in ' '.join(p['cmdline']).lower() for p in jvms),'SPARK_STOPPED_DURING_HTTP')
            report['project_java_processes']=jvms
            def request(route,fields=None,status=200):
                start=time.perf_counter();req=Request('http://127.0.0.1:8081'+route,data=urlencode(fields).encode() if fields is not None else None)
                if fields is not None: req.add_header('Content-Type','application/x-www-form-urlencoded')
                try:
                    with urlopen(req,timeout=30) as response: actual,body=response.status,response.read().decode('utf-8')
                except HTTPError as exc: actual,body=exc.code,exc.read().decode('utf-8')
                report['requests'].append(dict(route=route,method='GET' if fields is None else 'POST',status=actual,seconds=time.perf_counter()-start,bytes=len(body.encode())))
                check(actual==status,'HTTP_'+str(actual)+'_EXPECTED_'+str(status)+'_'+route)
                html=HTML(body)
                provenance=html.root.find(**{'class':'provenance'})
                check(len(provenance)==1 and provenance[0].attrs['data-run']==rid
                    and int(provenance[0].attrs['data-version'])==pointer['version'],'EVERY_REQUEST_ONE_SNAPSHOT')
                return html,body
            prefix=[('runId',rid),('version',str(pointer['version']))]
            catalog=list(db.items.find({'run_id':rid}));rules=list(db.association_rules.find({'run_id':rid}));sets=list(db.frequent_itemsets.find({'run_id':rid}))
            summaries=list(db.summaries.find({'basket_set_id':pointer['basket_set_id']}))
            html,body=request('/')
            check(html.element('basket-count').text()==str(m['stage_counts']['baskets']) and html.element('item-count').text()==str(m['stage_counts']['items']),'OVERVIEW_DENOMINATORS')
            monthly=sorted([r for r in summaries if r['summary_type']=='month'],key=lambda r:r['bucket_key'])
            money=lambda value:str(Decimal(value).quantize(Decimal('.01'),rounding=ROUND_HALF_UP))
            check(html.table('monthly')==[[r['bucket_key'],str(r['payload']['invoices']),money(r['payload']['line_value_gbp'])] for r in monthly],'ALL_MONTHLY_BUCKETS')
            check(html.element('amount').text()==money(sum(Decimal(r['payload']['line_value_gbp']) for r in monthly))+' GBP','EXACT_GBP_HALF_UP')
            sizes=sorted((int(r['bucket_key']),r['payload']['baskets']) for r in summaries if r['summary_type']=='basket_size')
            check(html.table('distribution')==[[str(a),str(b)] for a,b in sizes],'ALL_SIZE_BUCKETS')
            html,body=request('/patterns')
            for key,table in [('development','evaluation')]+([('final','final-evaluation')] if stage=='FINAL' else []):
                actual=html.table(table)
                for row,method in zip(actual,('rules','baseline')):
                    metric=m[key]['all'][method];n=metric['queries']
                    check(row[1]==f"{metric['hits']} / {n}" and row[3]==f"{metric['with_recommendations']} / {n}", 'METRIC_NUMERATOR_DENOMINATOR_'+key)
                    if n: check(row[2]==f"{100*metric['hits']/n:.4f}%" and row[4]==f"{100*metric['with_recommendations']/n:.4f}%",'METRIC_PERCENT_'+key)
            check(('MEASURED' if stage=='FINAL' else 'NOT_RUN') in html.element('final-status').text(),'TRUTHFUL_FINAL_LABEL')
            html,_=request('/basket')
            check({x.attrs['value'] for x in html.root.find('input',name='items')}=={r['stock_code'] for r in catalog},'WHOLE_TRAIN_CATALOG')
            index=RuleIndex(rules)
            cases=[['21080','21094','21467','21770','22704','22969'],['21080'],['21094'],['21080','21094','21086'],['21080','21080']]
            used={c for r in rules for c in r['antecedent']+[r['consequent']]}
            cases.append([next(r['stock_code'] for r in catalog if r['stock_code'] not in used)])
            if stage=='FINAL': cases.extend(r['query'] for r in load_jsonl(OUT/rid/'test-predictions.jsonl')[:10])
            known={r['stock_code'] for r in catalog}
            for query in cases:
                if not set(query)<=known:
                    # Offline evaluation retains unknown context in its denominator.
                    # The interactive form accepts only the run's train catalog.
                    html,_=request('/recommend',prefix+[('items',c) for c in query],400)
                    check(not html.recommendations(),'OFFLINE_UNKNOWN_CONTEXT_REJECTED_BY_INTERACTIVE_FORM')
                    continue
                html,_=request('/recommend',prefix+[('items',c) for c in query])
                expected=index.recommend(query,int(m['config']['k']))
                check(html.recommendations()==[r['consequent'] for r in expected],'REAL_HTTP_RANKING')
                check([r.attrs['data-antecedent'].split('|') for r in html.element('recommendations').find('article')]==[r['antecedent'] for r in expected],'REAL_HTTP_BEST_RULE')
            for fields,status in [(prefix,400),(prefix+[('items','UNKNOWN')],400),
                ([('runId',rid),('version','0'),('items','21080')],409),(prefix+[('items[$ne]','21080')],400)]:
                html,_=request('/recommend',fields,status);check(not html.recommendations(),'ERROR_NO_PREDICTIONS')
            if args.previous_run:
                html,_=request('/recommend',[('runId',args.previous_run),('version',str(args.previous_version)),('items','21080')],409)
                check(not html.recommendations(),'ACTUAL_PREVIOUS_PUBLICATION_FORM_STALE')
            html,_=request('/recommend',prefix+[('items',r['stock_code']) for r in catalog])
            check(len(html.root.find('input',checked='checked'))==len(catalog) and not html.recommendations(),'WHOLE_CATALOG_NO_TRUNCATION')
            names={r['stock_code']:r['display_name'] for r in catalog}
            order=sorted(rules,key=lambda r:(-r['confidence'],-r['lift'],-r['support'],r['consequent'],tuple(r['antecedent'])))
            for page in range((len(order)+24)//25):
                html,_=request('/patterns?'+urlencode(prefix+[('page',page)]));chunk=order[page*25:(page+1)*25]
                rows=html.table('rules')
                check(len(rows)==len(chunk) and all(a[0]==' + '.join(c+' — '+names[c] for c in r['antecedent'])
                    and a[1]==r['consequent']+' — '+names[r['consequent']]
                    and list(map(float,a[2:]))==[r['confidence'],r['lift'],r['support']] for a,r in zip(rows,chunk)),'EVERY_RULE_PAGE')
            order=sorted(sets,key=lambda r:(-r['frequency'],r['itemset_key']))
            for page in range((len(order)+24)//25):
                html,_=request('/patterns?'+urlencode(prefix+[('kind','itemsets'),('sort','frequency'),('page',page)]));chunk=order[page*25:(page+1)*25]
                rows=html.table('itemsets')
                check(len(rows)==len(chunk) and all(a[0]==' + '.join(c+' — '+names[c] for c in r['items'])
                    and int(a[1])==r['frequency'] and float(a[2])==r['support'] for a,r in zip(rows,chunk)),'EVERY_ITEMSET_PAGE')
            for route in ['/?page=-1','/?sort=bad','/patterns?min=NaN','/patterns?size=-1']:
                request(route,status=400)
            check(db.publication.find_one({'_id':'active'})==pointer,'HTTP_READ_ONLY_POINTER')
            report.update(status='PASS',source_to_web_verified=True,web_jar_sha256=file_hash(Path(saved['identity_path'])),
                checks=['every response run/version snapshot','all month/size/money/model rows','all train catalog and full basket',
                        'rank/best rule/invalid/stale/no fallback','manifest dev/final numerator and denominator','Spark stopped; web read only'],
                verifier_sha256=file_hash(Path(__file__)),human_review='PENDING_BOTH')
    except Exception as exc:
        report.update(status='FAIL',error_type=type(exc).__name__,error=str(exc));raise
    finally:
        stop.set()
        if sampler: sampler.join(2)
        report['measurement_method']='RSS sampled 1s with shared pages/gaps; HTTP wall includes DB/validation/render/transfer, not isolated query timing or SLA'
        if report['resource_samples']: report['sampled_peak_bytes']={k:max(s[k] for s in report['resource_samples']) for k in ('web_rss_bytes','mongo_rss_bytes','python_rss_bytes')}
        report['finished_at_utc']=now();save(path,report)
        print(json.dumps(dict(status=report['status'],receipt=str(path.relative_to(ROOT)),requests=len(report['requests']))))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--session',required=True,type=Path);p.add_argument('--previous-run');p.add_argument('--previous-version',type=int)
    main(p.parse_args())
