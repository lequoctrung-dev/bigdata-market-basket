"""M5 stage-aware, read-only validation; frozen M2/M3 code remains unchanged."""
import json
from pathlib import Path
import uuid

from m2_source import ROOT, SOURCE, SOURCE_HASH, SCHEMA, POLICY, canonical, check, digest, save
from m2_runtime import require_ready, bson_counts
from m3_prepare import BASKET_SET, M2_RUN, file_hash, load_jsonl, now, verified_preparation
from m3_protocol import PROTOCOL, evaluate, logical_checksum, validate_rule
from m3_verify import verify_run as verify_m3, require_bson_longs

OUT = ROOT/'artifacts/m5'
FREEZE = ROOT/'artifacts/m3/freeze-1a1f2ec6-331e-4b02-9aaf-18804793d4e9'
FREEZE_HASH = 'f7ee9c13432f0c99e7e5bcbf0363eed77eb4d5493b39e78fbb2e8e48557d053a'
COLLECTIONS = ('items', 'frequent_itemsets', 'association_rules')


def frozen_inputs(db):
    check(file_hash(FREEZE/'freeze.json') == FREEZE_HASH, 'FREEZE_HASH')
    frozen = json.loads((FREEZE/'freeze.json').read_text(encoding='utf-8'))
    for name, expected in json.loads((FREEZE/'hashes.json').read_text()).items():
        check(file_hash(FREEZE/name) == expected, 'FREEZE_FILE_'+name)
    check(frozen['protocol'] == PROTOCOL and frozen['protocol_sha256'] == digest(PROTOCOL), 'FROZEN_PROTOCOL')
    check(frozen['source_sha256'] == file_hash(SOURCE) == SOURCE_HASH, 'SOURCE_HASH')
    check(frozen['schema_version'] == SCHEMA and frozen['policy_hash'] == digest(POLICY), 'FROZEN_POLICY')
    # The selected trial's provenance also lists orchestration scripts developed
    # after that trial (freeze/verifier). Match the training inputs/code guarded
    # by m3_freeze itself; do not treat incidental provenance as executable input.
    for name in ('pipeline/m3_protocol.py','pipeline/m3_trial.py','pipeline/m3_prepare.py',
                 'pipeline/m2_runtime.py','pipeline/m2_source.py'):
        check(file_hash(ROOT/name) == frozen['executed_code_sha256'][name], 'FROZEN_EXECUTED_CODE_'+name)
    for name in ('pipeline/m3_ranking_cases.json','web/src/main/java/vn/edu/bigdata/m1/RuleRanking.java',
                 'pipeline/requirements.txt','web/pom.xml'):
        check(file_hash(ROOT/name) == frozen['integration_contract_sha256'][name], 'FROZEN_INTEGRATION_'+name)
    selected = ROOT/'artifacts/m3'/frozen['selected_run_id']
    check(file_hash(selected/'receipt.json') == frozen['selected_receipt_sha256'], 'FROZEN_RECEIPT')
    prep_path = ROOT/frozen['preparation']
    prep = verified_preparation(prep_path)
    check(file_hash(prep_path/'preparation.json') == frozen['preparation_sha256'], 'FROZEN_PREPARATION')
    require_ready(db, SOURCE_HASH)
    m2 = db.runs.find_one({'_id': M2_RUN})
    check(m2 and m2['stage'] == 'PREPROCESSING' and m2['status'] == 'VALIDATED'
          and m2['basket_set_status'] == 'READY' and m2['basket_set_id'] == BASKET_SET, 'M2_READY_STAGE')
    check(m2['manifest'] == json.loads((ROOT/f'artifacts/m2/pipeline-{M2_RUN}.json').read_text(encoding='utf-8')), 'M2_MANIFEST')
    lines = ROOT/m2['manifest']['output_directory']/'retained-lines.jsonl'
    check(file_hash(lines) == m2['manifest']['line_output']['sha256'], 'M2_RETAINED_HASH')
    verify_m3(db, frozen['selected_run_id'])  # metadata-only test, never items
    return frozen, prep_path, prep


def protected_snapshot(db):
    # No test basket items. Historical READY model outputs are small, separate from source rows.
    runs = list(db.runs.find({'status': 'READY'}).sort('_id', 1))
    return dict(runs={r['_id']: digest(r) for r in runs},
        outputs={r['_id']: {name: digest(list(db[name].find({'run_id': r['_id']}).sort('_id', 1)))
                 for name in COLLECTIONS} for r in runs},
        preprocessing=digest(db.runs.find_one({'_id': M2_RUN})),
        dataset=digest(db.datasets.find_one({'_id': SOURCE_HASH})),
        summaries=digest(list(db.summaries.find({'basket_set_id': BASKET_SET}).sort('_id', 1))))


def check_protected(db, before):
    after = protected_snapshot(db)
    for rid, expected in before['runs'].items():
        check(after['runs'].get(rid) == expected and after['outputs'].get(rid) == before['outputs'][rid], 'OLD_READY_CHANGED_'+rid)
    for name in ('preprocessing', 'dataset', 'summaries'):
        check(after[name] == before[name], 'OLD_INPUT_CHANGED_'+name)


def outputs_for(db, rid):
    return {name: list(db[name].find({'run_id': rid}).sort('_id', 1)) for name in COLLECTIONS}


def fail_unfinished(db, path, receipt, exc):
    """A late transport/stdout error must never rewrite a successfully READY run.

    Keep a separate incident first. If state cannot be read, leave it unresolved
    for readback; a failed call does not prove that the last state write failed.
    """
    incident=dict(run_id=receipt['run_id'],at_utc=now(),error_type=type(exc).__name__,error=str(exc))
    target=path/('failure-incident-'+str(uuid.uuid4())+'.json')
    save(target,incident)
    run=db.runs.find_one({'_id':receipt['run_id']})
    if run and run['status']=='READY':
        return
    failure=dict(receipt,status='FAIL',error_type=type(exc).__name__,error=str(exc),finished_at_utc=now())
    changed=db.runs.update_one({'_id':receipt['run_id'],'status':{'$in':['WRITING','VALIDATED']}},
        {'$set':{'status':'FAILED','manifest':bson_counts(failure)}})
    check(changed.matched_count==1,'FAILURE_STATE_UNRESOLVED_READBACK_REQUIRED')
    save(path/'receipt.json',failure)


def validate_outputs(db, rid, receipt):
    outputs = outputs_for(db, rid)
    catalog = outputs['items']
    known = {r['stock_code'] for r in catalog}
    n = receipt['counts']['train_baskets']
    check(n > 0 and n == receipt['split']['train']['baskets'], 'TRAIN_DENOMINATOR')
    check(len(known) == len(catalog) == receipt['counts']['train_items'], 'CATALOG_UNIQUE_COUNT')
    for name, rows in outputs.items():
        v = receipt['output_validation'][name]
        check(v['expected'] == v['actual'] == len(rows), 'OUTPUT_COUNT_'+name)
        check(len({r['_id'] for r in rows}) == len(rows), 'OUTPUT_UNIQUE_'+name)
        logical = [{k:v for k,v in r.items() if k not in ('_id', 'run_id')} for r in rows]
        check(v['checksum'] == logical_checksum(logical), 'OUTPUT_HASH_'+name)
        for r in rows:
            require_bson_longs(r)
            check(r['run_id'] == rid, 'OUTPUT_RUN')
            if name == 'items':
                check(r['_id'] == canonical([rid, r['stock_code']]) and isinstance(r['display_name'], str)
                      and r['display_name'].strip() and 0 < r['train_basket_count'] <= n, 'CATALOG_SCHEMA_KEY')
            elif name == 'frequent_itemsets':
                codes = r['items']
                check(codes and codes == sorted(set(codes)) and set(codes) <= known
                    and r['itemset_key'] == canonical(codes) and r['_id'] == canonical([rid,digest(codes)])
                    and r['train_basket_count'] == n and 0 < r['frequency'] <= n
                    and r['support'] == r['frequency']/n, 'ITEMSET_SCHEMA_KEY')
            else:
                validate_rule(r)
                check(set(r['antecedent']+[r['consequent']]) <= known
                    and r['rule_key'] == canonical([r['antecedent'],r['consequent']])
                    and r['_id'] == canonical([rid,digest([r['antecedent'],r['consequent']])]), 'RULE_SCHEMA_KEY')
    check(len(outputs['frequent_itemsets']) == receipt['counts']['itemsets']
          and len(outputs['association_rules']) == receipt['counts']['rules'], 'MODEL_COUNTS')
    return outputs


def verify_run(db, rid, allow_validated=False):
    path = OUT/rid
    receipt = json.loads((path/'receipt.json').read_text(encoding='utf-8'))
    run = db.runs.find_one({'_id': rid})
    stage = receipt['evaluation_stage']
    check(stage in ('DEVELOPMENT', 'FINAL'), 'EVALUATION_STAGE')
    check(run and run['status'] in (('READY','VALIDATED') if allow_validated else ('READY',))
        and run['stage'] == ('MODEL_FINAL' if stage == 'FINAL' else 'MODEL_DEVELOPMENT')
        and run['evaluation_stage'] == stage and run['mode'] == 'FULL_SOURCE'
        and run['schema_version'] == SCHEMA and run['dataset_id'] == SOURCE_HASH
        and run['basket_set_id'] == BASKET_SET and run['manifest'] == receipt
        and receipt['status'] == 'PASS', 'RUN_STAGE_MANIFEST')
    require_bson_longs(run)
    check(receipt['freeze_sha256'] == FREEZE_HASH and receipt['protocol'] == PROTOCOL
        and receipt['protocol_sha256'] == digest(PROTOCOL), 'RUN_FREEZE_PROTOCOL')
    frozen = json.loads((FREEZE/'freeze.json').read_text(encoding='utf-8'))
    check(receipt['config'] == frozen['config'] == run['config'], 'RUN_FROZEN_CONFIG')
    for name, expected in receipt['files_sha256'].items():
        check(file_hash(path/name) == expected, 'RUN_FILE_HASH_'+name)
    outputs = validate_outputs(db, rid, receipt)
    check(receipt['output_validation'] == frozen['output_validation'], 'FROZEN_MODEL_PARITY')
    queries = load_jsonl(ROOT/receipt['preparation']/'dev-queries.jsonl')
    predictions, development = evaluate(queries, outputs['association_rules'], outputs['items'], int(PROTOCOL['k']))
    check(predictions == load_jsonl(path/'dev-predictions.jsonl') and development == receipt['development'], 'DEV_REPLAY')
    if stage == 'FINAL':
        from m5_evaluate import verify_final
        verify_final(path, receipt, outputs)
        check(receipt['final_status'] == 'MEASURED', 'FINAL_STATUS')
    else:
        check(receipt['final_status'] == 'NOT_RUN', 'DEV_FINAL_STATUS')
    return dict(status='PASS', run_id=rid, evaluation_stage=stage, verified_at_utc=now(),
                output_validation=receipt['output_validation'], verifier_sha256=file_hash(Path(__file__)))
