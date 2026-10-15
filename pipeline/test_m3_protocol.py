"""Independent expectations for split/mask/metrics/ranking and train-only names."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import unittest

from m3_protocol import (PROTOCOL, RuleIndex, baseline, baseline_order, catalog_from_counts,
                         evaluate, mask, metrics, split_name, validate_rule)


class M3ProtocolTest(unittest.TestCase):
    def test_shared_independent_ranking_cases(self):
        fixture = json.loads(Path(__file__).with_name('m3_ranking_cases.json').read_text(encoding='utf-8'))
        for case in fixture['cases']:
            with self.subTest(case=case['name']):
                for rules in (case['rules'], list(reversed(case['rules']))):
                    answer = RuleIndex(rules).recommend(case['query'], case['k'])
                    self.assertEqual(case['expected'], [r['consequent'] for r in answer])
                    if 'best_antecedents' in case:
                        self.assertEqual(case['best_antecedents'], [r['antecedent'] for r in answer])

    def test_temporal_half_open_boundaries(self):
        self.assertEqual('train', split_name('2011-06-30T23:59:59'))
        self.assertEqual('dev', split_name('2011-07-01T00:00:00'))
        self.assertEqual('test', split_name('2011-10-01T00:00:00'))
        for t in ['2009-11-30T23:59:59','2011-12-10T00:00:00']:
            with self.assertRaisesRegex(RuntimeError, 'TIME_OUTSIDE_SPLIT'):
                split_name(t)

    def test_mask_independent_of_order_partition_or_duplicates(self):
        # Golden result pins SHA-256/version/seed/canonical encoding, not RNG order.
        expected = (['A','C','D'], 'B')
        self.assertEqual(expected, mask('INVOICE-0001', ['A','B','C','D']))
        self.assertEqual(expected, mask('INVOICE-0001', ['D','B','C','A','B']))
        self.assertEqual(3, len(expected[0]))
        self.assertNotIn(expected[1], expected[0])
        self.assertEqual({'A','B','C','D'}, set(expected[0]+[expected[1]]))
        with self.assertRaisesRegex(RuntimeError, 'MASK_REQUIRES_TWO_ITEMS'):
            mask('ONE', ['A'])

    def test_metrics_hand_calculated_no_recommendation_and_new_target_retained(self):
        rows = [dict(target='B', rules=['B'], baseline=['A']),
                dict(target='NEW', rules=[], baseline=['A']),
                dict(target='C', rules=['D'], baseline=['C'])]
        r, b = metrics(rows, 'rules'), metrics(rows, 'baseline')
        self.assertEqual((3, 1, 2, 1/3, 2/3), (r['queries'],r['hits'],r['with_recommendations'],r['recall_at_k'],r['recommendation_rate']))
        self.assertEqual((1/3, 1), (b['recall_at_k'],b['recommendation_rate']))
        self.assertEqual({'status':'NOT_APPLICABLE','queries':0,'hits':0,'with_recommendations':0,
                          'recall_at_k':None,'recommendation_rate':None}, metrics([], 'rules'))

    def test_no_rules_evaluation_uses_all_queries_including_unknown(self):
        catalog = [dict(stock_code='A', train_basket_count=5)]
        rows, result = evaluate([dict(query=['NEW_CONTEXT'], target='NEW_TARGET', invoice='1')], [], catalog, 5)
        self.assertTrue(rows[0]['new_target'])
        self.assertEqual(['NEW_CONTEXT'], rows[0]['new_context'])
        self.assertEqual(1, result['all']['rules']['queries'])
        self.assertEqual(0, result['all']['rules']['recall_at_k'])
        self.assertEqual(1, result['all']['baseline']['recommendation_rate'])

    def test_catalog_modal_description_tie_unicode_and_baseline_counts(self):
        names = defaultdict(Counter, {'A':Counter({'Name Z':2,'Name A':2}), 'B':Counter({'Title':3})})
        catalog = catalog_from_counts({'A':2,'B':4,'C':2}, names)
        self.assertEqual(['Name A','Title','C'], [r['display_name'] for r in catalog])
        ordered = baseline_order(catalog)
        self.assertEqual(['B','A','C'], ordered)
        self.assertEqual(['A','C'], baseline(['B'], ordered, 5))
        self.assertEqual([], baseline(ordered, ordered, 5))

    def test_invalid_rules_rejected_without_weakening_contract(self):
        valid = dict(antecedent=['A'], consequent='C', confidence=.7, lift=2., support=.2)
        for change in [dict(lift=float('nan')),dict(confidence=1.1),dict(support=0),
                       dict(antecedent=['B','A']),dict(antecedent=['A','A']),dict(consequent='A')]:
            with self.assertRaises(RuntimeError):
                validate_rule(dict(valid, **change))


if __name__ == '__main__':
    unittest.main()
