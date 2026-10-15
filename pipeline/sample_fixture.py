"""Dữ liệu tự tạo cho M1; tuyệt đối không đọc Online Retail II."""

from copy import deepcopy
from decimal import Decimal
import hashlib
import json

SCHEMA_VERSION = "m0-contract-v1"
POLICY_VERSION = "m1-synthetic-policy-v1"
RANKING_VERSION = "confidence-lift-support-codepoint-v1"
EXPECTED_BASKETS = {
    "0001": ["SKU_A", "SKU_B", "SKU_C"],
    "0002": ["SKU_A", "SKU_B", "SKU_C"],
    "0003": ["SKU_A", "SKU_B"],
    "0004": ["SKU_A", "SKU_C"],
    "0005": ["SKU_C"],
}
EXCLUDED_CODES = {
    "POST", "DOT", "C2", "BANK CHARGES", "AMAZONFEE", "D", "ADJUST",
    "ADJUST2", "B", "S", "M", "GIFT", "TEST001", "TEST002",
}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def cell(kind, value):
    return {"type": kind, "value": value}


def make_row(invoice, code, quantity="1", price="1.23456789", sheet=0, row=2):
    return {
        "sheet_index": sheet,
        "source_row": row,
        "source_cells": [
            cell("text", invoice), cell("text", code),
            cell("text", f"MẪU M1 — {code} <script>không chạy</script>"),
            cell("number", quantity), cell("local_datetime", "2020-01-02T03:04:05"),
            cell("number", price), cell("null", None), cell("text", "SYNTHETIC"),
        ],
    }


def fixture_rows():
    rows = []
    for invoice, items in EXPECTED_BASKETS.items():
        for code in items:
            rows.append(make_row(invoice, code, row=len(rows) + 2))
    # Numeric 1 và 1.0 bằng nhau, source_row nhỏ nhất vẫn được giữ.
    repeated = deepcopy(rows[0])
    repeated["source_row"] = 30
    repeated["source_cells"][3]["value"] = "1.0"
    rows.append(repeated)
    cross_sheet = deepcopy(rows[0])
    cross_sheet.update(sheet_index=1, source_row=2)
    rows.append(cross_sheet)
    # Cùng Invoice/StockCode nhưng khác Quantity phải giữ dòng này.
    rows.append(make_row("0001", "SKU_A", quantity="2", row=31))
    for i, code in enumerate(["POST", "m", "gift_0001_10", "TEST001", "TEST002"]):
        rows.append(make_row("0001", code, row=32 + i))
    rows.append(make_row("C0006", "SKU_A", row=37))
    rows.append(make_row("0007", "SKU_A", quantity="-1", row=38))
    rows.append(make_row("0008", "SKU_A", price="0", row=39))
    return rows


def tuple_key(cells):
    """Số chuẩn hóa theo giá trị; text/null/ngày giữ kiểu và payload."""
    values = []
    for c in cells:
        value = c["value"]
        if c["type"] == "number":
            value = format(Decimal(value).normalize(), "f")
        values.append([c["type"], value])
    return canonical(values)


def is_excluded(code):
    return code.upper() in EXCLUDED_CODES or code.lower().startswith("gift_")


def reference_itemsets():
    """Đáp án độc lập cho 5 giỏ, không gọi Spark hoặc DB."""
    from itertools import combinations
    counts = {}
    for items in EXPECTED_BASKETS.values():
        for size in range(1, len(items) + 1):
            for subset in combinations(items, size):
                counts[subset] = counts.get(subset, 0) + 1
    return counts
