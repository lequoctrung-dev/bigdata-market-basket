"""Read-only real M4 HTTP and DB readback evidence; never fit/test-final/mutate outputs."""
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import sys
import threading
import time
import zipfile
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import psutil
from pymongo import MongoClient

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'pipeline'))
from m2_source import URI, DATABASE, canonical, check, save
from m2_runtime import verify_owned_mongo
from m3_protocol import RuleIndex
from m3_prepare import file_hash


class Node:
    def __init__(self, tag='', attrs=()): self.tag,self.attrs,self.children=tag,dict(attrs),[]
    def text(self): return ''.join(c if isinstance(c,str) else c.text() for c in self.children).strip()
    def find(self, tag=None, **attrs):
        out=[]
        if (tag is None or self.tag==tag) and all(self.attrs.get(k)==v for k,v in attrs.items()): out.append(self)
        for c in self.children:
            if isinstance(c,Node): out.extend(c.find(tag,**attrs))
        return out


class HTML(HTMLParser):
    def __init__(self, html):
        super().__init__();self.root=Node();self.stack=[self.root];self.feed(html)
    def handle_starttag(self,tag,attrs):
        n=Node(tag,attrs);self.stack[-1].children.append(n)
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}: self.stack.append(n)
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==tag: self.stack=self.stack[:i];break
    def handle_data(self,data): self.stack[-1].children.append(data)
    def element(self,id): return self.root.find(id=id)[0]
    def table(self,id): return [[c.text() for c in r.find('td')] for r in self.element(id).find('tr') if r.find('td')]
    def recommendations(self): return [r.attrs['data-code'] for r in self.element('recommendations').find('article')]


def main():
    started=datetime.now(timezone.utc).isoformat(); timings=[]; checks=[]; samples=[]
    target=ROOT/'artifacts/m4'/('http-'+started.replace(':','')+'.json')
    resources=[];stop=threading.Event();sampler=None
    report=dict(started_at_utc=started,status='RUNNING',scope='TV1 real DEVELOPMENT HTTP, not human review/M6',checks=checks,requests=timings,samples=samples,resource_samples=resources)
    def request(path, fields=None, expected=200):
        before=time.perf_counter()
        req=Request('http://127.0.0.1:8081'+path,data=urlencode(fields).encode() if fields is not None else None)
        if fields is not None: req.add_header('Content-Type','application/x-www-form-urlencoded')
        try:
            with urlopen(req,timeout=30) as response: status,body=response.status,response.read().decode()
        except HTTPError as e: status,body=e.code,e.read().decode()
        timings.append(dict(path=path,method='POST' if fields is not None else 'GET',status=status,seconds=time.perf_counter()-before,bytes=len(body.encode())))
        if status!=expected:
            (ROOT/'artifacts/m4'/('failed-response-'+str(time.time_ns())+'.html')).write_text(body,encoding='utf-8')
        check(status==expected,f'HTTP_{status}_EXPECTED_{expected}_'+path)
        return HTML(body),body
    try:
        verify_owned_mongo()
        with MongoClient(URI) as client:
            db=client[DATABASE];p=db.publication.find_one({'_id':'active'});rid=p['run_id']
            m=db.runs.find_one({'_id':rid})['manifest'];basket=p['basket_set_id']
            report.update(run_id=rid,version=p['version'],basket_set_id=basket,source=m['dataset_id'],config=m['config'])
            process=json.loads((ROOT/'artifacts/m4/web-process.json').read_text())
            web=psutil.Process(process['process_id']);report['web_rss_before_bytes']=web.memory_info().rss
            mongo=psutil.Process(json.loads((ROOT/'artifacts/m2/mongo-process.json').read_text())['process_id'])
            def sample_resources():
                while not stop.is_set():
                    try: resources.append(dict(at_utc=datetime.now(timezone.utc).isoformat(),web_rss_bytes=web.memory_info().rss,mongo_rss_bytes=mongo.memory_info().rss,python_rss_bytes=psutil.Process().memory_info().rss,available_ram_bytes=psutil.virtual_memory().available))
                    except psutil.Error: pass
                    stop.wait(1)
            sampler=threading.Thread(target=sample_resources,daemon=True);sampler.start()
            with zipfile.ZipFile(process['identity_path']) as jar:
                report['web_libraries']=[n for n in jar.namelist() if n.startswith('BOOT-INF/lib/') and any(v in n for v in ['spring-boot-','spring-data-mongodb-','mongodb-driver-','bson-','tomcat-embed-core','thymeleaf-'])]
            # Only examine this project's Java processes; unrelated JVMs remain untouched.
            jvms=[]
            for proc in psutil.process_iter(['pid','name','cmdline']):
                try:
                    if proc.info['name']=='java.exe' and str(ROOT).lower() in ' '.join(proc.info['cmdline'] or []).lower(): jvms.append(proc.info)
                except psutil.Error: pass
            check(all(str(process['identity_path']).lower() in ' '.join(x['cmdline']).lower() for x in jvms),'PROJECT_SPARK_MUST_BE_STOPPED')
            report['project_java_processes']=jvms
            catalog=list(db.items.find({'run_id':rid}));rules=list(db.association_rules.find({'run_id':rid}));sets=list(db.frequent_itemsets.find({'run_id':rid}))
            summary=list(db.summaries.find({'basket_set_id':basket}))
            overview,body=request('/')
            check(overview.element('basket-count').text()==str(m['stage_counts']['baskets']),'UI_BASKET_COUNT')
            check(overview.element('item-count').text()==str(m['stage_counts']['items']),'UI_ALL_PERIOD_ITEM_COUNT')
            monthly=sorted([r for r in summary if r['summary_type']=='month'],key=lambda r:r['bucket_key'])
            expected=[[r['bucket_key'],str(r['payload']['invoices']),str(Decimal(r['payload']['line_value_gbp']).quantize(Decimal('.01'),rounding=ROUND_HALF_UP))] for r in monthly]
            check(overview.table('monthly')==expected,'EVERY_MONTH_GBP_INVOICES')
            amount=sum(Decimal(r['payload']['line_value_gbp']) for r in monthly)
            check(overview.element('amount').text()==str(amount.quantize(Decimal('.01'),rounding=ROUND_HALF_UP))+' GBP','FINAL_SUM_BIGDECIMAL_HALF_UP')
            sizes=sorted([[int(r['bucket_key']),r['payload']['baskets']] for r in summary if r['summary_type']=='basket_size'])
            check(overview.table('distribution')==[[str(x),str(n)] for x,n in sizes],'EVERY_BASKET_SIZE')
            report['kpi']=dict(baskets=m['stage_counts']['baskets'],items=m['stage_counts']['items'],months=len(monthly),sizes=len(sizes),amount_exact=str(amount),amount_ui=overview.element('amount').text())
            checks.extend(['real pointer/run/version/source/config','all 25 month/426 distribution buckets','money exact aggregate then HALF_UP','Spark stopped; HTTP consumes outputs'])
            patterns,body=request('/patterns')
            check('505 / 4293' in body and '109 / 4293' in body and '3513 / 4293' in body and 'NOT_RUN' in body,'DEVELOPMENT_METRICS_FINAL_LABEL')
            prefix=[('runId',rid),('version',str(p['version']))]
            basket_html,_=request('/basket'); options=basket_html.root.find('input',name='items')
            check({n.attrs['value'] for n in options}=={r['stock_code'] for r in catalog} and len(options)==len(catalog),'ENTIRE_TRAIN_CATALOG')
            index=RuleIndex(rules)
            cases=[('real_dev_558640',['21080','21094','21467','21770','22704','22969']),('one',['21080']),('many',['21080','21094']),('missing_one',['21094']),('existing',['21080','21094','21086']),('duplicate',['21080','21080','21094'])]
            used={c for r in rules for c in r['antecedent']+[r['consequent']]}
            no_rule=next(r['stock_code'] for r in catalog if r['stock_code'] not in used);cases.append(('catalog_no_rule',[no_rule]))
            for name,query in cases:
                html,body=request('/recommend',prefix+[('items',c) for c in query])
                expected=index.recommend(query,int(m['config']['k']));actual=html.recommendations()
                check(actual==[r['consequent'] for r in expected],'REAL_RANKING_'+name)
                actual_a=[n.attrs['data-antecedent'].split('|') for n in html.element('recommendations').find('article')]
                check(actual_a==[r['antecedent'] for r in expected],'BEST_ANTECEDENT_'+name)
                samples.append(dict(name=name,query=query,expected=expected,actual=actual,actual_antecedents=actual_a))
            check(samples[0]['actual']==['21086','21212'],'GOLDEN_REAL_DEV_CASE')
            for label,fields,status in [('empty',prefix,400),('unknown',prefix+[('items','21080'),('items','UNKNOWN')],400),
                ('stale',[('runId',rid),('version','0'),('items','21080')],409),('invalid_version',[('runId',rid),('version','x'),('items','21080')],400),
                ('object_query',prefix+[('items[$ne]','21080')],400)]:
                html,body=request('/recommend',fields,status)
                check(not html.recommendations(),'INVALID_INPUT_HAS_NO_PREDICTIONS_'+label)
            # All distinct catalog items are valid as a basket, with no truncation.
            html,body=request('/recommend',prefix+[('items',r['stock_code']) for r in catalog])
            check(not html.recommendations() and len(html.root.find('input',checked='checked'))==len(catalog),'ENTIRE_CATALOG_BASKET_UNTRUNCATED')
            for path in ['/?page=-1','/?page=999999','/?sort=bad','/patterns?min=NaN','/patterns?kind=bad','/patterns?size=-1','/patterns?sort=frequency','/basket?items%5B%24where%5D=1']:
                request(path,expected=400)
            # Verify every page of model tables against real DB in deterministic order.
            order=sorted(rules,key=lambda r:(-r['confidence'],-r['lift'],-r['support'],r['consequent'],tuple(r['antecedent'])))
            names={r['stock_code']:r['display_name'] for r in catalog}
            for page in range((len(order)+24)//25):
                html,_=request('/patterns?'+urlencode(prefix+[('page',str(page))]))
                actual=html.table('rules');chunk=order[page*25:(page+1)*25]
                check(len(actual)==len(chunk) and all(a[0]==' + '.join(c+' — '+names[c] for c in r['antecedent']) and a[1]==r['consequent']+' — '+names[r['consequent']]
                    and list(map(float,a[2:]))==[r['confidence'],r['lift'],r['support']] for a,r in zip(actual,chunk)),'EVERY_RULE_PAGE_'+str(page))
            order=sorted(sets,key=lambda r:(-r['frequency'],r['itemset_key']))
            for page in range((len(order)+24)//25):
                html,_=request('/patterns?'+urlencode(prefix+[('kind','itemsets'),('sort','frequency'),('page',str(page))]))
                actual=html.table('itemsets');chunk=order[page*25:(page+1)*25]
                check(len(actual)==len(chunk) and all(a[0]==' + '.join(c+' — '+names[c] for c in r['items']) and int(a[1])==r['frequency'] and float(a[2])==r['support'] for a,r in zip(actual,chunk)),'EVERY_ITEMSET_PAGE_'+str(page))
            for sort in ['quantity','baskets','code']:
                html,_=request('/?'+urlencode(prefix+[('sort',sort)]))
                rows=[r for r in summary if r['summary_type']=='item'];rows.sort(key=(lambda r:r['bucket_key']) if sort=='code' else lambda r:(-r['payload'][sort],r['bucket_key']))
                check(html.table('popular')==[[r['bucket_key'],str(r['payload']['baskets']),str(r['payload']['quantity'])] for r in rows[:25]],'POPULAR_SORT_'+sort)
            request('/patterns?kind=rules&sort=lift&min=0.01&size=2&q=21080')
            html,_=request('/patterns?q=ZZZZ_NO_MATCH');check(not html.table('rules'),'EMPTY_FILTER')
            request('/patterns?kind=itemsets&sort=support&q=HEART')
            check(db.publication.find_one({'_id':'active'})==p,'POINTER_UNCHANGED_BY_HTTP')
            checks.extend(['full train catalog/no-rule item','single/multiple/missing antecedent/existing/dedup matches Python','full 4556-item basket retained',
                'invalid/empty/unknown/stale/object input','all 856 rules/1349 itemsets paginated without loss','popular sorts/search/filter/empty','pointer unchanged'])
            report.update(status='PASS',web_rss_after_bytes=web.memory_info().rss,web_jar_sha256=file_hash(Path(process['identity_path'])),
                verifier_sha256=file_hash(Path(__file__)),human_review='PENDING_TV1',final_status='NOT_RUN')
    except Exception as exc:
        report.update(status='FAIL',error=str(exc),error_type=type(exc).__name__);raise
    finally:
        stop.set()
        if sampler: sampler.join(timeout=2)
        report['measurement_method']='HTTP wall includes Mongo reads/validation/filter/render/network; resource RSS sampled each second, shared pages included, gaps may miss peaks; no SLA or isolated query timing'
        if resources: report['sampled_peak_bytes']={key:max(r[key] for r in resources) for key in ('web_rss_bytes','mongo_rss_bytes','python_rss_bytes')}
        report['finished_at_utc']=datetime.now(timezone.utc).isoformat();save(target,report)
        print(canonical(dict(status=report['status'],receipt=str(target.relative_to(ROOT)),requests=len(timings))))


if __name__=='__main__': main()
