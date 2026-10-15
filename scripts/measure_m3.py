"""M3 measurement wrapper. Reuses M2 sampler with explicit M3 output/disk scope."""
import json
from pathlib import Path
import sys

import measure_m2

ROOT = Path(__file__).resolve().parents[1]


def disk_bytes():
    return {name: sum(p.stat().st_size for p in (ROOT/name).rglob('*') if p.is_file())
            for name in ('artifacts/m3','tmp/m3-spark','artifacts/m2/mongo-data')}


if __name__ == '__main__':
    # M2 sampler finds the Mongo process receipt relative to OUT. For M3 keep a
    # measurement-only snapshot, without changing the lifecycle owner's receipt.
    measure_m2.OUT = ROOT/'artifacts/m3'
    measure_m2.OUT.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(ROOT/'pipeline'))
    from m2_runtime import verify_owned_mongo
    verify_owned_mongo()
    source = ROOT/'artifacts/m2/mongo-process.json'
    saved = json.loads(source.read_text(encoding='utf-8-sig'))
    (measure_m2.OUT/'mongo-process.json').write_text(json.dumps(saved, indent=2), encoding='utf-8')
    measure_m2.disk_bytes = disk_bytes
    measure_m2.main()
