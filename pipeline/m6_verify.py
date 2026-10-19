"""M6 stage-aware read-only checker with explicit local session; no historical IDs."""
from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import psutil
from pymongo import MongoClient

from m2_source import ROOT, SOURCE_HASH, SCHEMA, POLICY, check, digest, save
from m2_runtime import verify_owned_mongo
from m3_prepare import file_hash, load_jsonl, now
from m3_protocol import PROTOCOL, evaluate, mask, split_name, logical_checksum
from m3_verify import require_bson_longs
from m5_common import validate_outputs
from m5_evaluate import verify_final, independent_predictions
from m6_common import DATABASE, URI, FREEZE_HASH, context, validated_inputs


def owned_web(session, allow_absent=False):
    saved = json.loads((session/'web-process.json').read_text(encoding='utf-8-sig'))
    check(Path(saved['root']).resolve() == ROOT and saved['port'] == 8081 and saved['database'] == DATABASE,
          'M6_WEB_RECEIPT_DESTINATION')
    try:
        proc = psutil.Process(saved['process_id'])
    except psutil.NoSuchProcess:
        check(allow_absent, 'M6_WEB_PROCESS_ABSENT')
        return None
    check(abs(proc.create_time()-datetime.fromisoformat(saved['started_at_utc'].replace('Z','+00:00')).timestamp()) < .01
          and proc.exe().lower() == saved['executable'].lower(), 'M6_WEB_PROCESS_IDENTITY')
    check(file_hash(Path(saved['executable'])).upper() == saved['executable_sha256'].upper()
          and file_hash(Path(saved['identity_path'])).upper() == saved['jar_sha256'].upper(), 'M6_WEB_BINARY_JAR')
    command = proc.cmdline()
    check(saved['identity_path'] in command and '--app.mode=DEVELOPMENT' in command
          and '--server.address=127.0.0.1' in command and '--server.port=8081' in command
          and any('127.0.0.1:27019/bigdata_m6?' in arg for arg in command), 'M6_WEB_COMMAND')
    sockets = [c for c in proc.net_connections(kind='tcp') if c.status == psutil.CONN_LISTEN]
    check(any(c.laddr.ip == '127.0.0.1' and c.laddr.port == 8081 for c in sockets), 'M6_WEB_LOOPBACK')
    return proc


def verify_run(db, rid, session, allow_validated=False):
    state, (frozen, selected, final_ref) = context(session)
    path = session/rid
    receipt = json.loads((path/'receipt.json').read_text(encoding='utf-8'))
    run = db.runs.find_one({'_id': rid})
    stage = receipt['evaluation_stage']
    check(stage in ('DEVELOPMENT','FINAL'), 'M6_MODEL_STAGE')
    check(run and run['status'] in (('READY','VALIDATED') if allow_validated else ('READY',))
          and run['stage'] == ('MODEL_FINAL' if stage == 'FINAL' else 'MODEL_DEVELOPMENT')
          and run['mode'] == 'FULL_SOURCE' and run['evaluation_stage'] == stage
          and run['dataset_id'] == SOURCE_HASH and run['schema_version'] == SCHEMA
          and receipt['dataset_id'] == SOURCE_HASH and receipt['schema_version'] == SCHEMA
          and run['policy_version'] == POLICY['version'] and receipt['policy'] == POLICY
          and run['manifest'] == receipt and receipt['status'] == 'PASS'
          and receipt['milestone'] == 'M6' and receipt['machine_id'] == state['machine_id']
          and receipt['database'] == DATABASE, 'M6_READY_MANIFEST')
    require_bson_longs(run)
    check(receipt['protocol'] == PROTOCOL and receipt['protocol_sha256'] == digest(PROTOCOL)
          and receipt['freeze_sha256'] == FREEZE_HASH and receipt['config'] == frozen['config'] == run['config']
          and run['ranking_version'] == PROTOCOL['ranking_version']
          and run['policy_hash'] == receipt['policy_hash'] == digest(POLICY)
          and receipt['machine_role'] == state['machine_role']
          and receipt['final_status'] == ('MEASURED' if stage == 'FINAL' else 'NOT_RUN'),
          'M6_FROZEN_RUN')
    _, prep_path, prep = validated_inputs(db, session, ROOT/receipt['preparation'])
    check(receipt['preprocessing_run_id'] == prep['preprocessing_run_id']
          and run['basket_set_id'] == receipt['basket_set_id'] == prep['basket_set_id']
          and file_hash(prep_path/'preparation.json') == receipt['preparation_sha256'], 'M6_RUN_LOCAL_LINEAGE')
    pre = db.runs.find_one({'_id': receipt['preprocessing_run_id']})
    check(receipt['stage_counts'] == pre['manifest']['counts'], 'M6_STAGE_COUNTS')
    for name, expected in receipt['files_sha256'].items():
        check(Path(name).name == name and file_hash(path/name) == expected, 'M6_OUTPUT_FILE_'+name)
    outputs = validate_outputs(db, rid, receipt)
    check(receipt['output_validation'] == frozen['output_validation'], 'M6_EXACT_MODEL_REPLICATION')
    for name, rows in outputs.items():
        check(rows == sorted(load_jsonl(path/f'{name}.jsonl'), key=lambda r:r['_id']), 'M6_FILE_DB_'+name)
    train = load_jsonl(prep_path/'train-baskets.jsonl')
    check(Counter(c for b in train for c in b['items']) ==
          {r['stock_code']:r['train_basket_count'] for r in outputs['items']}, 'M6_TRAIN_FREQUENCIES')
    queries = load_jsonl(prep_path/'dev-queries.jsonl')
    predictions, development = evaluate(queries, outputs['association_rules'], outputs['items'], int(PROTOCOL['k']))
    check(predictions == load_jsonl(path/'dev-predictions.jsonl') and development == receipt['development']
          == selected['development'], 'M6_ALL_DEVELOPMENT_REPLAY')
    check(predictions == independent_predictions(queries, outputs['association_rules'], outputs['items'], int(PROTOCOL['k'])),
          'M6_EXHAUSTIVE_DEVELOPMENT')
    if stage == 'FINAL':
        check(receipt['model_source_run_id'] != rid, 'M6_FINAL_MODEL_SOURCE')
        source = db.runs.find_one({'_id': receipt['model_source_run_id']})
        check(source and source['status'] == 'READY' and source['evaluation_stage'] == 'DEVELOPMENT'
              and source['manifest']['machine_id'] == state['machine_id']
              and source['manifest']['output_validation'] == receipt['output_validation'], 'M6_FINAL_LOCAL_MODEL')
        check(json.loads((path/'test-access.json').read_text(encoding='utf-8')) == receipt['test_access']
              and receipt['test_access']['event'] == 'M6_REPLICATION_TEST_ITEMS_READ_ATTEMPT', 'M6_REPLICATION_LEDGER')
        metadata = [{k:b[k] for k in ('invoice','invoice_time_local')}
                    for b in load_jsonl(prep_path/'split-metadata.jsonl') if b['split']=='test']
        baskets = load_jsonl(path/'test-baskets.jsonl')
        check([{k:b[k] for k in ('invoice','invoice_time_local')} for b in baskets] == metadata,
              'M6_TEST_SPLIT_MEMBERSHIP')
        check(all(split_name(b['invoice_time_local']) == 'test' for b in baskets), 'M6_TEST_BOUNDARIES')
        verify_final(path, receipt, outputs)
        check(receipt['final'] == final_ref['final'] and receipt['final_new_items'] == final_ref['final_new_items'],
              'M6_EXACT_FINAL_METRICS')
        for name in ('test-baskets.jsonl','test-queries.jsonl','test-predictions.jsonl'):
            check(file_hash(path/name) == final_ref['files_sha256'][name], 'M6_EXACT_FINAL_PAYLOAD_'+name)
    else:
        check(receipt['final_status'] == 'NOT_RUN', 'M6_DEVELOPMENT_FINAL_STATUS')
    return dict(status='PASS', milestone='M6', run_id=rid, evaluation_stage=stage,
        machine_id=state['machine_id'], verified_at_utc=now(), output_validation=receipt['output_validation'],
        verifier_sha256=file_hash(Path(__file__)), checks=['explicit local preprocessing/preparation lineage',
        'source/freeze/config/split/catalog/model exact parity','files and BSON Int64/keys/cross-references',
        'all dev predictions/exhaustive ranking/metrics', 'final replication replay when stage FINAL'])


if __name__ == '__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--session',required=True,type=Path);p.add_argument('--run-id',required=True)
    a=p.parse_args();session=a.session.resolve()
    verify_owned_mongo()
    with MongoClient(URI) as client:
        report=verify_run(client[DATABASE],a.run_id,session)
    target=session/a.run_id/('verification-'+now().replace(':','')+'.json')
    save(target,report);print(json.dumps(dict(status='PASS',receipt=str(target.relative_to(ROOT)))))
