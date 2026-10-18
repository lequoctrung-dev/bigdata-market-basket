"""Validate FINAL harness using synthetic/dev data only, before first test access."""
import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock
from m3_protocol import PROTOCOL, evaluate, mask
from m5_evaluate import final_queries, independent_predictions, arithmetic
from m5_common import fail_unfinished


class FinalHarnessTest(unittest.TestCase):
    def test_single_basket_excluded_unknown_and_no_rule_kept(self):
        baskets=[dict(invoice='one',invoice_time_local='2011-10-01T00:00:00',items=['A']),
                 dict(invoice='two',invoice_time_local='2011-10-01T00:00:01',items=['NEW','A'])]
        queries=final_queries(baskets)
        self.assertEqual(1,len(queries))
        self.assertEqual(set(['A','NEW']),set(queries[0]['query']+[queries[0]['target']]))
        rows,metrics=evaluate(queries,[],[dict(stock_code='A',train_basket_count=1)],5)
        self.assertEqual(rows,independent_predictions(queries,[],[dict(stock_code='A',train_basket_count=1)],5))
        self.assertEqual(1,metrics['all']['rules']['queries'])
        self.assertEqual(0,arithmetic(rows)['rules']['with_recommendations'])

    def test_exhaustive_ranking_matches_best_rule_and_baseline(self):
        rules=[dict(antecedent=['A'],consequent='B',support=.2,confidence=.7,lift=2.,rule_key='one'),
               dict(antecedent=['A','C'],consequent='B',support=.2,confidence=.8,lift=2.,rule_key='best'),
               dict(antecedent=['C'],consequent='D',support=.1,confidence=.6,lift=1.,rule_key='three')]
        catalog=[dict(stock_code=c,train_basket_count=n) for c,n in [('A',5),('B',4),('C',3),('D',1)]]
        queries=[dict(invoice='i',query=['A','C'],target='B'),dict(invoice='j',query=['UNKNOWN'],target='NEW')]
        actual=independent_predictions(queries,rules,catalog,5)
        self.assertEqual(evaluate(queries,rules,catalog,5)[0],actual)
        self.assertEqual(['best','three'],actual[0]['rule_keys'])
        self.assertEqual(dict(queries=2,hits=1,with_recommendations=1),arithmetic(actual)['rules'])

    def test_empty_keeps_null_metrics(self):
        self.assertEqual([],independent_predictions([],[],[],5))
        self.assertIsNone(evaluate([],[],[],5)[1]['all']['rules']['recall_at_k'])

    def test_late_error_never_rewrites_ready_receipt(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder);(path/'receipt.json').write_text('immutable-ready-receipt',encoding='utf-8')
            db=Mock();db.runs.find_one.return_value={'status':'READY'}
            fail_unfinished(db,path,{'run_id':'ready'},BrokenPipeError('late stdout failure'))
            self.assertEqual('immutable-ready-receipt',(path/'receipt.json').read_text(encoding='utf-8'))
            db.runs.update_one.assert_not_called()
            self.assertEqual(1,len(list(path.glob('failure-incident-*.json'))))


if __name__=='__main__': unittest.main()
