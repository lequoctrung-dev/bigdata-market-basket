"""Attach sampled group RSS to actual M5 step times; preserve failure receipts."""
import argparse
from datetime import datetime, timedelta
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', required=True, type=Path)
    parser.add_argument('--measurement', required=True, type=Path)
    args = parser.parse_args()
    run = json.loads(args.receipt.read_text(encoding='utf-8'))
    measured = json.loads(args.measurement.read_text(encoding='utf-8'))
    if run['status'] not in ('PASS','FAIL') or 'exit_code' not in measured:
        raise RuntimeError('INCOMPLETE_MEASUREMENT')
    origin = datetime.fromisoformat(measured['sampling_started_at_utc'])
    begin = datetime.fromisoformat(run['started_at_utc'])
    samples = [json.loads(line) for line in args.measurement.with_suffix('.samples.jsonl').read_text(encoding='utf-8').splitlines()]
    steps = []
    for step in run['steps']:
        end = datetime.fromisoformat(step['end_at_utc'])
        values = [s for s in samples if begin <= origin+timedelta(seconds=s['elapsed_seconds']) < end]
        steps.append(dict(name=step['name'], seconds=step['seconds'], sample_count=len(values),
            peak_sampled_rss_bytes={g: max((s['rss_bytes'][g] for s in values), default=None)
                                    for g in measured['peak_sampled_rss_bytes']}))
        begin = end
    report = dict(run_id=run['run_id'], scope='M5_STAGE_MEASURED_TV1', run_status=run['status'],
        exit_code=measured['exit_code'], memory_method=measured['memory_method'],
        unit='bytes (MiB = bytes/1048576)', wall_seconds=measured['elapsed_seconds'],
        peak_sampled_rss_bytes=measured['peak_sampled_rss_bytes'], steps=steps,
        disk_before_bytes=measured['disk_before_bytes'], disk_after_bytes=measured['disk_after_bytes'],
        disk_limit='Logical file byte snapshots; not allocated bytes or peak scratch; Spark may remove its scratch on stop.',
        measurement_sha256=hashlib.sha256(args.measurement.read_bytes()).hexdigest(),
        receipt_sha256=hashlib.sha256(args.receipt.read_bytes()).hexdigest())
    target = args.receipt.parent/'resources-m5.json'
    if target.exists():
        raise RuntimeError('RESOURCE_SUMMARY_ALREADY_EXISTS')
    target.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({'resources':str(target),'wall_seconds':report['wall_seconds']}))


if __name__ == '__main__':
    main()
