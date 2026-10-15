"""Join timestamped step boundaries with real RSS samples, preserving raw evidence."""
import argparse
from datetime import datetime, timedelta
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', required=True, type=Path)
    parser.add_argument('--measurement', required=True, type=Path)
    args = parser.parse_args()
    run = json.loads(args.receipt.read_text(encoding='utf-8'))
    measurement = json.loads(args.measurement.read_text(encoding='utf-8'))
    if run['status'] not in ('PASS', 'FAIL') or 'exit_code' not in measurement:
        raise RuntimeError('RUN_OR_MEASUREMENT_INCOMPLETE')
    origin = datetime.fromisoformat(measurement['sampling_started_at_utc'])
    samples = [json.loads(line) for line in args.measurement.with_suffix('.samples.jsonl').read_text(encoding='utf-8').splitlines()]
    output = {'run_id': run['run_id'], 'scope': 'M2_PREPROCESSING_TV1',
              'run_status': run['status'], 'exit_code': measurement['exit_code'],
              'memory_method': measurement['memory_method'], 'unit': 'bytes (MiB = bytes/1048576)',
              'groups': 'python includes batch Python and launcher/helper children other than java.exe; JVM and owned mongod separate',
              'measurement_sha256': hashlib.sha256(args.measurement.read_bytes()).hexdigest(),
              'peak_sampled_rss_bytes': measurement['peak_sampled_rss_bytes'],
              'wall_seconds': measurement['elapsed_seconds'], 'steps': {}}
    for name, step in run['step_measurements'].items():
        begin, end = (datetime.fromisoformat(step[k]) for k in ['started_at_utc','finished_at_utc'])
        selected = [s for s in samples if begin <= origin+timedelta(seconds=s['elapsed_seconds']) <= end]
        output['steps'][name] = {'seconds': run['steps_seconds'][name], 'sample_count': len(selected),
            'peak_sampled_rss_bytes': {group: max((s['rss_bytes'][group] for s in selected), default=None)
                                      for group in measurement['peak_sampled_rss_bytes']},
            'disk_end_logical_file_bytes': step['disk_end_bytes']}
    path = ROOT / 'artifacts/m2' / f'resources-{run["run_id"]}.json'
    path.write_text(json.dumps(output, indent=2), encoding='utf-8')
    print(json.dumps({'resource_summary': str(path), 'wall_seconds': output['wall_seconds']}))


if __name__ == '__main__':
    main()
