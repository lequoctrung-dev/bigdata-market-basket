"""Measure only the launched batch tree and verified owned Mongo/web, every second."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
import uuid
import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'pipeline'))
from m2_source import save
from m2_runtime import verify_owned_mongo
from m3_prepare import now, file_hash, provenance
from m6_common import context


def disk_bytes(session):
    folders = [session, ROOT/'tmp/m6-spark', ROOT/'artifacts/m2/mongo-data']
    return {str(folder.relative_to(ROOT)): sum(p.stat().st_size for p in folder.rglob('*') if p.is_file())
            for folder in folders}


def main(args):
    session = args.session.resolve()
    state, _ = context(session)
    verify_owned_mongo()
    saved = json.loads((ROOT/'artifacts/m2/mongo-process.json').read_text(encoding='utf-8-sig'))
    mongo = psutil.Process(saved['process_id'])
    base = session/(args.label+'-'+str(uuid.uuid4()))
    report = dict(status='RUNNING', started_at_utc=now(), machine_role=state['machine_role'],
        machine_id=state['machine_id'], command=args.command, sample_interval_seconds=1,
        memory_method='Sampled RSS bytes, includes shared pages; not private memory or exact peak. Combined is computed at each sample.',
        disk_method='Logical file bytes before/after; not allocated bytes or peak scratch.',
        disk_before_bytes=disk_bytes(session), script_sha256=file_hash(Path(__file__)))
    report['provenance'] = provenance()
    code_folder = session/'executed-code'
    code_folder.mkdir(exist_ok=True)
    for name, expected in report['provenance']['code_sha256'].items():
        source = ROOT/name
        check_name = expected+'-'+name.replace('/','__')
        destination = code_folder/check_name
        if not destination.exists(): destination.write_bytes(source.read_bytes())
        if file_hash(destination) != expected: raise RuntimeError('M6_EXECUTED_CODE_SNAPSHOT')
    save(base.with_suffix('.json'), report)
    start = time.monotonic()
    peak = dict(python=0, jvm=0, mongo=0, web=0, combined=0)
    seen_jvms, gaps = {}, []
    with base.with_suffix('.stdout.log').open('x', encoding='utf-8') as stdout, \
         base.with_suffix('.stderr.log').open('x', encoding='utf-8') as stderr, \
         base.with_suffix('.samples.jsonl').open('x', encoding='utf-8') as samples:
        child = subprocess.Popen(args.command, cwd=ROOT, stdout=stdout, stderr=stderr)
        parent = psutil.Process(child.pid)
        while True:
            groups = dict(python=0, jvm=0, mongo=0, web=0)
            try:
                children = [parent, *parent.children(recursive=True)]
            except psutil.NoSuchProcess:
                children = []
            for proc in children + [mongo]:
                try:
                    name = proc.name().lower()
                    group = 'mongo' if proc.pid == mongo.pid else 'jvm' if name == 'java.exe' else 'python'
                    groups[group] += proc.memory_info().rss
                    if group == 'jvm': seen_jvms[proc.pid] = proc.create_time()
                except psutil.NoSuchProcess:
                    pass
                except psutil.AccessDenied:
                    gaps.append(dict(at_utc=now(), pid=proc.pid, reason='ACCESS_DENIED'))
            web_receipt = session/'web-process.json'
            if web_receipt.exists():
                from m6_verify import owned_web
                web = owned_web(session, allow_absent=True)
                if web: groups['web'] = web.memory_info().rss
            groups['combined'] = sum(groups.values())
            for key, value in groups.items(): peak[key] = max(peak[key], value)
            samples.write(json.dumps(dict(at_utc=now(), elapsed_seconds=time.monotonic()-start,
                rss_bytes=groups, available_ram_bytes=psutil.virtual_memory().available,
                free_disk_bytes=psutil.disk_usage(str(ROOT)).free))+'\n')
            samples.flush()
            if child.poll() is not None: break
            time.sleep(1)
        # A terminated Python child can leave its Java gateway after Spark.stop.
        # Only descendants actually sampled during this launched batch are eligible.
        cleanup = []
        for pid, created in seen_jvms.items():
            try:
                proc = psutil.Process(pid)
                if proc.create_time() == created and 'org.apache.spark.deploy.SparkSubmit' in ' '.join(proc.cmdline()):
                    proc.wait(timeout=3)
            except psutil.TimeoutExpired:
                proc.terminate(); proc.wait(timeout=15)
                cleanup.append(dict(pid=pid, create_time=created, reason='owned batch gateway after Python exit'))
            except psutil.NoSuchProcess:
                pass
        report.update(status='PASS' if child.returncode == 0 else 'FAIL', exit_code=child.returncode,
            elapsed_seconds=time.monotonic()-start, peak_sampled_rss_bytes=peak, sampling_gaps=gaps,
            owned_gateway_cleanup=cleanup, disk_after_bytes=disk_bytes(session), finished_at_utc=now())
        save(base.with_suffix('.json'), report)
        print(json.dumps(dict(measurement=str(base.with_suffix('.json').relative_to(ROOT)),
                              exit_code=child.returncode)), flush=True)
        return child.returncode


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--session', required=True, type=Path)
    p.add_argument('--label', required=True)
    p.add_argument('command', nargs=argparse.REMAINDER)
    a=p.parse_args()
    if not a.command or not a.label.replace('-','').isalnum(): p.error('command and simple label required')
    sys.exit(main(a))
