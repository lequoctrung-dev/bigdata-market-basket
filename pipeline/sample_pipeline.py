"""Prototype M1: MongoDB -> Spark/P-01/FP-Growth -> MongoDB; chỉ dữ liệu mẫu."""

import argparse
from datetime import datetime, timezone
from decimal import Decimal
import importlib.metadata
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import uuid

from bson.int64 import Int64
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pyspark.ml.fpm import FPGrowth
from pyspark.sql import SparkSession, Window, functions as F, types as T

from sample_fixture import (
    SCHEMA_VERSION, POLICY_VERSION, RANKING_VERSION, EXPECTED_BASKETS,
    EXCLUDED_CODES, canonical, digest, fixture_rows, reference_itemsets, tuple_key,
)

ROOT = Path(__file__).resolve().parents[1]
DATABASE = "bigdata_m1_sample"
URI = "mongodb://127.0.0.1:27018/?directConnection=true&serverSelectionTimeoutMS=5000"
CONNECTOR = "org.mongodb.spark:mongo-spark-connector_2.13:11.1.0"


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def ensure(condition, message):
    if not condition:
        raise RuntimeError(message)


def immutable_insert(collection, document):
    """Chạy lại cùng ID chỉ được phép cùng nội dung, không overwrite nguồn."""
    existing = collection.find_one({"_id": document["_id"]})
    if existing is not None:
        ensure(existing == document, f"ID_CONFLICT in {collection.name}")
        return
    try:
        collection.insert_one(document)
    except DuplicateKeyError:
        ensure(collection.find_one({"_id": document["_id"]}) == document,
               f"ID_CONFLICT in {collection.name}")


def read_spark(spark, collection, schema, match=None):
    reader = (spark.read.format("mongodb").option("connection.uri", URI)
              .option("database", DATABASE).option("collection", collection)
              .option("partitioner", "com.mongodb.spark.sql.connector.read.partitioner.SinglePartitionPartitioner")
              .option("mode", "FAILFAST").schema(schema))
    if match:
        reader = reader.option("aggregation.pipeline", canonical([{"$match": match}]))
    return reader.load()


def write_spark(frame, collection):
    # Không mode overwrite: connector overwrite có thể DROP collection.
    (frame.write.format("mongodb").option("connection.uri", URI)
     .option("database", DATABASE).option("collection", collection)
     .option("operationType", "replace").option("idFieldList", "_id")
     .option("upsertDocument", "true").option("ignoreNullValues", "false")
     .option("ordered", "true").mode("append").save())


def ranked(rules, query, k):
    query = set(query)
    candidates = {}
    for rule in rules:
        if set(rule["antecedent"]) <= query and rule["consequent"] not in query:
            key = (-rule["confidence"], -rule["lift"], -rule["support"],
                   rule["consequent"], tuple(rule["antecedent"]))
            previous = candidates.get(rule["consequent"])
            if previous is None or key < previous[0]:
                candidates[rule["consequent"]] = (key, rule)
    return [value[1] for value in sorted(candidates.values(), key=lambda v: v[0])[:k]]


def publish_run(db, run_id, basket_set_id, previous):
    run = db.runs.find_one({"_id": run_id})
    ensure(run is not None and run.get("status") == "READY"
           and run.get("schema_version") == SCHEMA_VERSION
           and run.get("basket_set_id") == basket_set_id,
           "RUN_NOT_READY_FOR_PUBLICATION")
    pointer = {"_id": "active", "run_id": run_id, "basket_set_id": basket_set_id,
               "schema_version": SCHEMA_VERSION,
               "version": 1 if previous is None else previous["version"] + 1,
               "published_at_utc": now()}
    if previous is None:
        db.publication.insert_one(pointer)
    else:
        ensure(db.publication.replace_one({"_id": "active", "run_id": previous["run_id"],
                                           "version": previous["version"]}, pointer).modified_count == 1,
               "PUBLICATION_VERSION_CONFLICT")
    return pointer


def build(args):
    receipt = {
        "milestone": "M1", "machine_role": args.machine_role, "mode": "SAMPLE",
        "dataset_kind": "SYNTHETIC", "started_at_utc": now(), "status": "RUNNING",
        "schema_version": SCHEMA_VERSION, "checks": {}, "limitations": [
            "Không đọc Online Retail II; không full-source/đánh giá khoa học final.",
            "Không thay receipt hoặc học/review của thành viên trên máy khác.",
        ],
    }
    receipt_path = ROOT / "artifacts/m1" / args.machine_role / "pipeline-receipt.json"
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    client = None
    spark = None
    run_id = str(uuid.uuid4())
    receipt["run_id"] = run_id
    try:
        # Chỉ kết nối đích cố định đã chọn cho M1; không nhận URI chứa secrets.
        client = MongoClient(URI)
        client.admin.command("ping")
        db = client[DATABASE]
        old_pointer = db.publication.find_one({"_id": "active"})
        receipt["environment"] = {
            "python": sys.version.split()[0],
            "pyspark": importlib.metadata.version("pyspark"),
            "pymongo": importlib.metadata.version("pymongo"),
            "mongodb": client.server_info()["version"],
            "connector_coordinate": CONNECTOR,
            "java_version": subprocess.run(["java", "-version"], capture_output=True, text=True).stderr.strip(),
        }
        rows = fixture_rows()
        dataset_id = digest(rows)
        basket_set_id = digest([dataset_id, SCHEMA_VERSION, POLICY_VERSION, "merchandise"])
        receipt.update(dataset_id=dataset_id, basket_set_id=basket_set_id,
                       policy_version=POLICY_VERSION, ranking_version=RANKING_VERSION,
                       code_revision=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                       working_tree_dirty=bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).strip()),
                       code_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__), Path(__file__).with_name("sample_fixture.py")]})
        metadata = {
            "_id": dataset_id, "source_sha256": dataset_id, "dataset_kind": "SYNTHETIC",
            "mode": "SAMPLE", "schema_version": SCHEMA_VERSION,
            "description": "M1 five-basket fixture, không phải Online Retail II",
            "status": "READY", "expected_row_count": Int64(len(rows)),
        }
        for row in rows:
            document = dict(row, dataset_id=dataset_id,
                            _id=canonical([dataset_id, row["sheet_index"], row["source_row"]]),
                            tuple_key=tuple_key(row["source_cells"]))
            immutable_insert(db.source_rows, document)
        ensure(db.source_rows.count_documents({"dataset_id": dataset_id}) == len(rows), "SOURCE_COUNT")
        immutable_insert(db.datasets, metadata)
        # Thử idempotency và xung đột bằng cùng API nguồn, không sửa dữ liệu.
        first = db.source_rows.find_one({"dataset_id": dataset_id})
        immutable_insert(db.source_rows, first)
        try:
            immutable_insert(db.source_rows, dict(first, tuple_key="deliberate-conflict"))
        except RuntimeError as exc:
            ensure(str(exc).startswith("ID_CONFLICT"), "CONFLICT_WRONG_ERROR")
        else:
            raise RuntimeError("SOURCE_CONFLICT_NOT_REJECTED")
        receipt["checks"]["source_retry_and_conflict"] = True
        db.runs.insert_one({"_id": run_id, "run_id": run_id, "dataset_id": dataset_id,
                            "basket_set_id": basket_set_id, "status": "WRITING", "mode": "SAMPLE",
                            "schema_version": SCHEMA_VERSION})
        os.environ["PYSPARK_PYTHON"] = sys.executable
        os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
        os.environ.setdefault("SPARK_LOCAL_IP", "127.0.0.1")
        jars = sorted((ROOT / "tmp/connector").glob("*.jar"))
        expected_jars = {"mongo-spark-connector_2.13-11.1.0.jar", "mongodb-driver-sync-5.1.4.jar",
                         "mongodb-driver-core-5.1.4.jar", "bson-5.1.4.jar", "bson-record-codec-5.1.4.jar"}
        ensure({p.name for p in jars} == expected_jars, "Run Setup to resolve the exact pinned connector/driver JARs")
        classpath = os.pathsep.join(str(p) for p in jars)
        receipt["connector_jars_sha256"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in jars}
        # local[2] shares the driver JVM. Load local runtime dependencies before
        # gateway launch instead of Spark addFile distribution (winutils chmod).
        spark = (SparkSession.builder.appName("BigData-M1-Synthetic").master("local[2]")
                 .config("spark.driver.memory", "512m")
                 .config("spark.sql.shuffle.partitions", "2")
                 .config("spark.default.parallelism", "2")
                 .config("spark.ui.enabled", "false")
                 .config("spark.driver.bindAddress", "127.0.0.1")
                 .config("spark.driver.extraClassPath", classpath)
                 .config("spark.executor.extraClassPath", classpath).getOrCreate())
        spark.sparkContext.setLogLevel("WARN")
        receipt["environment"].update(spark=spark.version,
            scala=spark.sparkContext._jvm.scala.util.Properties.versionNumberString())
        cell_schema = T.StructType([T.StructField("type", T.StringType(), False),
                                    T.StructField("value", T.StringType(), True)])
        source_schema = T.StructType([
            T.StructField("_id", T.StringType(), False), T.StructField("dataset_id", T.StringType(), False),
            T.StructField("sheet_index", T.LongType(), False), T.StructField("source_row", T.LongType(), False),
            T.StructField("source_cells", T.ArrayType(cell_schema, False), False),
            T.StructField("tuple_key", T.StringType(), False),
        ])
        source = read_spark(spark, "source_rows", source_schema, {"dataset_id": dataset_id}).repartition(2)
        raw_count = source.count()
        retained = (source.withColumn("source_rank", F.row_number().over(
            Window.partitionBy("tuple_key").orderBy("sheet_index", "source_row")))
            .filter(F.col("source_rank") == 1))
        retained_count = retained.count()
        winner = retained.filter(F.col("tuple_key") == first["tuple_key"]).select("sheet_index", "source_row").collect()
        ensure(len(winner) == 1 and winner[0].sheet_index == 0 and winner[0].source_row == 2, "P01_FIRST_SOURCE")
        ensure(raw_count - retained_count == 2, "P01_DUPLICATE_COUNT")
        receipt["checks"]["p01_first_source_across_partitions"] = True
        def value(i):
            return F.col("source_cells").getItem(i).getField("value")
        lines = retained.select(
            "_id", "source_cells", F.trim(value(0)).alias("invoice"), F.trim(value(1)).alias("stock_code"),
            value(2).alias("description"), value(3).cast(T.LongType()).alias("quantity"),
            value(4).alias("invoice_time_local"), value(5).alias("price_text"),
            value(6).alias("customer_id"))
        positive = lines.filter((~F.upper("invoice").startswith("C")) & (F.col("quantity") > 0)
                                & (F.col("price_text").cast(T.DecimalType(20, 8)) > 0))
        merchandise = positive.filter(~F.upper("stock_code").isin(sorted(EXCLUDED_CODES))
                                       & ~F.lower("stock_code").startswith("gift_"))
        ensure(merchandise.filter(F.col("stock_code") == "SKU_A").count() == 5, "DO_NOT_DEDUP_INVOICE_ITEM")
        baskets = (merchandise.groupBy("invoice").agg(F.sort_array(F.collect_set("stock_code")).alias("items"),
                    F.min("invoice_time_local").alias("invoice_time_local"),
                    F.count("*").alias("retained_line_count"))
                   .withColumn("basket_set_id", F.lit(basket_set_id)))
        expected_baskets = {r.invoice: list(r.items) for r in baskets.collect()}
        ensure(expected_baskets == EXPECTED_BASKETS, "BASKET_REFERENCE")
        # Five baskets are train-only mechanism fixture; no dev/test evaluation.
        k, min_support, min_confidence = 3, 0.4, 0.5
        model = FPGrowth(itemsCol="items", minSupport=min_support, minConfidence=min_confidence).fit(baskets)
        itemsets = {tuple(sorted(r.items)): r.freq for r in model.freqItemsets.collect()}
        reference = reference_itemsets()
        ensure(itemsets == {key: n for key, n in reference.items() if n / 5 >= min_support}, "ITEMSET_REFERENCE")
        rules = []
        for row in model.associationRules.collect():
            antecedent, consequent = sorted(row.antecedent), row.consequent[0]
            union = tuple(sorted(antecedent + [consequent]))
            expected = (reference[union] / 5,
                        reference[union] / reference[tuple(antecedent)],
                        (reference[union] / reference[tuple(antecedent)]) / (reference[(consequent,)] / 5))
            values = (row.support, row.confidence, row.lift)
            ensure(all(math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-12) for a, b in zip(values, expected)), "RULE_REFERENCE")
            rule_key = canonical([antecedent, consequent])
            rules.append({"_id": canonical([run_id, digest([antecedent, consequent])]),
                          "run_id": run_id, "rule_key": rule_key, "antecedent": antecedent,
                          "consequent": consequent, "support": float(row.support),
                          "confidence": float(row.confidence), "lift": float(row.lift)})
        expected_rule_keys = set()
        for union, frequency in reference.items():
            if len(union) < 2 or frequency / 5 < min_support:
                continue
            for consequent in union:
                antecedent = tuple(c for c in union if c != consequent)
                if frequency / reference[antecedent] >= min_confidence:
                    expected_rule_keys.add(canonical([list(antecedent), consequent]))
        ensure({r["rule_key"] for r in rules} == expected_rule_keys, "RULE_SET_REFERENCE")
        receipt["checks"]["fp_growth_against_independent_counts"] = True
        basket_out = baskets.withColumn("_id", F.to_json(F.array(F.lit(basket_set_id), F.col("invoice"))))
        write_spark(basket_out, "baskets")
        before = db.baskets.count_documents({"basket_set_id": basket_set_id})
        write_spark(basket_out, "baskets")
        ensure(before == db.baskets.count_documents({"basket_set_id": basket_set_id}) == 5, "CONNECTOR_RETRY_DUPLICATED")
        receipt["checks"]["connector_append_replace_retry"] = True
        for items, frequency in itemsets.items():
            key = canonical(list(items))
            immutable_insert(db.frequent_itemsets, {"_id": canonical([run_id, digest(list(items))]),
                "run_id": run_id, "items": list(items), "itemset_key": key,
                "frequency": Int64(frequency), "train_basket_count": Int64(5), "support": frequency / 5})
        # Rules/catalog are written with Spark too; schema is explicit, including empty-array/null round-trip.
        rule_schema = T.StructType([
            *[T.StructField(n, T.StringType(), False) for n in ["_id", "run_id", "rule_key"]],
            T.StructField("antecedent", T.ArrayType(T.StringType(), False), False),
            T.StructField("consequent", T.StringType(), False),
            *[T.StructField(n, T.DoubleType(), False) for n in ["support", "confidence", "lift"]],
        ])
        write_spark(spark.createDataFrame(rules, rule_schema), "association_rules")
        catalog = [{"_id": canonical([run_id, code]), "run_id": run_id, "stock_code": code,
                    "display_name": f"MẪU M1 — {code} <script>không chạy</script>",
                    "train_basket_count": Int64(reference[(code,)])}
                   for code in sorted({c for codes in EXPECTED_BASKETS.values() for c in codes})]
        for document in catalog:
            immutable_insert(db.items, document)
        # Sample quantities fit 10 digits. 20+20+1 precision would exceed 38
        # and Spark would reduce scale to 6; preserve 8 decimal places here.
        ensure(merchandise.filter(F.col("quantity") >= 10**10).count() == 0, "SAMPLE_QUANTITY_RANGE")
        money = merchandise.select((F.col("quantity").cast(T.DecimalType(10, 0))
                                     * F.col("price_text").cast(T.DecimalType(20, 8))).alias("amount"))
        ensure(money.schema["amount"].dataType.scale == 8, "MONEY_SCALE_CHANGED")
        amount = money.agg(F.sum("amount")).first()[0]
        # 11 item rows + extra Quantity=2 row = 13 units, all same exact fixture price.
        expected_amount = Decimal("1.23456789") * 13
        ensure(amount == expected_amount, "EXACT_MONEY_TOTAL")
        receipt["checks"]["exact_decimal_product_and_sum"] = True
        receipt["decimal_types"] = {"quantity": "decimal(10,0)", "price": "decimal(20,8)",
                                    "product": money.schema.simpleString(), "sample_only": True}
        summary = {"_id": canonical([basket_set_id, "merchandise", "m1", "all"]),
                   "basket_set_id": basket_set_id, "scope": "merchandise", "summary_type": "m1",
                   "bucket_key": "all", "basket_count": 5, "line_value_gbp": format(amount, "f"),
                   "roundtrip": {"invoice": "0001", "customer_id": None, "items": ["SKU_A", "SKU_B"],
                       "empty_items": [], "price_text": "1.23456789", "invoice_time_local": "2020-01-02T03:04:05"}}
        summary_schema = T.StructType([
            *[T.StructField(n, T.StringType(), False) for n in ["_id", "basket_set_id", "scope", "summary_type", "bucket_key"]],
            T.StructField("basket_count", T.LongType(), False), T.StructField("line_value_gbp", T.StringType(), False),
            T.StructField("roundtrip", T.StructType([
                T.StructField("invoice", T.StringType(), False), T.StructField("customer_id", T.StringType(), True),
                T.StructField("items", T.ArrayType(T.StringType()), False), T.StructField("empty_items", T.ArrayType(T.StringType()), False),
                T.StructField("price_text", T.StringType(), False), T.StructField("invoice_time_local", T.StringType(), False),
            ]), False),
        ])
        write_spark(spark.createDataFrame([summary], summary_schema), "summaries")
        returned = read_spark(spark, "summaries", summary_schema, {"_id": summary["_id"]}).first().asDict(recursive=True)
        ensure(returned == summary, "SPARK_BSON_ROUNDTRIP")
        receipt["checks"]["spark_bson_decimal_text_null_arrays_local_time"] = True
        sample_queries = [[], ["SKU_A"], ["SKU_A", "SKU_B"], ["SKU_A", "SKU_B", "SKU_C"], ["SKU_C"]]
        ranking_cases = [{"query": query, "expected": [r["consequent"] for r in ranked(rules, query, k)]}
                         for query in sample_queries]
        positive_count, merchandise_count = positive.count(), merchandise.count()
        receipt["counts"] = {"raw": raw_count, "retained": retained_count,
                             "duplicates_after_first": raw_count - retained_count,
                             "positive_valid": positive_count, "merchandise": merchandise_count,
                             "baskets": 5, "itemsets": len(itemsets), "rules": len(rules)}
        for collection, match, expected_count in [
            (db.baskets, {"basket_set_id": basket_set_id}, 5),
            (db.items, {"run_id": run_id}, 3),
            (db.frequent_itemsets, {"run_id": run_id}, len(itemsets)),
            (db.association_rules, {"run_id": run_id}, len(rules)),
            (db.summaries, {"_id": summary["_id"]}, 1),
        ]:
            ensure(collection.count_documents(match) == expected_count, f"OUTPUT_COUNT_{collection.name}")
        db.runs.update_one({"_id": run_id, "status": "WRITING"}, {"$set": {
            "status": "VALIDATED", "policy_version": POLICY_VERSION, "ranking_version": RANKING_VERSION,
            "config": {"min_support": min_support, "min_confidence": min_confidence, "k": k,
                       "split": "SYNTHETIC_TRAIN_ONLY", "seed": None},
            "manifest": {"mode": "SAMPLE", "dataset_kind": "SYNTHETIC", "evaluation_stage": "SAMPLE",
                         "final_status": "NOT_RUN", "counts": receipt["counts"], "ranking_cases": ranking_cases,
                         "environment": receipt["environment"], "code_sha256": receipt["code_sha256"],
                         "code_revision": receipt["code_revision"], "working_tree_dirty": receipt["working_tree_dirty"],
                         "connector_jars_sha256": receipt["connector_jars_sha256"],
                         "train_basket_count": 5, "sample_only": True},
        }})
        ensure(db.runs.update_one({"_id": run_id, "status": "VALIDATED"}, {"$set": {"status": "READY"}}).modified_count == 1, "READY_STATE")
        pointer = publish_run(db, run_id, basket_set_id, old_pointer)
        try:
            publish_run(db, run_id, basket_set_id, dict(pointer, version=pointer["version"] - 1))
        except RuntimeError as exc:
            ensure(str(exc) == "PUBLICATION_VERSION_CONFLICT", "CAS_WRONG_ERROR")
        else:
            raise RuntimeError("STALE_PUBLICATION_NOT_REJECTED")
        # A deliberately incomplete run must never change the active pointer.
        failed_id = str(uuid.uuid4())
        db.runs.insert_one({"_id": failed_id, "status": "FAILED", "mode": "SAMPLE",
                            "schema_version": SCHEMA_VERSION, "error_code": "M1_INJECTED_WRITE_FAILURE"})
        try:
            publish_run(db, failed_id, basket_set_id, pointer)
        except RuntimeError as exc:
            ensure(str(exc) == "RUN_NOT_READY_FOR_PUBLICATION", "FAILED_RUN_WRONG_ERROR")
        else:
            raise RuntimeError("FAILED_RUN_PUBLICATION_NOT_REJECTED")
        ensure(db.publication.find_one({"_id": "active"}) == pointer, "FAILED_RUN_CHANGED_POINTER")
        receipt["checks"]["publication_cas_and_failed_run"] = True
        receipt.update(status="PASS", publication_version=pointer["version"], ranking_cases=ranking_cases,
                       expected_money_gbp=format(expected_amount, "f"))
    except Exception as exc:
        receipt.update(status="FAIL", error_type=type(exc).__name__)
        # Keep local traceback for diagnosis; do not put connection URI/secrets in receipt.
        if client is not None:
            try:
                client[DATABASE].runs.update_one({"_id": run_id, "status": {"$in": ["WRITING", "VALIDATED"]}},
                                                {"$set": {"status": "FAILED", "error_code": type(exc).__name__}})
            except Exception:
                receipt["failure_state_update"] = "UNCONFIRMED"
        raise
    finally:
        if spark is not None:
            spark.stop()
        if client is not None:
            client.close()
        receipt["finished_at_utc"] = now()
        receipt_text = json.dumps(receipt, ensure_ascii=False, indent=2)
        receipt_path.with_name(f"pipeline-receipt-{run_id}.json").write_text(receipt_text, encoding="utf-8")
        receipt_path.write_text(receipt_text, encoding="utf-8")
        print(canonical({"receipt": str(receipt_path.relative_to(ROOT)), "status": receipt["status"]}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--machine-role", required=True, choices=["TV1", "TV2"])
    build(parser.parse_args())
