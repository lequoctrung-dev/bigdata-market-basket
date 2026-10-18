"""Record current identity, frozen inputs and protected READY data without opening test items."""
import json
from pathlib import Path
import subprocess
import sys
import psutil
from pymongo import MongoClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'pipeline'))
from m2_source import ROOT, URI, DATABASE, save
from m2_runtime import verify_owned_mongo, writer_lock
from m3_prepare import file_hash, now
from m5_common import OUT, frozen_inputs, protected_snapshot


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT/('preflight-'+now().replace(':','')+'.json')
    report = dict(status='RUNNING', started_at_utc=now(), test_access='NOT_OPENED_BY_THIS_COMMAND')
    try:
        verify_owned_mongo()
        with writer_lock(), MongoClient(URI) as client:
            db = client[DATABASE]
            frozen, prep_path, prep = frozen_inputs(db)
            report.update(protected=protected_snapshot(db), pointer=db.publication.find_one({'_id':'active'}),
                freeze_sha256=file_hash(ROOT/'artifacts/m3/freeze-1a1f2ec6-331e-4b02-9aaf-18804793d4e9/freeze.json'),
                preparation=str(prep_path.relative_to(ROOT)), split=prep['split'], config=frozen['config'],
                available_ram_bytes=psutil.virtual_memory().available, free_disk_bytes=psutil.disk_usage(str(ROOT)).free,
                mongo_process=json.loads((ROOT/'artifacts/m2/mongo-process.json').read_text(encoding='utf-8-sig')),
                git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                protected_files={name:file_hash(ROOT/name) for name in subprocess.check_output(
                    ['git','ls-files'],cwd=ROOT,text=True,encoding='utf-8').splitlines()
                    if name.startswith(('pipeline/','scripts/','requirements-review/evidence/'))
                    or name.endswith('.docx') or name.startswith(('requirements-review/01_','requirements-review/15_'))},
                status='PASS')
    except Exception as exc:
        report.update(status='FAIL', error_type=type(exc).__name__, error=str(exc))
        raise
    finally:
        report['finished_at_utc'] = now()
        save(path, report)
        print(json.dumps({'status':report['status'],'receipt':str(path.relative_to(ROOT))}))


if __name__ == '__main__':
    main()
