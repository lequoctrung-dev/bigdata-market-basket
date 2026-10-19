"""M6 context and guards. Historical M2/M3/M5 modules and READY data stay unchanged."""
from datetime import datetime
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import subprocess
import sys
import uuid
import winreg

import psutil
from bson import BSON
from pymongo import MongoClient

from m2_source import ROOT, SOURCE, SOURCE_HASH, SCHEMA, POLICY, URI, check, digest, save
from m2_runtime import verify_owned_mongo, writer_lock, bson_counts
from m3_prepare import file_hash, now, load_jsonl, jsonl, provenance
from m3_protocol import PROTOCOL

DATABASE = 'bigdata_m6'
FREEZE_HASH = 'f7ee9c13432f0c99e7e5bcbf0363eed77eb4d5493b39e78fbb2e8e48557d053a'
FINAL_HASH = 'e2552b5aca7fc45c2c86a32f53700ed474bb0c2e670ed0424f9fa332c1da7efe'
MODEL_COLLECTIONS = ('items', 'frequent_itemsets', 'association_rules')


def machine_identity():
    # Keep only an opaque stable identifier; never log the underlying Windows ID.
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Cryptography',
                        0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY) as key:
        value = winreg.QueryValueEx(key, 'MachineGuid')[0]
    return hashlib.sha256(('bigdata-m6-machine-v1:' + value).encode()).hexdigest()


def reference(path):
    path = Path(path).resolve()
    check(file_hash(path/'freeze.json') == FREEZE_HASH, 'M6_REFERENCE_FREEZE_HASH')
    frozen = json.loads((path/'freeze.json').read_text(encoding='utf-8'))
    hashes = json.loads((path/'hashes.json').read_text())
    check(hashes == {'freeze.json': FREEZE_HASH,
                    'verification.json': '153263e3ceaddb50ceebc893942984b21ce70130cbea683ad633acfdbf601de6'},
          'M6_FREEZE_VERIFICATION_HASHES')
    for name, expected in hashes.items():
        check(name in ('freeze.json', 'verification.json') and file_hash(path/name) == expected,
              'M6_REFERENCE_HASH_' + name)
    check(file_hash(path/'selected-receipt.json') == frozen['selected_receipt_sha256'], 'M6_SELECTED_REFERENCE_HASH')
    check(file_hash(path/'final-receipt.json') == FINAL_HASH, 'M6_FINAL_REFERENCE_HASH')
    selected = json.loads((path/'selected-receipt.json').read_text(encoding='utf-8'))
    final = json.loads((path/'final-receipt.json').read_text(encoding='utf-8'))
    check(frozen['protocol'] == PROTOCOL and frozen['protocol_sha256'] == digest(PROTOCOL)
          and frozen['source_sha256'] == SOURCE_HASH and frozen['schema_version'] == SCHEMA
          and frozen['policy'] == POLICY and frozen['policy_hash'] == digest(POLICY), 'M6_FROZEN_SEMANTICS')
    check(selected['config'] == frozen['config'] == final['config']
          and selected['output_validation'] == frozen['output_validation'] == final['output_validation'],
          'M6_REFERENCE_CONFIG_MODEL')
    for name in ('pipeline/m3_protocol.py', 'pipeline/m3_trial.py', 'pipeline/m3_prepare.py',
                 'pipeline/m2_runtime.py', 'pipeline/m2_source.py'):
        check(file_hash(ROOT/name) == frozen['executed_code_sha256'][name], 'M6_FROZEN_CODE_' + name)
    for name in ('pipeline/m3_ranking_cases.json', 'web/src/main/java/vn/edu/bigdata/m1/RuleRanking.java',
                 'pipeline/requirements.txt', 'web/pom.xml'):
        check(file_hash(ROOT/name) == frozen['integration_contract_sha256'][name], 'M6_FROZEN_CONTRACT_' + name)
    check({p.name: file_hash(p) for p in (ROOT/'tmp/connector').glob('*.jar')} == selected['jars_sha256'],
          'M6_LOCAL_JARS_HASH')
    for requirement in (ROOT/'pipeline/requirements.txt').read_text().splitlines():
        if not requirement.strip(): continue
        package, version = requirement.split('==')
        check(importlib.metadata.version(package.split('[')[0]) == version, 'M6_PACKAGE_VERSION_'+package)
    return frozen, selected, final


def context(session):
    session = Path(session).resolve()
    check(session.is_relative_to(ROOT/'artifacts/m6'), 'M6_SESSION_OUTSIDE_WORKSPACE')
    state = json.loads((session/'session.json').read_text(encoding='utf-8'))
    check(state['database'] == DATABASE and state['machine_id'] == machine_identity(), 'M6_SESSION_MACHINE_DB')
    check(state['session_id'] == session.name and state['machine_role'] == session.parent.name
          and state['machine_role'] in ('TV1', 'TV2'), 'M6_SESSION_ROLE_ID')
    ref_path = ROOT/state['reference']
    for name, expected in state['reference_hashes'].items():
        check(file_hash(ref_path/name) == expected, 'M6_SESSION_REFERENCE_CHANGED')
    return state, reference(ref_path)


def namespace_hashes(db):
    """Read every existing document, preserving BSON types; log only hashes/counts."""
    result = {}
    for name in sorted(db.list_collection_names()):
        value, count = hashlib.sha256(), 0
        for row in db[name].find().sort('_id', 1):
            value.update(BSON.encode(row)); count += 1
        result[name] = dict(count=count, bson_sha256=value.hexdigest())
    return result


def ready_snapshot(db):
    runs = list(db.runs.find({'status': 'READY'}).sort('_id', 1))
    return dict(pointer=db.publication.find_one({'_id': 'active'}),
        runs={r['_id']: digest(r) for r in runs},
        outputs={r['_id']: {name: digest(list(db[name].find({'run_id': r['_id']}).sort('_id', 1)))
                            for name in MODEL_COLLECTIONS} for r in runs})


def check_ready_snapshot(db, before):
    after = ready_snapshot(db)
    check(after['pointer'] == before['pointer'], 'M6_UNEXPECTED_PUBLICATION_MUTATION')
    for rid, checksum in before['runs'].items():
        check(after['runs'].get(rid) == checksum and after['outputs'].get(rid) == before['outputs'][rid],
              'M6_OLD_READY_CHANGED_' + rid)


def new_session(role, ref_path):
    verify_owned_mongo()
    frozen, selected, final = reference(ref_path)
    check(file_hash(SOURCE) == SOURCE_HASH, 'M6_SOURCE_HASH')
    path = ROOT/'artifacts/m6'/role/str(uuid.uuid4())
    path.mkdir(parents=True, exist_ok=False)
    state = dict(milestone='M6', mode='FULL_RUN', status='IN_PROGRESS', session_id=path.name,
        machine_role=role, machine_id=machine_identity(), database=DATABASE, started_at_utc=now(),
        operator='AGENT_ASSISTED_TECHNICAL_EXECUTION', human_demo='PENDING_USER',
        tv2_runtime='ASSUMED_EQUIVALENT_BY_USER_NOT_MEASURED',
        reference=str(Path(ref_path).resolve().relative_to(ROOT)),
        reference_hashes={p.name: file_hash(p) for p in Path(ref_path).glob('*.json')},
        source_sha256=SOURCE_HASH, freeze_sha256=FREEZE_HASH, protocol_sha256=digest(PROTOCOL),
        config=frozen['config'], versions=dict(python=sys.version, platform=platform.platform(),
            packages={n: importlib.metadata.version(n) for n in ('pyspark','pymongo','numpy','openpyxl','psutil')}),
        available_ram_bytes=psutil.virtual_memory().available, free_disk_bytes=psutil.disk_usage(str(ROOT)).free,
        **provenance())
    save(path/'session.json', state)
    with writer_lock(), MongoClient(URI) as client:
        save(path/'protected-m2-before.json', namespace_hashes(client['bigdata_m2']))
        save(path/'m6-ready-before.json', ready_snapshot(client[DATABASE]))
    print(json.dumps(dict(session=str(path.relative_to(ROOT)), status='IN_PROGRESS')), flush=True)
    return path


def postcheck_preprocessing(db, receipt):
    from m3_verify import require_bson_longs
    require_bson_longs(db.runs.find_one({'_id': receipt['run_id']}))
    basket = receipt['basket_set_id']
    check(db.baskets.count_documents({'basket_set_id': basket, 'retained_line_count': {'$type': 'long'}})
          == receipt['counts']['baskets'], 'M6_PRE_BSON_BASKETS')
    for kind, fields, expected in [('item', ['rows','quantity','baskets'], receipt['counts']['items']),
        ('month', ['invoices','lines'], len(receipt['monthly'])),
        ('basket_size', ['baskets'], len(receipt['size_distribution']))]:
        check(db.summaries.count_documents({'basket_set_id': basket, 'summary_type': kind,
              **{f'payload.{field}': {'$type': 'long'} for field in fields}}) == expected,
              'M6_PRE_BSON_SUMMARY_' + kind)
    lines = ROOT/receipt['output_directory']/'retained-lines.jsonl'
    check(file_hash(lines) == receipt['line_output']['sha256'], 'M6_PRE_LINES_HASH')
    check(sum(1 for _ in lines.open('rb')) == receipt['counts']['retained'], 'M6_PRE_LINES_COUNT')


def validated_inputs(db, session, preparation):
    from m2_runtime import require_ready, STORAGE_VERSION
    from m2_source import PARSER
    from m3_prepare import verified_preparation
    state, (frozen, selected, final) = context(session)
    preparation = Path(preparation).resolve()
    check(preparation.is_relative_to(session), 'M6_PREPARATION_FROM_OTHER_SESSION')
    prep = verified_preparation(preparation)
    check(prep['milestone'] == 'M6' and prep['database'] == DATABASE
          and prep['machine_id'] == state['machine_id'] and prep['machine_role'] == state['machine_role'],
          'M6_PREPARATION_ORIGIN')
    pre = db.runs.find_one({'_id': prep['preprocessing_run_id']})
    check(pre and pre['stage'] == 'PREPROCESSING' and pre['status'] == 'VALIDATED'
          and pre['basket_set_status'] == 'READY', 'M6_PREPROCESSING_READY')
    receipt = json.loads((session/f"pipeline-{pre['_id']}.json").read_text(encoding='utf-8'))
    check(pre['manifest'] == receipt and receipt['milestone'] == 'M6' and receipt['status'] == 'PASS'
          and receipt['schema_version'] == SCHEMA and receipt['parser_version'] == PARSER
          and receipt['policy'] == POLICY and receipt['storage_encoding_version'] == STORAGE_VERSION
          and receipt['machine_id'] == state['machine_id'] and receipt['machine_role'] == state['machine_role'],
          'M6_PREPROCESSING_MANIFEST')
    require_ready(db, SOURCE_HASH)
    postcheck_preprocessing(db, receipt)
    check(prep['basket_set_id'] == pre['basket_set_id'] == frozen['basket_set_id'], 'M6_BASKET_SET_SEMANTICS')
    check(prep['split'] == frozen['split'] and prep['invoice_overlap'] == 0, 'M6_FROZEN_SPLIT')
    for name in ('train-baskets.jsonl','dev-baskets.jsonl','dev-queries.jsonl','catalog.jsonl','split-metadata.jsonl'):
        check(file_hash(preparation/name) == frozen['train_input_files_sha256'][name], 'M6_RECREATED_INPUT_' + name)
    # Exact current DB inputs must equal the newly generated local input files.
    for part, low, high in [('train',PROTOCOL['train_start'],PROTOCOL['dev_start']),
                            ('dev',PROTOCOL['dev_start'],PROTOCOL['test_start'])]:
        current = list(db.baskets.find({'basket_set_id': prep['basket_set_id'],
            'invoice_time_local': {'$gte':low, '$lt':high}}, {'_id':0}).sort('invoice',1))
        check(current == load_jsonl(preparation/f'{part}-baskets.jsonl'), 'M6_CURRENT_INPUT_'+part)
    return frozen, preparation, prep


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--machine-role', required=True, choices=['TV1','TV2'])
    parser.add_argument('--reference', required=True, type=Path)
    args = parser.parse_args()
    new_session(args.machine_role, args.reference.resolve())
