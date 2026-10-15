"""Kiểm tra quy ước nguồn/đáp án độc lập, không giả thành Spark runtime."""
import unittest
from sample_fixture import fixture_rows, make_row, tuple_key, reference_itemsets, is_excluded


class FixtureTest(unittest.TestCase):
    def test_numbers_equal_by_value_text_and_whitespace_distinct(self):
        first = make_row("0001", "SKU_A")
        numeric = make_row("0001", "SKU_A", quantity="1.0")
        self.assertEqual(tuple_key(first["source_cells"]), tuple_key(numeric["source_cells"]))
        numeric["source_cells"][3] = {"type": "text", "value": "1"}
        self.assertNotEqual(tuple_key(first["source_cells"]), tuple_key(numeric["source_cells"]))
        spaced = make_row("0001", "SKU_A ")
        self.assertNotEqual(tuple_key(first["source_cells"]), tuple_key(spaced["source_cells"]))

    def test_qty_difference_retained_and_two_duplicates_only(self):
        rows = fixture_rows()
        self.assertEqual(22, len(rows))
        self.assertEqual(20, len({tuple_key(r["source_cells"]) for r in rows}))
        self.assertNotEqual(tuple_key(make_row("0001", "SKU_A")["source_cells"]),
                            tuple_key(make_row("0001", "SKU_A", quantity="2")["source_cells"]))

    def test_exclusions_preserve_alphabetic_merchandise(self):
        for code in ["B", "POST", "m", "gift_0001_10", "TEST001", "TEST002"]:
            self.assertTrue(is_excluded(code))
        for code in ["SKU_A", "SKU_B", "SKU_C", "PADS", "SP1002"]:
            self.assertFalse(is_excluded(code))

    def test_independent_hand_counts(self):
        counts = reference_itemsets()
        self.assertEqual(4, counts[("SKU_A",)])
        self.assertEqual(3, counts[("SKU_B",)])
        self.assertEqual(3, counts[("SKU_A", "SKU_B")])
        self.assertEqual(2, counts[("SKU_A", "SKU_B", "SKU_C")])


if __name__ == "__main__":
    unittest.main()
