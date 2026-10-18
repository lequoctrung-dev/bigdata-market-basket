"""M5 sampler: same measured RSS method as M2, separate evidence and disk scope."""
import json
from pathlib import Path
import sys
import measure_m2

ROOT = Path(__file__).resolve().parents[1]


def disk_bytes():
    return {name:sum(p.stat().st_size for p in (ROOT/name).rglob('*') if p.is_file())
        for name in ('artifacts/m5','tmp/m5-spark','artifacts/m2/mongo-data')}


if __name__ == '__main__':
    sys.path.insert(0,str(ROOT/'pipeline'))
    from m2_runtime import verify_owned_mongo
    verify_owned_mongo()
    measure_m2.OUT = ROOT/'artifacts/m5'
    measure_m2.OUT.mkdir(parents=True,exist_ok=True)
    saved = json.loads((ROOT/'artifacts/m2/mongo-process.json').read_text(encoding='utf-8-sig'))
    (measure_m2.OUT/'mongo-process.json').write_text(json.dumps(saved,indent=2),encoding='utf-8')
    measure_m2.disk_bytes = disk_bytes
    measure_m2.main()
