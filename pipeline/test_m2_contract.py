"""Regression boundaries for full-source M2, not counts copied from its code."""
import unittest
from copy import deepcopy
from datetime import datetime
from decimal import Decimal

from m2_source import encode_cell, tuple_key, identifier, excluded, immutable_batch, document
from m2_runtime import bson_counts
from bson import BSON
from bson.int64 import Int64


class MemoryCollection:
    """Only the read branch is used to exercise READY conflict semantics."""
    def __init__(self, rows):
        self.rows = rows

    def find(self, query):
        return [row for row in self.rows if row['_id'] in query['_id']['$in']]


class TypedSourceContract(unittest.TestCase):
    def key(self, value):
        return tuple_key([encode_cell(value)])

    def test_actual_bson_counts_keep_long_bool_and_string_ids(self):
        # Round-trip real BSON; plain Python equality hides int32 vs int64.
        decoded = BSON(BSON.encode(bson_counts({'count': 1, 'large': 2**40, 'rows': [{'n': 0}],
                                               'enabled': True, 'invoice': '0001'}))).decode()
        self.assertIsInstance(decoded['count'], Int64)
        self.assertIsInstance(decoded['large'], Int64)
        self.assertIsInstance(decoded['rows'][0]['n'], Int64)
        self.assertIs(type(decoded['enabled']), bool)
        self.assertEqual(decoded['invoice'], '0001')

    def test_numeric_equivalence_preserves_type_text_and_null(self):
        self.assertEqual(self.key(1), self.key(1.0))
        self.assertEqual(self.key(-0.0), self.key(0))
        for value in ['1', ' 1', '1 ', None, '', 'A', 'a']:
            self.assertNotEqual(self.key(1), self.key(value))
        self.assertNotEqual(self.key('A'), self.key('a'))
        self.assertNotEqual(self.key('A'), self.key(' A'))
        self.assertNotEqual(self.key(None), self.key(''))
        self.assertNotEqual(self.key(datetime(2010, 1, 1)), self.key('2010-01-01T00:00:00'))

    def test_tuple_boundaries_and_non_key_quantity_price(self):
        row = ('0001', 'A', 'name', 1, datetime(2010, 1, 1), 1.23456789, None, 'UK')
        first = document(0, 2, row)
        later = document(1, 200, row)
        self.assertEqual(first['tuple_key'], later['tuple_key'])
        self.assertNotEqual(first['_id'], later['_id'])
        for column in (3, 5):
            changed = list(row)
            changed[column] = 2
            self.assertNotEqual(first['tuple_key'], document(0, 3, changed)['tuple_key'])
        self.assertNotEqual(tuple_key([encode_cell('a,b'), encode_cell('c')]),
                            tuple_key([encode_cell('a'), encode_cell('b,c')]))

    def test_identifier_and_classification_boundaries(self):
        self.assertEqual(identifier(123.0), '123')
        self.assertEqual(identifier(' 00123a '), '00123a')
        self.assertIsNone(identifier(None))
        for code in ['post', 'ADJUST2', 'B', 'm', 'GIFT', 'gift_0001_10', 'TEST001', 'test002']:
            self.assertTrue(excluded(code), code)
        for code in ['PADS', 'DCGS0003', 'SP1002', '10000A', 'XYZ', 'gifted']:
            self.assertFalse(excluded(code), code)

    def test_ready_retry_never_fills_missing_or_overwrites(self):
        row = {'_id': 'source-1', 'source_cells': [{'type': 'text', 'value': ' original '}]}
        immutable_batch(MemoryCollection([deepcopy(row)]), [row], ready=True)
        with self.assertRaisesRegex(RuntimeError, 'SOURCE_PAYLOAD_CONFLICT'):
            immutable_batch(MemoryCollection([deepcopy(row)]), [dict(row, source_cells=[])], ready=True)
        with self.assertRaisesRegex(RuntimeError, 'READY_SOURCE_MISSING_ROW'):
            immutable_batch(MemoryCollection([]), [row], ready=True)

    def test_unsupported_numbers_and_booleans_are_not_coerced(self):
        for value in [True, float('nan'), float('inf'), Decimal('1')]:
            with self.assertRaises((ValueError, RuntimeError)):
                encode_cell(value)


if __name__ == '__main__':
    unittest.main()
