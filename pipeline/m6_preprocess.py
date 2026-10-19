"""M6 preprocessing in bigdata_m6; reuse frozen pure transforms, preserve old READY."""

import argparse
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid
import psutil

from pymongo import MongoClient
from pyspark import StorageLevel
from pyspark.sql import SparkSession, Window, functions as F, types as T

from m2_source import (ROOT, SOURCE, SOURCE_HASH, SCHEMA, PARSER, POLICY,
                       canonical, digest, check, immutable_batch, save, document)
from m2_runtime import verify_owned_mongo, writer_lock, require_ready, bson_counts, STORAGE_VERSION


from m2_pipeline import source_schema, first_rows, verify_typed_fixture, normalize, quality_flags, position_checksum, write_immutable_frames
from m6_common import URI, DATABASE, context, ready_snapshot, check_ready_snapshot, postcheck_preprocessing


def read_source(spark, reverse=False):
    pipeline = [{'$match': {'dataset_id': SOURCE_HASH}}]
    if reverse:
        pipeline.append({'$sort': {'sheet_index': -1, 'source_row': -1}})
    return (spark.read.format('mongodb').option('connection.uri', URI).option('database', DATABASE)
            .option('collection', 'source_rows').option('mode', 'FAILFAST')
            .option('partitioner', 'com.mongodb.spark.sql.connector.read.partitioner.SinglePartitionPartitioner')
            .option('aggregation.pipeline', canonical(pipeline)).schema(source_schema()).load())


def build(args):
    OUT = args.session
    audit_path = args.session / 'audit/audit.json'
    audit = json.loads(audit_path.read_text(encoding='utf-8'))
    check(audit['source_sha256'] == SOURCE_HASH and audit['policy'] == POLICY, 'AUDIT_POLICY_SOURCE')
    q_precision = audit['integer_digits']['Quantity']
    price_scale = audit['scale']['Price']
    price_precision = audit['integer_digits']['Price'] + price_scale
    check(audit['scale']['Quantity'] == 0, 'NONINTEGER_QUANTITY_REVIEW_REQUIRED')
    product_precision = q_precision + price_precision + 1
    check(product_precision <= 38, 'DECIMAL_PRODUCT_PRECISION_REVIEW_REQUIRED')
    check(product_precision + math.ceil(math.log10(audit['counts']['raw'])) <= 38,
          'DECIMAL_SUM_PRECISION_REVIEW_REQUIRED')
    basket_set = digest([SOURCE_HASH, PARSER, SCHEMA, STORAGE_VERSION, digest(POLICY), 'merchandise'])
    run = str(uuid.uuid4())
    output = args.session / 'processed' / run
    output.mkdir(parents=True, exist_ok=False)
    receipt = {'milestone': 'M6', 'mode': 'FULL_SOURCE', 'stage': 'PREPROCESSING', 'status': 'RUNNING',
               'machine_role': args.machine_role,
               'run_id': run, 'basket_set_id': basket_set, 'dataset_id': SOURCE_HASH,
               'schema_version': SCHEMA, 'parser_version': PARSER, 'policy': POLICY, 'policy_hash': digest(POLICY),
               'storage_encoding_version': STORAGE_VERSION,
               'started_at_utc': datetime.now(timezone.utc).isoformat(), 'checks': {}, 'steps_seconds': {},
               'code_revision': subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip(),
               'code_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in
                               [Path(__file__), Path(__file__).with_name('m2_pipeline.py'), Path(__file__).with_name('m2_source.py'), Path(__file__).with_name('m2_runtime.py'), Path(__file__).with_name('m6_common.py')]},
               'audit_sha256': hashlib.sha256(audit_path.read_bytes()).hexdigest(),
               'output_directory': str(output.relative_to(ROOT)), 'publication': 'NOT_ATTEMPTED',
               'model': 'NOT_RUN', 'split': 'NOT_SET_M3', 'human_review': 'PENDING_TV2'}
    spark = None
    state, _ = context(args.session)
    receipt.update(database=DATABASE, machine_id=state['machine_id'])
    client = MongoClient(URI)
    db = client[DATABASE]
    protected = ready_snapshot(db)
    started = time.monotonic()
    stage_start_utc = datetime.now(timezone.utc).isoformat()
    def step(name):
        nonlocal started, stage_start_utc
        receipt['steps_seconds'][name] = time.monotonic()-started
        receipt.setdefault('step_measurements', {})[name] = {
            'started_at_utc': stage_start_utc, 'finished_at_utc': datetime.now(timezone.utc).isoformat(),
            'disk_end_bytes': {folder: sum(p.stat().st_size for p in (ROOT / folder).rglob('*') if p.is_file())
                               for folder in [f'tmp/m6-spark/{run}', str(output.relative_to(ROOT)), 'artifacts/m2/mongo-data']}}
        started = time.monotonic()
        stage_start_utc = datetime.now(timezone.utc).isoformat()
        print(canonical({'step': name, 'seconds': receipt['steps_seconds'][name]}), flush=True)
        save(OUT / f'pipeline-{run}.json', receipt)
    try:
        receipt['available_ram_before_bytes'] = psutil.virtual_memory().available
        check(receipt['available_ram_before_bytes'] >= 1024**3, 'AVAILABLE_RAM_OPERATIONAL_GUARD')
        metadata = require_ready(db, SOURCE_HASH)
        check(db.source_rows.count_documents({'dataset_id': SOURCE_HASH}) == audit['counts']['raw'], 'SOURCE_COUNT')
        db.runs.insert_one({'_id': run, 'run_id': run, 'dataset_id': SOURCE_HASH, 'basket_set_id': basket_set,
                            'schema_version': SCHEMA, 'mode': 'FULL_SOURCE', 'stage': 'PREPROCESSING',
                            'status': 'WRITING', 'basket_set_status': 'WRITING'})
        os.environ['PYSPARK_PYTHON'] = sys.executable
        os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
        os.environ.setdefault('SPARK_LOCAL_IP', '127.0.0.1')
        jars = sorted((ROOT / 'tmp/connector').glob('*.jar'))
        expected = {'mongo-spark-connector_2.13-11.1.0.jar', 'mongodb-driver-sync-5.1.4.jar',
                    'mongodb-driver-core-5.1.4.jar', 'bson-5.1.4.jar', 'bson-record-codec-5.1.4.jar'}
        check({p.name for p in jars} == expected, 'CONNECTOR_JARS')
        receipt['jars_sha256'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in jars}
        classpath = os.pathsep.join(str(p) for p in jars)
        scratch = ROOT / 'tmp/m6-spark' / run
        scratch.mkdir(parents=True, exist_ok=False)
        config = {'spark.driver.memory': '1280m', 'spark.sql.shuffle.partitions': '16',
                  'spark.default.parallelism': '2', 'spark.ui.enabled': 'false',
                  'spark.sql.adaptive.coalescePartitions.enabled': 'false',
                  'spark.driver.bindAddress': '127.0.0.1', 'spark.driver.extraClassPath': classpath,
                  'spark.executor.extraClassPath': classpath, 'spark.local.dir': str(scratch),
                  'spark.sql.ansi.enabled': 'true', 'spark.sql.decimalOperations.allowPrecisionLoss': 'false'}
        builder = SparkSession.builder.master('local[2]').appName('BigData-M6-FullSource')
        for key, value in config.items():
            builder = builder.config(key, value)
        spark = builder.getOrCreate()
        spark.sparkContext.setLogLevel('WARN')
        receipt['config'] = config
        receipt['environment'] = {'spark': spark.version, 'scala': spark.sparkContext._jvm.scala.util.Properties.versionNumberString(),
            'mongodb': client.server_info()['version'], 'python': sys.version,
            'java': subprocess.run(['java','-version'], capture_output=True, text=True).stderr.strip(),
            'packages': {n: importlib.metadata.version(n) for n in ['pyspark','pymongo','openpyxl','psutil']}}
        verify_typed_fixture(spark)
        receipt['checks']['typed_tuple_quantity_price_null_whitespace_case_date_fixture'] = True
        step('startup')
        source = read_source(spark).persist(StorageLevel.DISK_ONLY)
        check(source.count() == audit['counts']['raw'], 'SPARK_RAW_COUNT')
        step('mongo_read')
        retained = first_rows(source, 8).persist(StorageLevel.DISK_ONLY)
        retained_count = retained.count()
        check(retained_count == audit['counts']['retained'] == 1033036, 'P01_COUNT')
        checksum = position_checksum(retained)
        check(checksum == audit['retained_position_checksum'], 'P01_REFERENCE_LINEAGE')
        # Complete second pass: reversed Mongo order and a different partition count.
        alternate = first_rows(read_source(spark, reverse=True), 13)
        check(alternate.count() == retained_count and position_checksum(alternate) == checksum, 'P01_PARTITION_STABILITY')
        receipt['checks']['p01_full_count_lineage_reverse_partitions_8_13'] = True
        receipt['retained_position_checksum'] = checksum
        source.unpersist()
        step('p01_and_stability')
        lines = normalize(retained, q_precision, price_precision, price_scale).persist(StorageLevel.DISK_ONLY)
        flags = quality_flags(lines)
        quality = lines.agg(*[F.sum(F.coalesce(expr, F.lit(False)).cast('long')).alias(name)
                              for name, expr in flags.items()]).first().asDict()
        for name, value in quality.items():
            check(value == audit['overlapping_retained_quality'][name], f'QUALITY_{name}')
        valid = F.lit(True)
        for name, expr in list(flags.items())[:8]:
            valid = valid & ~F.coalesce(expr, F.lit(False))
        positive = lines.filter(valid)
        positive_count = positive.count()
        positive_value = positive.agg(F.sum(F.col('quantity')*F.col('price'))).first()[0]
        check(positive_count == audit['counts']['positive_valid'], 'POSITIVE_COUNT')
        check(positive_value == Decimal(audit['positive_value_gbp']), 'POSITIVE_MONEY')
        exclusion = F.upper('stock_code').isin(POLICY['excluded']) | F.lower('stock_code').startswith('gift_')
        merchandise = positive.filter(~exclusion).withColumn('line_value', F.col('quantity')*F.col('price')).persist(StorageLevel.DISK_ONLY)
        product_type = merchandise.schema['line_value'].dataType
        check(product_type.scale == price_scale, 'PRODUCT_SCALE_LOSS')
        receipt['decimal_types'] = {'quantity': f'decimal({q_precision},0)',
            'price': f'decimal({price_precision},{price_scale})', 'product': product_type.simpleString(),
            'sum': merchandise.select(F.sum('line_value')).schema.simpleString()}
        count = merchandise.count()
        total = merchandise.agg(F.sum('line_value')).first()[0]
        check(count == audit['counts']['merchandise'], 'MERCHANDISE_COUNT')
        check(total == Decimal(audit['merchandise_value_gbp']), 'EXACT_MONEY_TOTAL')
        missing_customer = merchandise.filter(F.col('customer_id').isNull() | (F.col('customer_id') == '')).count()
        check(missing_customer == audit['counts']['merchandise_missing_customer'], 'CUSTOMER_NOT_DROPPED')
        excluded_counts = {r.stock_code: r['count'] for r in positive.filter(exclusion).groupBy('stock_code').count().collect()}
        check(excluded_counts == audit['excluded_positive_rows'], 'EXCLUDED_MAPPING_COUNTS')
        receipt['counts'] = {'raw': audit['counts']['raw'], 'duplicates': audit['counts']['raw']-retained_count,
            'retained': retained_count, 'invalid_or_nonpositive': retained_count-positive_count,
            'positive_valid': positive_count, 'excluded': positive_count-count, 'merchandise': count,
            'merchandise_missing_customer': missing_customer}
        receipt.update(overlapping_retained_quality=quality, excluded_positive_rows=excluded_counts,
                       merchandise_value_gbp=str(total), positive_value_gbp=str(positive_value))
        receipt['checks']['quality_p02_counts_customer_and_exact_money'] = True
        step('quality_and_p02')
        # Preserve all retained line values + lineage, including reasons for exclusion.
        export = (lines.withColumn('positive_valid', valid)
                  .withColumn('p02_excluded', F.coalesce(exclusion, F.lit(False)))
                  .withColumn('line_value', (F.col('quantity')*F.col('price')).cast('string'))
                  .withColumn('quantity', F.col('quantity').cast('long'))
                  .withColumn('price', F.col('price').cast('string')).drop('parsed_time'))
        line_path = output / 'retained-lines.jsonl'
        line_hash = hashlib.sha256()
        exported = 0
        with line_path.open('wb') as stream:
            for row in export.toLocalIterator():
                encoded = (canonical(row.asDict())+'\n').encode()
                stream.write(encoded)
                line_hash.update(encoded)
                exported += 1
        check(exported == retained_count, 'LINE_EXPORT_COUNT')
        receipt['line_output'] = {'rows': exported, 'sha256': line_hash.hexdigest(), 'bytes': line_path.stat().st_size,
                                  'order': 'Spark partition order; lineage explicit; byte hash is attempt-specific'}
        step('line_export')
        baskets = merchandise.groupBy('invoice').agg(F.sort_array(F.collect_set('stock_code')).alias('items'),
            F.min('invoice_time_local').alias('invoice_time_local'), F.count('*').alias('retained_line_count'),
            F.sum('line_value').alias('line_value'),
            *[expr for column in ['invoice_time_local', 'customer_id', 'country'] for expr in
              [F.min(column).alias(column+'_min'), F.max(column).alias(column+'_max')]])
        basket_docs, basket_hash, size_dist = [], hashlib.sha256(), Counter()
        month_values = {}
        for row in baskets.orderBy('invoice').toLocalIterator():
            items = list(row.items)
            check(items == sorted(set(items)), 'BASKET_UNIQUE_SORTED')
            basket_hash.update((canonical([row.invoice, items, row.invoice_time_local, row.retained_line_count])+'\n').encode())
            size_dist[len(items)] += 1
            month = row.invoice_time_local[:7]
            bucket = month_values.setdefault(month, {'invoices': 0, 'lines': 0, 'line_value_gbp': Decimal(0)})
            bucket['invoices'] += 1
            bucket['lines'] += row.retained_line_count
            bucket['line_value_gbp'] += row.line_value
            basket_docs.append({'_id': canonical([basket_set, row.invoice]), 'basket_set_id': basket_set,
                'invoice': row.invoice, 'items': items, 'invoice_time_local': row.invoice_time_local,
                'retained_line_count': row.retained_line_count,
                'quality_flags': {'multi_timestamp': row.invoice_time_local_min != row.invoice_time_local_max,
                                  'multi_day': row.invoice_time_local_min[:10] != row.invoice_time_local_max[:10],
                                  'multi_customer': row.customer_id_min != row.customer_id_max,
                                  'multi_country': row.country_min != row.country_max}})
        check(len(basket_docs) == audit['basket_count'] and basket_hash.hexdigest() == audit['basket_checksum'], 'BASKET_REFERENCE')
        check({str(k): v for k, v in size_dist.items()} == audit['size_distribution'], 'BASKET_DISTRIBUTION')
        for month, value in month_values.items():
            value['line_value_gbp'] = str(value['line_value_gbp'])
            check(all(Decimal(str(v)) == Decimal(str(audit['monthly'][month][k])) for k, v in value.items()), 'MONTH_REFERENCE')
        item_reference = json.loads((args.session / 'audit/item-reference.json').read_text(encoding='utf-8'))
        item_values = merchandise.groupBy('stock_code').agg(F.count('*').alias('rows'), F.sum('quantity').alias('quantity'),
            F.countDistinct('invoice').alias('baskets'), F.sum('line_value').alias('line_value_gbp')).collect()
        check(len(item_values) == audit['item_count'], 'ITEM_COUNT')
        summaries = []
        def summary(kind, key, payload):
            return {'_id': canonical([basket_set, 'merchandise', kind, key]), 'basket_set_id': basket_set,
                'scope': 'merchandise', 'summary_type': kind, 'bucket_key': key, 'payload': payload,
                'denominator_baskets': len(basket_docs), 'policy_hash': digest(POLICY),
                'definition_version': 'm2-all-period-not-train-v1'}
        for row in item_values:
            ref = item_reference[row.stock_code]
            check(all(Decimal(str(row[k])) == Decimal(str(v)) for k, v in ref.items()), 'ITEM_REFERENCE')
            summaries.append(summary('item', row.stock_code, {'rows': row.rows, 'quantity': int(row.quantity),
                'baskets': row.baskets, 'line_value_gbp': str(row.line_value_gbp)}))
        summaries.extend(summary('month', month, value) for month, value in sorted(month_values.items()))
        summaries.extend(summary('basket_size', str(size), {'baskets': frequency}) for size, frequency in sorted(size_dist.items()))
        summaries.append({'_id': canonical([basket_set, 'raw', 'quality', 'all']), 'basket_set_id': basket_set,
            'scope': 'raw', 'summary_type': 'quality', 'bucket_key': 'all',
            'payload': {'stage_counts': receipt['counts'], 'overlapping_retained_quality': quality,
                        'overlapping_quality_scope': 'p01_retained', 'excluded_positive_rows': excluded_counts,
                        'excluded_scope': 'positive_valid'},
            'denominators': {'raw': audit['counts']['raw'], 'p01_retained': retained_count, 'positive_valid': positive_count},
            'policy_hash': digest(POLICY), 'definition_version': 'm2-quality-explicit-scopes-v1'})
        step('baskets_and_summaries_reference')
        db.baskets.create_index([('basket_set_id', 1), ('invoice', 1)], unique=True)
        db.summaries.create_index([('basket_set_id', 1), ('scope', 1), ('summary_type', 1), ('bucket_key', 1)], unique=True)
        write_immutable_frames(db, 'baskets', iter(basket_docs))
        write_immutable_frames(db, 'summaries', iter(summaries))
        # Retry full basket output through exact-payload comparison, without updates.
        write_immutable_frames(db, 'baskets', iter(basket_docs))
        check(db.baskets.count_documents({'basket_set_id': basket_set}) == len(basket_docs), 'BASKET_DB_COUNT')
        check(db.summaries.count_documents({'basket_set_id': basket_set}) == len(summaries), 'SUMMARY_DB_COUNT')
        check(db.baskets.count_documents({'basket_set_id': basket_set,
              'retained_line_count': {'$type': 'long'}}) == len(basket_docs), 'BASKET_COUNT_BSON_LONG')
        check(db.summaries.count_documents({'basket_set_id': basket_set, 'summary_type': 'item',
              **{f'payload.{name}': {'$type': 'long'} for name in ['rows', 'quantity', 'baskets']}})
              == len(item_values), 'ITEM_COUNTS_BSON_LONG')
        check_ready_snapshot(db, protected)
        receipt['counts'].update(baskets=len(basket_docs), items=len(item_values), summaries=len(summaries),
                                 single_item_baskets=size_dist[1], multi_item_baskets=len(basket_docs)-size_dist[1])
        receipt.update(basket_checksum=basket_hash.hexdigest(),
                       size_distribution={str(k): v for k, v in sorted(size_dist.items())}, monthly=month_values)
        receipt['checks']['basket_items_monthly_reference_and_immutable_retry'] = True
        receipt['checks']['actual_bson_int64_counts'] = True
        step('mongo_output_validation')
        receipt['status'] = 'PASS'
        receipt['database'] = DATABASE
        receipt['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
        # VALIDATED is a preprocessing checkpoint; no READY model/run or active pointer.
        check(db.runs.update_one({'_id': run, 'status': 'WRITING'}, {'$set': {'status': 'VALIDATED',
            'basket_set_status': 'READY', 'manifest': bson_counts(receipt)}}).modified_count == 1, 'M6_PREPROCESSING_STATE')
        postcheck_preprocessing(db, receipt)
        save(OUT / f'final-verification-{run}.json', dict(status='PASS', run_id=run, basket_set_id=basket_set, verified_at_utc=datetime.now(timezone.utc).isoformat(), scope='M6_READ_ONLY_STAGE_POSTCHECK_NO_LEGACY_INVALIDATION'))
    except Exception as exc:
        receipt.update(status='FAIL', error_type=type(exc).__name__)
        db.runs.update_one({'_id': run, 'status': {'$in': ['WRITING','VALIDATED']}}, {'$set': {'status': 'FAILED',
                            'basket_set_status': 'INCOMPLETE', 'error_type': type(exc).__name__}})
        raise
    finally:
        save(OUT / f'pipeline-{run}.json', receipt)
        if spark is not None:
            spark.stop()
        client.close()
        print(canonical({'run_id': run, 'status': receipt['status']}), flush=True)



if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--session', required=True, type=Path)
    args=parser.parse_args();args.session=args.session.resolve()
    state,_=context(args.session);args.machine_role=state['machine_role']
    verify_owned_mongo()
    with writer_lock():
        build(args)
