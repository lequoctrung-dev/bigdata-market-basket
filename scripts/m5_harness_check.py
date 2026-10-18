"""Exhaustive FINAL harness check against all DEVELOPMENT queries before test."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'pipeline'))
from m2_source import ROOT, check, save
from m3_prepare import load_jsonl, file_hash, now
from m5_evaluate import independent_predictions, arithmetic
from m5_common import OUT


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run-id',required=True);a=p.parse_args()
    path=OUT/a.run_id
    receipt=json.loads((path/'receipt.json').read_text(encoding='utf-8'))
    check(receipt['evaluation_stage']=='DEVELOPMENT','DEV_ONLY_HARNESS')
    stored=load_jsonl(path/'dev-predictions.jsonl')
    queries=[{k:r[k] for k in ('invoice','invoice_time_local','query','target')} for r in stored]
    actual=independent_predictions(queries,load_jsonl(path/'association_rules.jsonl'),load_jsonl(path/'items.jsonl'),int(receipt['config']['k']))
    check(actual==stored,'ALL_DEV_EXHAUSTIVE_ORDER_BEST_RULE_BASELINE')
    save(OUT/('harness-dev-'+a.run_id+'.json'),dict(status='PASS',run_id=a.run_id,queries=len(actual),
        checked_at_utc=now(),test_access='NOT_OPENED',arithmetic=arithmetic(actual),
        evaluator_sha256=file_hash(ROOT/'pipeline/m5_evaluate.py')))
    print(json.dumps(dict(status='PASS',queries=len(actual),test_access='NOT_OPENED')))
