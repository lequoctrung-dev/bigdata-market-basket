"""M6: freshly computed local preprocessing -> train-only frozen Spark fit -> NEW run.

No test items are read. Never invoke the M3 grid/selection or mutate historical runs.
"""
import importlib.metadata
import json
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

from m2_source import ROOT, SOURCE_HASH, SCHEMA, POLICY, check, digest, save, canonical
from m2_runtime import verify_owned_mongo, writer_lock, bson_counts
from m3_prepare import file_hash, now, jsonl, load_jsonl, provenance
from m3_protocol import PROTOCOL, evaluate
from m3_trial import checked_model, output_docs, write_readback, MIN_AVAILABLE_BYTES
from m5_common import fail_unfinished
from m6_common import URI, DATABASE, FREEZE_HASH, context, validated_inputs, ready_snapshot, check_ready_snapshot
from m6_verify import verify_run


def complete(db, path, receipt):
    """Postcheck VALIDATED with persisted manifest before final transition; no writes after READY."""
    receipt.update(status='PASS', finished_at_utc=now(),
        files_sha256={p.name:file_hash(p) for p in sorted(path.glob('*.jsonl'))})
    save(path/'receipt.json', receipt)
    rid = receipt['run_id']
    check(db.runs.update_one({'_id':rid,'status':'WRITING'},
        {'$set':{'status':'VALIDATED','manifest':bson_counts(receipt)}}).modified_count == 1, 'VALIDATE_CAS')
    report = verify_run(db, rid, path.parent, allow_validated=True)
    save(path/'postcheck-before-ready.json', report)
    check(db.runs.update_one({'_id':rid,'status':'VALIDATED'}, {'$set':{'status':'READY'}}).modified_count == 1, 'READY_CAS')


def main(session, preparation):
    OUT = session
    verify_owned_mongo()
    with writer_lock(), MongoClient(URI) as client:
        db = client[DATABASE]
        frozen, prep_path, prep = validated_inputs(db, session, preparation)
        state, (_, old, _) = context(session)
        M2_RUN = prep['preprocessing_run_id']; BASKET_SET = prep['basket_set_id']
        before = ready_snapshot(db)
        rid = str(uuid.uuid4()); path = OUT/rid
        path.mkdir(parents=True, exist_ok=False)
        config = frozen['config'].copy()
        receipt = dict(milestone='M6', mode='FULL_SOURCE', evaluation_stage='DEVELOPMENT',
            machine_role=state['machine_role'], machine_id=state['machine_id'], database=DATABASE, run_id=rid, status='RUNNING', started_at_utc=now(),
            dataset_id=SOURCE_HASH, basket_set_id=BASKET_SET, preprocessing_run_id=M2_RUN,
            schema_version=SCHEMA, policy=POLICY, policy_hash=digest(POLICY),
            ranking_version=PROTOCOL['ranking_version'], protocol=PROTOCOL, protocol_sha256=digest(PROTOCOL),
            config=config, freeze_sha256=FREEZE_HASH, selected_m3_run_id=frozen['selected_run_id'],
            preparation=str(prep_path.relative_to(ROOT)), preparation_sha256=file_hash(prep_path/'preparation.json'),
            split=prep['split'], invoice_overlap=0, stage_counts=db.runs.find_one({'_id':M2_RUN})['manifest']['counts'],
            final_status='NOT_RUN', publication='NOT_ATTEMPTED', human_review='PENDING_BOTH',
            input_reuse='None of historical outputs; full XLSX audit/import/Spark preprocessing and preparation rerun in this session',
            execution='fresh Mongo train read, Spark fit/extraction/independent validation/dev eval/new immutable outputs',
            checks=[], steps=[], **provenance())
        run = dict(_id=rid, run_id=rid, status='WRITING', stage='MODEL_DEVELOPMENT',
            evaluation_stage='DEVELOPMENT', mode='FULL_SOURCE', dataset_id=SOURCE_HASH, basket_set_id=BASKET_SET,
            schema_version=SCHEMA, policy_version=POLICY['version'], policy_hash=digest(POLICY),
            ranking_version=PROTOCOL['ranking_version'], config=config)
        save(path/'receipt.json', receipt)
        db.runs.insert_one(bson_counts(run))
        spark = timer = None
        start = last = time.monotonic()
        def step(name):
            nonlocal last
            current = time.monotonic()
            receipt['steps'].append(dict(name=name,seconds=current-last,end_at_utc=now()))
            last = current
            save(path/'receipt.json',receipt)
            print(name,flush=True)
        try:
            receipt['available_ram_before_bytes'] = psutil.virtual_memory().available
            check(receipt['available_ram_before_bytes'] >= MIN_AVAILABLE_BYTES, 'AVAILABLE_RAM_OPERATIONAL_GUARD')
            train = list(db.baskets.find({'basket_set_id':BASKET_SET,'invoice_time_local':
                {'$gte':PROTOCOL['train_start'],'$lt':PROTOCOL['dev_start']}},{'_id':0}).sort('invoice',1))
            check(train == load_jsonl(prep_path/'train-baskets.jsonl'), 'MONGO_TRAIN_FROZEN_INPUT')
            catalog = load_jsonl(prep_path/'catalog.jsonl'); queries = load_jsonl(prep_path/'dev-queries.jsonl')
            os.environ['PYSPARK_PYTHON'] = os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
            os.environ.setdefault('SPARK_LOCAL_IP','127.0.0.1')
            jars = sorted((ROOT/'tmp/connector').glob('*.jar'))
            receipt['jars_sha256'] = {p.name:file_hash(p) for p in jars}
            # old is a checksum-verified reference receipt, never a training input
            check(receipt['jars_sha256'] == old['jars_sha256'], 'PINNED_JARS')
            cp = os.pathsep.join(map(str,jars)); scratch = ROOT/'tmp/m6-spark'/rid
            scratch.mkdir(parents=True,exist_ok=False)
            spark_config = dict(old['spark_config'], **{'spark.local.dir':str(scratch), 'spark.driver.extraClassPath':cp, 'spark.executor.extraClassPath':cp})
            receipt['spark_config'] = spark_config
            builder = SparkSession.builder.master(config['master']).appName('BigData-M6-FrozenTrain')
            for k,v in spark_config.items(): builder = builder.config(k,v)
            spark = builder.getOrCreate(); spark.sparkContext.setLogLevel('WARN')
            receipt['environment'] = dict(python=sys.version,spark=spark.version,
                scala=spark.sparkContext._jvm.scala.util.Properties.versionNumberString(),
                java=spark.sparkContext._jvm.java.lang.System.getProperty('java.version'),mongodb=client.server_info()['version'],
                jvm_input_arguments=list(spark.sparkContext._jvm.java.lang.management.ManagementFactory.getRuntimeMXBean().getInputArguments()),
                jvm_max_heap_bytes=spark.sparkContext._jvm.java.lang.Runtime.getRuntime().maxMemory(),
                packages={n:importlib.metadata.version(n) for n in ('pyspark','pymongo','numpy','psutil')})
            check('-Xss4m' in receipt['environment']['jvm_input_arguments']
                and receipt['environment']['jvm_max_heap_bytes'] == 768*1024**2,'JVM_ACTUAL_STACK_HEAP')
            step('source_validation_mongo_train_spark_start')
            spark.sparkContext.setJobGroup(rid,'M6 frozen train fit/extraction',interruptOnCancel=True)
            expired = threading.Event()
            def cancel():
                expired.set(); spark.sparkContext.cancelJobGroup(rid)
            timer = threading.Timer(config['max_job_seconds'],cancel); timer.daemon=True; timer.start()
            frame = spark.createDataFrame([(b['items'],) for b in train],
                T.StructType([T.StructField('items',T.ArrayType(T.StringType(),False),False)])).repartition(config['num_partitions']).cache()
            check(frame.count() == len(train),'SPARK_TRAIN_COUNT')
            model = FPGrowth(itemsCol='items',minSupport=config['min_support'],minConfidence=config['min_confidence'],
                numPartitions=config['num_partitions']).fit(frame)
            step('train_materialize_fit')
            itemsets,rules = checked_model(model,train,catalog,config,receipt)
            check(not expired.is_set(),'MODEL_TIME_LIMIT'); timer.cancel()
            step('extract_and_independent_all_counts')
            # Spark is shut down before new output becomes publishable or test is opened.
            spark.stop(); spark=None
            predictions,development = evaluate(queries,rules,catalog,int(PROTOCOL['k']))
            receipt.update(counts=dict(train_baskets=len(train),train_items=len(catalog),itemsets=len(itemsets),rules=len(rules),eligible_dev_queries=len(queries)),
                development=development,new_items=dict(targets=sum(r['new_target'] for r in predictions), queries_with_new_context=sum(bool(r['new_context']) for r in predictions), context_occurrences=sum(len(r['new_context']) for r in predictions)))
            jsonl(path/'dev-predictions.jsonl',predictions)
            outputs = output_docs(rid,catalog,itemsets,rules,len(train))
            for name,rows in outputs.items(): jsonl(path/f'{name}.jsonl',rows)
            receipt['output_validation'] = write_readback(db,outputs,rid)
            check(receipt['output_validation'] == frozen['output_validation'],'EXACT_FROZEN_MODEL_PARITY_BEFORE_TEST')
            check(development == old['development'],'DEVELOPMENT_PARITY_BEFORE_TEST')
            check_ready_snapshot(db,before)
            step('development_mongo_outputs_frozen_parity')
            receipt['elapsed_seconds'] = time.monotonic()-start
            complete(db,path,receipt)
            print(canonical({'run_id':rid,'status':'PASS','test_access':'NOT_OPENED'}),flush=True)
        except Exception as exc:
            fail_unfinished(db,path,receipt,exc)
            raise
        finally:
            if timer: timer.cancel()
            if spark: spark.stop()


if __name__ == '__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--session',required=True,type=Path);p.add_argument('--preparation',required=True,type=Path)
    a=p.parse_args();main(a.session.resolve(),a.preparation.resolve())
