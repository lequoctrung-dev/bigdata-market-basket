"""Select only completed DEVELOPMENT trials; freeze a new artifact, never final eval."""
import argparse
import json
from pathlib import Path
import uuid

from pymongo import MongoClient
from m2_source import ROOT, URI, DATABASE, POLICY, SCHEMA, canonical, check, digest, save
from m2_runtime import verify_owned_mongo, writer_lock
from m3_prepare import OUT, file_hash, now, provenance, verified_preparation
from m3_protocol import PROTOCOL, TRIALS, selection_key
from m3_verify import verify_run


def freeze(preparation):
    prep = verified_preparation(preparation)
    trials = []
    for path in OUT.glob('*/receipt.json'):
        receipt = json.loads(path.read_text(encoding='utf-8'))
        if receipt['preparation_sha256'] == file_hash(preparation/'preparation.json'):
            trials.append((path, receipt))
    check({r['trial_index'] for _,r in trials} == set(range(len(TRIALS))), 'PLANNED_TRIALS_NOT_ALL_ATTEMPTED')
    completed = [r for _,r in trials if r['status'] == 'PASS']
    check(completed, 'NO_SUCCESSFUL_TRIALS')
    selected = min(completed, key=selection_key)
    # Freeze the actual executed implementation; new code requires another trial.
    for filename in ('pipeline/m3_protocol.py','pipeline/m3_trial.py','pipeline/m3_prepare.py',
                     'pipeline/m2_runtime.py','pipeline/m2_source.py'):
        check(file_hash(ROOT/filename) == selected['code_sha256'][filename], 'EXECUTED_CODE_CHANGED_'+filename)
    verify_owned_mongo()
    with writer_lock(), MongoClient(URI) as client:
        verification = verify_run(client[DATABASE], selected['run_id'])
        path = OUT/('freeze-'+str(uuid.uuid4()))
        path.mkdir(parents=True, exist_ok=False)
        artifact = dict(version='m3-development-freeze-v1', frozen_at_utc=now(),
            evaluation_stage='DEVELOPMENT', final_status='NOT_RUN', selected_run_id=selected['run_id'],
            selected_trial_index=selected['trial_index'], config=selected['config'], protocol=PROTOCOL,
            protocol_sha256=digest(PROTOCOL), source_sha256=selected['dataset_id'], basket_set_id=selected['basket_set_id'],
            schema_version=SCHEMA, policy=POLICY, policy_hash=digest(POLICY),
            split=prep['split'], preparation_sha256=file_hash(preparation/'preparation.json'),
            preparation=str(preparation.relative_to(ROOT)), train_input_files_sha256=prep['files_sha256'],
            selected_receipt_sha256=file_hash(OUT/selected['run_id']/'receipt.json'),
            output_validation=selected['output_validation'], executed_code_sha256=selected['code_sha256'],
            integration_contract_sha256={name:file_hash(ROOT/name) for name in (
                'pipeline/m3_ranking_cases.json',
                'web/src/main/java/vn/edu/bigdata/m1/RuleRanking.java',
                'web/src/test/java/vn/edu/bigdata/m1/M3SharedRankingTest.java',
                'pipeline/requirements.txt','web/pom.xml',
                'requirements-review/11_SPECIFICATION_DRAFT.md','requirements-review/12_TECHNICAL_DESIGN.md')},
            selection_rule='max dev Recall@5, then recommendation rate, fewer rules, higher support, run_id',
            trials=[dict(run_id=r['run_id'], trial_index=r['trial_index'], status=r['status'],
                         error=r.get('error'), config=r['config'], development=r.get('development'),
                         receipt_sha256=file_hash(p)) for p,r in sorted(trials, key=lambda pair: pair[1]['started_at_utc'])],
            publication='NOT_ATTEMPTED; READY run selected explicitly, no newest-run lookup',
            human_review='PENDING_TV2', **provenance())
        save(path/'verification.json', verification)
        save(path/'freeze.json', artifact)
        save(path/'hashes.json', {p.name:file_hash(p) for p in sorted(path.glob('*.json'))})
        print(canonical({'freeze':str(path.relative_to(ROOT)), 'selected_run_id':selected['run_id'], 'status':'PASS'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--preparation', required=True, type=Path)
    freeze(parser.parse_args().preparation.resolve())
