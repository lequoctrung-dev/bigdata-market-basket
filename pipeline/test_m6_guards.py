"""M6 isolation/identity/recovery tests; never write a real database or claim runtime TV2."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

import m6_common
from m6_publish import recover
from m6_common import ready_snapshot, check_ready_snapshot
import m6_source
import m6_preprocess
import m6_prepare
import m6_model
import m6_evaluate


class M6GuardsTest(unittest.TestCase):
    def test_all_stage_destinations_are_isolated_from_historical_db(self):
        for module in (m6_source,m6_preprocess,m6_prepare,m6_model,m6_evaluate):
            self.assertEqual('bigdata_m6',module.DATABASE,module.__name__)

    def test_copied_session_from_other_machine_is_rejected_before_reference_or_db(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); session=root/'artifacts/m6/TV1/session'
            session.mkdir(parents=True)
            (session/'session.json').write_text(json.dumps(dict(database='bigdata_m6',machine_id='other-machine')))
            with patch.object(m6_common,'ROOT',root), patch.object(m6_common,'machine_identity',return_value='current-machine'), \
                 patch.object(m6_common,'reference') as reference:
                with self.assertRaisesRegex(RuntimeError,'M6_SESSION_MACHINE_DB'):
                    m6_common.context(session)
                reference.assert_not_called()

    def test_recovery_never_mutates_or_increments_version(self):
        before=dict(run_id='old',version=1); target=dict(run_id='new',version=2)
        intent=dict(intent_id='i',before=before,target=target)
        db=Mock()
        for actual,expected in [(before,'NOT_APPLIED'),(target,'APPLIED'),(dict(run_id='third',version=3),'CONFLICT')]:
            db.publication.find_one.return_value=actual
            self.assertEqual(expected,recover(db,intent)['status'])
        db.publication.replace_one.assert_not_called()
        db.publication.insert_one.assert_not_called()

    def test_ready_protection_rejects_payload_or_pointer_changes(self):
        before=dict(pointer=dict(run_id='old',version=1),runs={'old':'hash'},outputs={'old':{'items':'hash'}})
        db=Mock()
        with patch.object(m6_common,'ready_snapshot',return_value=dict(before,pointer=dict(run_id='new',version=2))):
            with self.assertRaisesRegex(RuntimeError,'M6_UNEXPECTED_PUBLICATION_MUTATION'):
                check_ready_snapshot(db,before)
        with patch.object(m6_common,'ready_snapshot',return_value=dict(before,outputs={'old':{'items':'changed'}})):
            with self.assertRaisesRegex(RuntimeError,'M6_OLD_READY_CHANGED'):
                check_ready_snapshot(db,before)


if __name__=='__main__': unittest.main()
