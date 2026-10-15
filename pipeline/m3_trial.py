"""One bounded full-train Spark FP-Growth trial; immutable run, DEVELOPMENT only."""
import argparse
from collections import Counter, defaultdict
import importlib.metadata
import json
import math
import os
from pathlib import Path
import sys
import threading
import time
import uuid

import psutil
from pymongo import MongoClient
from pyspark.ml.fpm import FPGrowth
from pyspark.sql import SparkSession, types as T

from m2_source import ROOT, SOURCE_HASH, URI, DATABASE, SCHEMA, POLICY, canonical, check, digest, save, immutable_batch
from m2_runtime import verify_owned_mongo, writer_lock, bson_counts
from m3_prepare import OUT, BASKET_SET, M2_RUN, file_hash, jsonl, load_jsonl, now, provenance, verified_preparation
from m3_protocol import PROTOCOL, TRIALS, evaluate, logical_checksum, validate_rule

MAX_OUTPUTS = 200000
MAX_JOB_SECONDS = 600
MIN_AVAILABLE_BYTES = 1024**3


def output_docs(run_id, catalog, itemsets, rules, n):
    items = [dict(r, _id=canonical([run_id, r['stock_code']]), run_id=run_id) for r in catalog]
    sets = [dict(_id=canonical([run_id, digest(list(key))]), run_id=run_id,
                 items=list(key), itemset_key=canonical(list(key)), frequency=value,
                 train_basket_count=n, support=value/n) for key, value in sorted(itemsets.items())]
    rules = [dict(r, _id=canonical([run_id, digest([r['antecedent'],r['consequent']])]), run_id=run_id) for r in rules]
    for rows in (items, sets, rules):
        check(len({r['_id'] for r in rows}) == len(rows), 'HASH_OR_ID_COLLISION')
    return dict(items=items, frequent_itemsets=sets, association_rules=rules)


def write_readback(db, outputs, run_id):
    validation = {}
    for collection, rows in outputs.items():
        for start in range(0, len(rows), 500):
            immutable_batch(db[collection], [bson_counts(row) for row in rows[start:start+500]])
        expected = sorted(rows, key=lambda r: r['_id'])
        actual = list(db[collection].find({'run_id': run_id}).sort('_id', 1))
        check(actual == expected, 'OUTPUT_READBACK_'+collection)
        field = 'train_basket_count' if collection == 'items' else 'frequency' if collection == 'frequent_itemsets' else None
        if field:
            check(db[collection].count_documents({'run_id': run_id, field: {'$type': 'long'}}) == len(rows), 'BSON_LONG_'+collection)
        if collection == 'frequent_itemsets':
            check(db[collection].count_documents({'run_id': run_id, 'train_basket_count': {'$type': 'long'}}) == len(rows), 'ITEMSET_DENOM_BSON_LONG')
        validation[collection] = dict(expected=len(rows), actual=len(actual), checksum=logical_checksum(
            [{k:v for k,v in row.items() if k not in ('_id','run_id')} for row in actual]))
    return validation


def checked_model(model, train, catalog, config, receipt):
    n = len(train)
    freq_frame = model.freqItemsets
    rules_frame = model.associationRules
    receipt['spark_output_schema'] = {'itemsets': freq_frame.schema.jsonValue(), 'rules': rules_frame.schema.jsonValue()}
    check(isinstance(freq_frame.schema['freq'].dataType, T.LongType)
          and isinstance(rules_frame.schema['consequent'].dataType, T.ArrayType), 'SPARK_OUTPUT_SCHEMA')
    count = freq_frame.count()
    check(count <= MAX_OUTPUTS, 'ITEMSET_OPERATIONAL_LIMIT')
    itemsets = {}
    for row in freq_frame.collect():
        key = tuple(sorted(row.items))
        check(key and len(set(key)) == len(key) and key not in itemsets
              and 0 < row.freq <= n and row.freq >= math.ceil(config['min_support']*n), 'ITEMSET_CONTRACT')
        itemsets[key] = int(row.freq)
    count = rules_frame.count()
    check(count <= MAX_OUTPUTS, 'RULE_OPERATIONAL_LIMIT')
    rules, keys = [], set()
    for row in rules_frame.collect():
        check(len(row.consequent) == 1 and len(row.antecedent) == len(set(row.antecedent)), 'CONSEQUENT_NOT_SCALAR_SEMANTICS')
        a, c = sorted(row.antecedent), row.consequent[0]
        key = canonical([a,c])
        check(key not in keys, 'DUPLICATE_RULE_KEY')
        keys.add(key)
        rule = dict(antecedent=a, consequent=c, rule_key=key, support=float(row.support),
                    confidence=float(row.confidence), lift=float(row.lift))
        validate_rule(rule)
        union, an, cn = itemsets[tuple(sorted(a+[c]))], itemsets[tuple(a)], itemsets[(c,)]
        expected = (union/n, union/an, (union/an)/(cn/n))
        check(all(math.isclose(rule[k], v, rel_tol=1e-12, abs_tol=1e-12)
                  for k,v in zip(('support','confidence','lift'), expected)), 'RULE_METRICS_COUNTS')
        check(rule['confidence'] >= config['min_confidence'], 'RULE_CONFIDENCE')
        rules.append(rule)
    expected_keys = set()
    for union, frequency in itemsets.items():
        if len(union) < 2:
            continue
        for c in union:
            a = tuple(x for x in union if x != c)
            if frequency/itemsets[a] >= config['min_confidence']:
                expected_keys.add(canonical([list(a), c]))
    check(keys == expected_keys, 'RULE_GENERATION_COMPLETENESS')
    frequencies = {r['stock_code']: r['train_basket_count'] for r in catalog}
    check({k[0]:v for k,v in itemsets.items() if len(k) == 1} ==
          {c:v for c,v in frequencies.items() if v >= math.ceil(config['min_support']*n)}, 'TRAIN_SINGLETON_FREQUENCIES')
    # Independent vertical invoice sets: validate EVERY itemset without relying on Spark's freq.
    vertical = defaultdict(set)
    for i, b in enumerate(train):
        for c in b['items']:
            vertical[c].add(i)
    for key, frequency in itemsets.items():
        common = set(vertical[key[0]])
        for c in key[1:]:
            common.intersection_update(vertical[c])
        check(len(common) == frequency, 'INDEPENDENT_ALL_ITEMSET_COUNTS')
    receipt['checks'].extend(['Spark schema/consequent cardinality','all itemset frequencies independently counted',
                              'every rule metrics and rule-set completeness','train denominator/singleton catalog parity'])
    return itemsets, sorted(rules, key=lambda r: r['rule_key'])


def trial(preparation, trial_index, machine_role):
    prep = verified_preparation(preparation)
    check(0 <= trial_index < len(TRIALS), 'TRIAL_INDEX')
    verify_owned_mongo()
    with writer_lock(), MongoClient(URI) as client:
        db = client[DATABASE]
        run_id = str(uuid.uuid4())
        path = OUT/run_id
        path.mkdir(parents=True, exist_ok=False)
        config = dict(TRIALS[trial_index], k=PROTOCOL['k'], driver_memory='768m', master='local[2]',
                      driver_java_options='-Xss4m', max_job_seconds=MAX_JOB_SECONDS, max_outputs=MAX_OUTPUTS)
        receipt = dict(milestone='M3', mode='FULL_SOURCE', evaluation_stage='DEVELOPMENT',
                       machine_role=machine_role, status='RUNNING', run_id=run_id, trial_index=trial_index,
                       preparation=str(preparation.relative_to(ROOT)), preparation_sha256=file_hash(preparation/'preparation.json'),
                       dataset_id=SOURCE_HASH, basket_set_id=BASKET_SET, preprocessing_run_id=M2_RUN,
                       protocol=PROTOCOL, config=config, protocol_sha256=digest(PROTOCOL), schema_version=SCHEMA,
                       policy=POLICY, policy_hash=digest(POLICY), ranking_version=PROTOCOL['ranking_version'],
                       started_at_utc=now(), final_status='NOT_RUN', human_review='PENDING_TV2',
                       publication='NOT_ATTEMPTED', checks=[], steps=[], **provenance())
        db.runs.insert_one(bson_counts(dict(_id=run_id, run_id=run_id, dataset_id=SOURCE_HASH, basket_set_id=BASKET_SET,
            stage='MODEL_DEVELOPMENT', mode='FULL_SOURCE', evaluation_stage='DEVELOPMENT', status='WRITING',
            schema_version=SCHEMA, policy_version=POLICY['version'], policy_hash=digest(POLICY),
            ranking_version=PROTOCOL['ranking_version'], config=config)))
        spark, timer = None, None
        start, last = time.monotonic(), time.monotonic()
        def step(label):
            nonlocal last
            current = time.monotonic()
            receipt['steps'].append(dict(name=label, seconds=current-last, end_at_utc=now()))
            last = current
            save(path/'receipt.json', receipt)
            print(label, flush=True)
        try:
            receipt['available_ram_before_bytes'] = psutil.virtual_memory().available
            check(receipt['available_ram_before_bytes'] >= MIN_AVAILABLE_BYTES, 'AVAILABLE_RAM_OPERATIONAL_GUARD')
            train = load_jsonl(preparation/'train-baskets.jsonl')
            catalog = load_jsonl(preparation/'catalog.jsonl')
            queries = load_jsonl(preparation/'dev-queries.jsonl')
            check(len(train) == prep['split']['train']['baskets'] and len(queries) == prep['eligible_dev_queries'], 'TRAIN_QUERY_COUNTS')
            os.environ['PYSPARK_PYTHON'] = sys.executable
            os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
            os.environ.setdefault('SPARK_LOCAL_IP', '127.0.0.1')
            jars = sorted((ROOT/'tmp/connector').glob('*.jar'))
            m2 = json.loads((ROOT/f'artifacts/m2/pipeline-{M2_RUN}.json').read_text(encoding='utf-8'))
            receipt['jars_sha256'] = {p.name: file_hash(p) for p in jars}
            check(receipt['jars_sha256'] == m2['jars_sha256'], 'PINNED_JARS_HASH')
            cp = os.pathsep.join(str(p) for p in jars)
            scratch = ROOT/'tmp/m3-spark'/run_id
            scratch.mkdir(parents=True, exist_ok=False)
            spark_config = {'spark.driver.memory': config['driver_memory'], 'spark.sql.shuffle.partitions': '8',
                'spark.driver.extraJavaOptions': config['driver_java_options'],
                'spark.default.parallelism': '2', 'spark.ui.enabled': 'false',
                'spark.sql.adaptive.coalescePartitions.enabled': 'false', 'spark.driver.bindAddress': '127.0.0.1',
                'spark.driver.extraClassPath': cp, 'spark.executor.extraClassPath': cp, 'spark.local.dir': str(scratch)}
            receipt['spark_config'] = spark_config
            builder = SparkSession.builder.master(config['master']).appName('BigData-M3-Development')
            for key, value in spark_config.items():
                builder = builder.config(key, value)
            spark = builder.getOrCreate()
            spark.sparkContext.setLogLevel('WARN')
            receipt['environment'] = dict(python=sys.version, spark=spark.version,
                scala=spark.sparkContext._jvm.scala.util.Properties.versionNumberString(),
                java=spark.sparkContext._jvm.java.lang.System.getProperty('java.version'),
                mongodb=client.server_info()['version'],
                jvm_input_arguments=list(spark.sparkContext._jvm.java.lang.management.ManagementFactory.getRuntimeMXBean().getInputArguments()),
                jvm_max_heap_bytes=spark.sparkContext._jvm.java.lang.Runtime.getRuntime().maxMemory(),
                packages={name: importlib.metadata.version(name) for name in ('pyspark','pymongo','numpy','psutil')})
            check('-Xss4m' in receipt['environment']['jvm_input_arguments']
                  and receipt['environment']['jvm_max_heap_bytes'] == 768*1024**2, 'JVM_ACTUAL_STACK_HEAP')
            step('read_and_spark_startup')
            spark.sparkContext.setJobGroup(run_id, 'bounded M3 train fit and extraction', interruptOnCancel=True)
            expired = threading.Event()
            def cancel():
                expired.set()
                spark.sparkContext.cancelJobGroup(run_id)
            timer = threading.Timer(MAX_JOB_SECONDS, cancel)
            timer.daemon = True
            timer.start()
            frame = spark.createDataFrame([(b['items'],) for b in train],
                T.StructType([T.StructField('items', T.ArrayType(T.StringType(), False), False)])).repartition(config['num_partitions']).cache()
            check(frame.count() == len(train), 'SPARK_TRAIN_COUNT')
            model = FPGrowth(itemsCol='items', minSupport=config['min_support'],
                             minConfidence=config['min_confidence'], numPartitions=config['num_partitions']).fit(frame)
            step('fit_train')
            itemsets, rules = checked_model(model, train, catalog, config, receipt)
            check(not expired.is_set(), 'TRIAL_TIME_LIMIT')
            timer.cancel()
            step('extract_and_independent_validation')
            receipt['counts'] = dict(train_baskets=len(train), train_items=len(catalog), itemsets=len(itemsets),
                                     rules=len(rules), eligible_dev_queries=len(queries))
            predictions, development = evaluate(queries, rules, catalog, PROTOCOL['k'])
            receipt['development'] = development
            receipt['new_items'] = dict(targets=sum(r['new_target'] for r in predictions),
                queries_with_new_context=sum(bool(r['new_context']) for r in predictions),
                context_occurrences=sum(len(r['new_context']) for r in predictions))
            jsonl(path/'dev-predictions.jsonl', predictions)
            step('evaluate_development')
            outputs = output_docs(run_id, catalog, itemsets, rules, len(train))
            for name, docs in outputs.items():
                jsonl(path/f'{name}.jsonl', docs)
            receipt['output_validation'] = write_readback(db, outputs, run_id)
            receipt['checks'].append('immutable output exact readback/IDs/canonical keys/BSON long')
            # Concrete real examples include evidence paths; no raw personal fields.
            examples = {'scope': 'DEVELOPMENT', 'run_id': run_id,
                'prediction_examples': predictions[:5],
                'train_rule_examples': rules[:3],
                'train_lineage': str((preparation/'train-lineage-examples.jsonl').relative_to(ROOT)),
                'test_status': 'NOT_RUN'}
            save(path/'review-examples.json', examples)
            step('mongo_write_readback')
            receipt.update(split=prep['split'], invoice_overlap=0,
                stage_counts=json.loads((ROOT/f'artifacts/m2/pipeline-{M2_RUN}.json').read_text(encoding='utf-8'))['counts'],
                status='PASS', elapsed_seconds=time.monotonic()-start, finished_at_utc=now(),
                files_sha256={p.name: file_hash(p) for p in sorted(path.glob('*.jsonl'))})
            manifest = bson_counts(receipt)
            check(db.runs.update_one({'_id': run_id, 'status': 'WRITING'}, {'$set': {'status': 'VALIDATED', 'manifest': manifest}}).modified_count == 1, 'RUN_VALIDATE_STATE')
            check(db.runs.update_one({'_id': run_id, 'status': 'VALIDATED'}, {'$set': {'status': 'READY'}}).modified_count == 1, 'RUN_READY_STATE')
            check(db.runs.find_one({'_id': run_id})['manifest'] == manifest, 'MANIFEST_READBACK')
        except Exception as exc:
            receipt.update(status='FAIL', error=str(exc), error_type=type(exc).__name__, finished_at_utc=now(), elapsed_seconds=time.monotonic()-start)
            db.runs.update_one({'_id': run_id, 'status': {'$in': ['WRITING','VALIDATED']}},
                {'$set': {'status': 'FAILED', 'error_type': type(exc).__name__, 'manifest': bson_counts(receipt)}})
            raise
        finally:
            if timer:
                timer.cancel()
            save(path/'receipt.json', receipt)
            if spark:
                spark.stop()
            print(canonical({'run_id': run_id, 'status': receipt['status']}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--preparation', type=Path, required=True)
    parser.add_argument('--trial-index', type=int, required=True)
    parser.add_argument('--machine-role', choices=['TV1','TV2'], required=True)
    args = parser.parse_args()
    trial(args.preparation.resolve(), args.trial_index, args.machine_role)
