"""M5 FINAL: new immutable run, frozen identical model, explicit test-access ledger."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import sys
import uuid
from pymongo import MongoClient
from m2_source import ROOT, URI, DATABASE, check, digest, save, canonical
from m2_runtime import verify_owned_mongo, writer_lock, bson_counts
from m3_prepare import BASKET_SET, file_hash, now, jsonl, load_jsonl, provenance
from m3_protocol import PROTOCOL, mask, evaluate, logical_checksum
from m3_trial import write_readback
from m5_common import OUT, frozen_inputs, verify_run, outputs_for, protected_snapshot, check_protected, fail_unfinished
from m5_model import complete


def final_queries(baskets):
    return [dict(invoice=b['invoice'],invoice_time_local=b['invoice_time_local'],
                 query=mask(b['invoice'],b['items'])[0],target=mask(b['invoice'],b['items'])[1])
            for b in baskets if len(b['items']) >= 2]


def independent_predictions(queries, rules, catalog, k):
    """Exhaustive matching/sorting independent of RuleIndex and baseline()/metrics()."""
    rows=[]
    ordered=sorted(catalog,key=lambda r:(-r['train_basket_count'],r['stock_code']))
    known={r['stock_code'] for r in catalog}
    for q in queries:
        context=set(q['query'])
        matches=sorted([r for r in rules if all(c in context for c in r['antecedent'])
                        and r['consequent'] not in context],
            key=lambda r:(-r['confidence'],-r['lift'],-r['support'],r['consequent'],tuple(r['antecedent'])))
        best={}
        for r in matches: best.setdefault(r['consequent'],r)
        top=list(best.values())[:k]
        rows.append(dict(q,rules=[r['consequent'] for r in top],rule_keys=[r['rule_key'] for r in top],
            baseline=[r['stock_code'] for r in ordered if r['stock_code'] not in context][:k],
            new_target=q['target'] not in known,new_context=sorted(context-known)))
    return rows


def arithmetic(rows):
    return {m:dict(queries=len(rows),hits=sum(r['target'] in r[m] for r in rows),
        with_recommendations=sum(len(r[m])>0 for r in rows)) for m in ('rules','baseline')}


def verify_final(path, receipt, outputs):
    baskets=load_jsonl(path/'test-baskets.jsonl')
    queries=load_jsonl(path/'test-queries.jsonl')
    check(queries == final_queries(baskets),'ALL_TEST_MASK_REPLAY')
    split=receipt['split']['test']; ids=[b['invoice'] for b in baskets]
    check(len(ids) == len(set(ids)) == split['baskets'],'TEST_UNIQUE_COUNT')
    check(sum(len(b['items'])==1 for b in baskets) == split['single_item_baskets']
        and all(b['items'] and b['items']==sorted(set(b['items'])) for b in baskets),'TEST_ARRAYS_SINGLES')
    predictions,metric=evaluate(queries,outputs['association_rules'],outputs['items'],int(PROTOCOL['k']))
    check(metric == receipt['final'] and len(queries) == receipt['counts']['eligible_test_queries'],'FINAL_METRICS_REPLAY')
    stored=load_jsonl(path/'test-predictions.jsonl')
    core=[{k:v for k,v in r.items() if k not in ('best_rules','rules_hit','baseline_hit','rules_nonempty','baseline_nonempty')} for r in stored]
    check(core == predictions == independent_predictions(queries,outputs['association_rules'],outputs['items'],int(PROTOCOL['k'])), 'ALL_FINAL_INDEPENDENT_PREDICTIONS')
    rules={r['rule_key']:r for r in outputs['association_rules']}
    for r in stored:
        check(r['best_rules'] == [{k:v for k,v in rules[key].items() if k not in ('_id','run_id')} for key in r['rule_keys']], 'FINAL_BEST_RULES')
        for method in ('rules','baseline'):
            check(r[method+'_hit'] == (r['target'] in r[method]) and r[method+'_nonempty'] == bool(r[method]), 'FINAL_QUERY_FLAGS')
    for method,counts in arithmetic(predictions).items():
        check(all(receipt['final']['all'][method][k] == v for k,v in counts.items()),'FINAL_INDEPENDENT_ARITHMETIC')
    return dict(status='PASS',queries=len(queries),arithmetic=arithmetic(predictions),sample_predictions=stored[:10],
                sample_arithmetic=arithmetic(stored[:10]),verifier_sha256=file_hash(Path(__file__)))


def main(integrated_run, e2e):
    verify_owned_mongo()
    with writer_lock(), MongoClient(URI) as client:
        db=client[DATABASE]
        frozen, prep_path, prep=frozen_inputs(db)
        verify_run(db,integrated_run)
        gate=json.loads(e2e.read_text(encoding='utf-8'))
        check(gate['status']=='PASS' and gate['run_id']==integrated_run and gate['evaluation_stage']=='DEVELOPMENT'
            and gate['requests'] and gate['source_to_web_verified'] is True,'END_TO_END_BEFORE_TEST_GATE')
        source=db.runs.find_one({'_id':integrated_run})
        check(source['evaluation_stage']=='DEVELOPMENT' and source['manifest']['milestone']=='M5','M5_INTEGRATED_MODEL_REQUIRED')
        before=protected_snapshot(db)
        rid=str(uuid.uuid4()); path=OUT/rid; path.mkdir(parents=True,exist_ok=False)
        receipt=dict(source['manifest'])
        receipt.update(run_id=rid,evaluation_stage='FINAL',status='RUNNING',started_at_utc=now(),
            human_review='PENDING_BOTH',model_source_run_id=integrated_run,
            model_source_receipt_sha256=file_hash(OUT/integrated_run/'receipt.json'),
            e2e_gate=str(e2e.relative_to(ROOT)),e2e_gate_sha256=file_hash(e2e),
            execution='unchanged verified M5 train model rekeyed to new FINAL UUID; no refit/selection after test',
            steps=[],checks=[],**provenance())
        receipt.pop('finished_at_utc',None);receipt.pop('files_sha256',None)
        run={k:v for k,v in source.items() if k!='manifest'}
        run.update(_id=rid,run_id=rid,status='WRITING',stage='MODEL_FINAL',evaluation_stage='FINAL')
        db.runs.insert_one(bson_counts(run));save(path/'receipt.json',receipt)
        start=time.monotonic()
        try:
            outputs=outputs_for(db,integrated_run)
            for name,rows in outputs.items():
                for row in rows:
                    row['run_id']=rid
                    if name=='items': row['_id']=canonical([rid,row['stock_code']])
                    else: row['_id']=canonical([rid,digest(row['items'] if name=='frequent_itemsets' else [row['antecedent'],row['consequent']])])
                jsonl(path/f'{name}.jsonl',rows)
            receipt['output_validation']=write_readback(db,outputs,rid)
            check(receipt['output_validation']==frozen['output_validation'],'FINAL_FROZEN_MODEL_BEFORE_TEST')
            jsonl(path/'dev-predictions.jsonl',load_jsonl(OUT/integrated_run/'dev-predictions.jsonl'))
            # Persist BEFORE the first Mongo cursor requests any final test items.
            # This file survives failures and is never rewritten or hidden by retries.
            access=dict(event='FIRST_TEST_ITEMS_READ_ATTEMPT',at_utc=now(),run_id=rid,
                freeze_sha256=receipt['freeze_sha256'],protocol_sha256=digest(PROTOCOL),
                command_args=sys.argv,code_sha256=receipt['code_sha256'],
                model_validation=receipt['output_validation'],e2e_sha256=file_hash(e2e))
            with (path/'test-access.json').open('x',encoding='utf-8') as stream: json.dump(access,stream,ensure_ascii=False,indent=2)
            receipt['test_access']=access
            baskets=list(db.baskets.find({'basket_set_id':BASKET_SET,'invoice_time_local':
                {'$gte':PROTOCOL['test_start'],'$lt':PROTOCOL['test_end']}},{'_id':0}).sort('invoice',1))
            metadata=[{k:b[k] for k in ('invoice','invoice_time_local')} for b in baskets]
            expected=[{k:b[k] for k in ('invoice','invoice_time_local')} for b in load_jsonl(prep_path/'split-metadata.jsonl') if b['split']=='test']
            check(metadata==expected and logical_checksum(metadata)==prep['split']['test']['invoice_time_sha256'],'TEST_FROZEN_MEMBERSHIP')
            check(all(b['items'] and b['items']==sorted(set(b['items'])) for b in baskets),'TEST_BASKET_CANONICAL')
            # Only now, after the exposure ledger, verify the full M2 basket
            # content checksum including the previously sealed test items.
            combined=sorted(load_jsonl(prep_path/'train-baskets.jsonl')+load_jsonl(prep_path/'dev-baskets.jsonl')+baskets,
                            key=lambda b:b['invoice'])
            basket_hash=hashlib.sha256()
            for b in combined:
                basket_hash.update((canonical([b['invoice'],b['items'],b['invoice_time_local'],b['retained_line_count']])+'\n').encode('utf-8'))
            m2=db.runs.find_one({'_id':receipt['preprocessing_run_id']})['manifest']
            check(basket_hash.hexdigest()==m2['basket_checksum'],'FULL_M2_BASKET_CHECKSUM_AFTER_TEST_ACCESS')
            receipt['m2_basket_checksum_after_test_access']=basket_hash.hexdigest()
            queries=final_queries(baskets)
            predictions,metric=evaluate(queries,outputs['association_rules'],outputs['items'],int(PROTOCOL['k']))
            check(predictions==independent_predictions(queries,outputs['association_rules'],outputs['items'],int(PROTOCOL['k'])),'FINAL_INDEPENDENT_PREDICTIONS')
            rules={r['rule_key']:r for r in outputs['association_rules']}
            detailed=[]
            for r in predictions:
                detailed.append(dict(r,best_rules=[{k:v for k,v in rules[key].items() if k not in ('_id','run_id')} for key in r['rule_keys']],
                    **{method+suffix: (r['target'] in r[method] if suffix=='_hit' else bool(r[method]))
                       for method in ('rules','baseline') for suffix in ('_hit','_nonempty')}))
            jsonl(path/'test-baskets.jsonl',baskets);jsonl(path/'test-queries.jsonl',queries);jsonl(path/'test-predictions.jsonl',detailed)
            receipt['split']=json.loads(json.dumps(prep['split']))
            receipt['split']['test'].update(single_item_baskets=sum(len(b['items'])==1 for b in baskets),
                eligible_queries=len(queries),max_basket_size=max((len(b['items']) for b in baskets),default=0),basket_sha256=logical_checksum(baskets))
            receipt['counts']=dict(receipt['counts'],eligible_test_queries=len(queries))
            receipt.update(final=metric,final_status='MEASURED',final_new_items=dict(
                targets=sum(r['new_target'] for r in predictions),queries_with_new_context=sum(bool(r['new_context']) for r in predictions),
                context_occurrences=sum(len(r['new_context']) for r in predictions),no_rule_queries=sum(not r['rules'] for r in predictions)))
            save(path/'independent-final-verification.json',verify_final(path,receipt,outputs))
            check_protected(db,before)
            receipt.update(elapsed_seconds=time.monotonic()-start,
                steps=[dict(name='copy_frozen_model_test_access_evaluation_independent_check',seconds=time.monotonic()-start,end_at_utc=now())])
            complete(db,path,receipt)
            print(canonical(dict(status='PASS',run_id=rid,final=metric['all'])))
        except Exception as exc:
            fail_unfinished(db,path,receipt,exc)
            raise


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--integrated-run',required=True)
    parser.add_argument('--e2e-receipt',type=Path,required=True)
    args=parser.parse_args();main(args.integrated_run,args.e2e_receipt.resolve())
