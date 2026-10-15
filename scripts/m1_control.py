"""Receipt đọc web M1 và shutdown MongoDB riêng đã được launcher xác minh."""

import argparse
from datetime import datetime, timezone
import json
import hashlib
from pathlib import Path
import re
import uuid
import zipfile
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://127.0.0.1:8081"


def get(path):
    with urlopen(BASE + path, timeout=10) as response:
        return response.read().decode("utf-8")


def post(run, version, items):
    fields = [("runId", run), ("version", str(version)), *[("items", item) for item in items]]
    with urlopen(Request(BASE + "/recommend", data=urlencode(fields).encode(), method="POST"), timeout=10) as response:
        return response.read().decode("utf-8")


def recommendation_codes(html):
    table = re.search(r'<table\b(?=[^>]*\bid="recommendations")[^>]*>(.*?)</table>', html, re.S)
    if not table:
        return []
    return re.findall(r'<tr[^>]*>\s*<td[^>]*>\s*([^<]+)</td>', table.group(1))


def verify_web(role):
    receipt = {"milestone": "M1", "machine_role": role, "mode": "SAMPLE", "checks": {}, "status": "FAIL"}
    output = ROOT / "artifacts/m1" / role / "web-receipt.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        proof = json.loads(get("/m1/verification"))
        assert proof["all_passed"] is True and proof["mode"] == "SAMPLE", "JAVA_ROUNDTRIP"
        receipt["proof"] = proof
        jar = ROOT / "web/target/market-basket-m1-0.0.1-SNAPSHOT.jar"
        receipt["web_jar_sha256"] = hashlib.sha256(jar.read_bytes()).hexdigest()
        with zipfile.ZipFile(jar) as package:
            receipt["packaged_mongo_dependencies"] = [name for name in package.namelist()
                if name.startswith("BOOT-INF/lib/") and any(part in name for part in ["mongodb-driver", "bson-", "spring-data-mongodb"])]
        receipt["checks"].update(proof["checks"])
        html = get("/")
        assert "DỮ LIỆU TỰ TẠO / SAMPLE" in html, "SAMPLE_LABEL"
        assert "&lt;script&gt;" in html and "<script>không chạy</script>" not in html, "THYMELEAF_ESCAPE"
        assert 'name="runId"' in html and 'name="version"' in html, "FORM_VERSION"
        run, version = proof["run_id"], proof["publication_version"]
        recommended = post(run, version, ["SKU_A", "SKU_B"])
        assert "Gợi ý từ luật" in recommended and recommendation_codes(recommended) == ["SKU_C"], "REAL_FORM_RULES"
        duplicate = post(run, version, ["SKU_A", "SKU_A", "SKU_B"])
        assert recommendation_codes(duplicate) == ["SKU_C"], "DUPLICATE_SELECTION"
        empty = post(run, version, [])
        assert "Hãy chọn ít nhất một sản phẩm" in empty, "EMPTY_CART"
        unknown = post(run, version, ["UNKNOWN"])
        assert "mã không hợp lệ" in unknown, "UNKNOWN_ITEM"
        no_rule = post(run, version, ["SKU_A", "SKU_B", "SKU_C"])
        assert "Không có luật gợi ý" in no_rule and recommendation_codes(no_rule) == [], "NO_FALLBACK"
        stale = post(run, version - 1, ["SKU_A"])
        assert "Lượt dữ liệu đã đổi" in stale, "STALE_FORM"
        receipt["checks"].update({"sample_label": True, "thymeleaf_escapes_names": True, "form_run_version": True,
            "real_form_rules": True, "duplicate_selection": True, "empty_cart": True,
            "unknown_item": True, "no_fallback": True, "stale_form": True})
        receipt["status"] = "PASS"
    except Exception as exc:
        receipt["error_type"] = type(exc).__name__
        if isinstance(exc, AssertionError):
            receipt["failed_check"] = str(exc)
        raise
    finally:
        receipt["checked_at_utc"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        receipt_text = json.dumps(receipt, ensure_ascii=False, indent=2)
        output.with_name(f"web-receipt-{uuid.uuid4()}.json").write_text(receipt_text, encoding="utf-8")
        output.write_text(receipt_text, encoding="utf-8")
        print(json.dumps({"status": receipt["status"], "receipt": str(output.relative_to(ROOT))}), flush=True)


def shutdown_mongo():
    from pymongo import MongoClient
    from pymongo.errors import AutoReconnect
    with MongoClient("mongodb://127.0.0.1:27018/?directConnection=true&serverSelectionTimeoutMS=5000") as client:
        try:
            client.admin.command("shutdown", force=False)
        except AutoReconnect:
            # The server closes the connection during successful shutdown.
            # Launcher additionally checks the pinned process has exited.
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["verify-web", "shutdown-mongo"])
    parser.add_argument("--machine-role", choices=["TV1", "TV2"])
    args = parser.parse_args()
    if args.action == "verify-web":
        if not args.machine_role:
            parser.error("--machine-role is required for receipt")
        verify_web(args.machine_role)
    else:
        shutdown_mongo()
