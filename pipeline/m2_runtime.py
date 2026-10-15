"""M2 local writer lock and receipt identity; no kill/reset or configurable URI."""
from contextlib import contextmanager
from datetime import datetime
import hashlib
import json
import msvcrt
from pathlib import Path
import psutil
from bson.int64 import Int64

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/m2'
STORAGE_VERSION = 'm2-bson-counts-int64-v1'


def bson_counts(value):
    """Python small int otherwise becomes BSON int32; preserve boolean scalars."""
    if isinstance(value, dict):
        return {key: bson_counts(item) for key, item in value.items()}
    if isinstance(value, list):
        return [bson_counts(item) for item in value]
    if type(value) is int:
        return Int64(value)
    return value


def verify_owned_mongo():
    saved = json.loads((OUT / 'mongo-process.json').read_text(encoding='utf-8-sig'))
    if Path(saved['root']).resolve() != ROOT or saved['port'] != 27019 or saved['database'] != 'bigdata_m2':
        raise RuntimeError('M2_RECEIPT_DESTINATION')
    process = psutil.Process(saved['process_id'])
    expected_time = datetime.fromisoformat(saved['started_at_utc'].replace('Z', '+00:00')).timestamp()
    if abs(process.create_time()-expected_time) > 0.01 or process.exe().lower() != saved['executable'].lower():
        raise RuntimeError('M2_PROCESS_IDENTITY')
    if saved['identity_path'] not in process.cmdline() or '--port' not in process.cmdline() or '27019' not in process.cmdline():
        raise RuntimeError('M2_PROCESS_COMMAND')
    with open(saved['executable'], 'rb') as stream:
        if hashlib.file_digest(stream, 'sha256').hexdigest().upper() != saved['executable_sha256'].upper():
            raise RuntimeError('M2_BINARY_CHANGED')
    listeners = [c for c in process.net_connections(kind='tcp') if c.status == psutil.CONN_LISTEN]
    if not any(c.laddr.ip == '127.0.0.1' and c.laddr.port == 27019 for c in listeners):
        raise RuntimeError('M2_LISTENER_NOT_OWNED')


@contextmanager
def writer_lock():
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / 'writer.lock').open('a+b') as stream:
        stream.seek(0)
        if not stream.read(1):
            stream.write(b'0')
            stream.flush()
        stream.seek(0)
        msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        try:
            yield
        finally:
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)


def require_ready(db, dataset_id):
    metadata = db.datasets.find_one({'_id': dataset_id})
    if not metadata or metadata.get('status') != 'READY':
        raise RuntimeError('SOURCE_NOT_READY')
    for sheet in metadata['sheets']:
        if db.source_rows.count_documents({'dataset_id': dataset_id, 'sheet_index': sheet['sheet_index']}) != sheet['count']:
            raise RuntimeError('READY_SOURCE_SHEET_COUNT')
    if db.source_rows.count_documents({'dataset_id': dataset_id}) != metadata['expected_row_count']:
        raise RuntimeError('READY_SOURCE_TOTAL_COUNT')
    return metadata
