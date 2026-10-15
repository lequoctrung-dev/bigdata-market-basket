"""Run one M2 step; sample Python/JVM/Mongo RSS separately every second."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
import psutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/m2'


def disk_bytes():
    return {name: sum(p.stat().st_size for p in (ROOT / name).rglob('*') if p.is_file())
            for name in ['artifacts/m2', 'data/processed/m2', 'tmp/m2-spark']}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
    base = OUT / f'{args.label}-{stamp}'
    receipt = {'label': args.label, 'started_at_utc': datetime.now(timezone.utc).isoformat(),
               'command': args.command, 'platform': platform.platform(), 'python': sys.version,
               'packages': {n: importlib.metadata.version(n) for n in ['pyspark','pymongo','numpy','openpyxl','psutil']},
               'code_revision': subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip(),
               'working_tree_dirty': bool(subprocess.check_output(['git','status','--porcelain'], cwd=ROOT, text=True).strip()),
               'code_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                               for folder in ['pipeline','scripts'] for p in (ROOT / folder).glob('*') if p.is_file()},
               'disk_before_bytes': disk_bytes(), 'sample_interval_seconds': 1,
               'memory_method': 'Sampled RSS; sum per group at each sample. RSS includes shared pages; not private memory or exact high-water mark.'}
    mongo = None
    mongo_receipt = OUT / 'mongo-process.json'
    if mongo_receipt.exists():
        saved = json.loads(mongo_receipt.read_text(encoding='utf-8-sig'))
        try:
            candidate = psutil.Process(saved['process_id'])
            if candidate.exe().lower() == saved['executable'].lower() and saved['identity_path'] in ' '.join(candidate.cmdline()):
                mongo = candidate
        except psutil.NoSuchProcess:
            pass
    peak = {'python': 0, 'jvm': 0, 'mongo': 0, 'combined': 0}
    started = time.monotonic()
    receipt['sampling_started_at_utc'] = datetime.now(timezone.utc).isoformat()
    with base.with_suffix('.stdout.log').open('w', encoding='utf-8') as stdout, \
         base.with_suffix('.stderr.log').open('w', encoding='utf-8') as stderr, \
         base.with_suffix('.samples.jsonl').open('w', encoding='utf-8') as samples:
        process = subprocess.Popen(args.command, cwd=ROOT, stdout=stdout, stderr=stderr)
        parent = psutil.Process(process.pid)
        while True:
            groups = {'python': 0, 'jvm': 0, 'mongo': 0}
            try:
                children = [parent, *parent.children(recursive=True)]
            except psutil.NoSuchProcess:
                children = []
            for child in children + ([mongo] if mongo else []):
                try:
                    name = child.name().lower()
                    group = 'mongo' if child == mongo else 'jvm' if name == 'java.exe' else 'python'
                    groups[group] += child.memory_info().rss
                except psutil.NoSuchProcess:
                    pass
            groups['combined'] = sum(groups.values())
            for group in peak:
                peak[group] = max(peak[group], groups[group])
            samples.write(json.dumps({'elapsed_seconds': time.monotonic()-started, 'rss_bytes': groups,
                                      'available_ram_bytes': psutil.virtual_memory().available})+'\n')
            samples.flush()
            if process.poll() is not None:
                break
            time.sleep(1)
        receipt.update(exit_code=process.returncode, elapsed_seconds=time.monotonic()-started,
                       peak_sampled_rss_bytes=peak, disk_after_bytes=disk_bytes(),
                       finished_at_utc=datetime.now(timezone.utc).isoformat())
        base.with_suffix('.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
        print(json.dumps({'measurement': str(base.with_suffix('.json')), 'exit_code': process.returncode}), flush=True)
        sys.exit(process.returncode)


if __name__ == '__main__':
    main()
