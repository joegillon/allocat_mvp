import unittest
import unittest.mock
from unittest.mock import patch
from tests.helpers import *
import globals as gbl
from models.ledger_dataset import LedgerDataSet
from presenters.import_presenter import ImportPresenter
import tests.ledger_data.test_db as test_db
import tests.ledger_data.test_salary_import as test_xl_data
import tests.ledger_data.test_data as test_data


class TestImportPresenter(unittest.TestCase):

    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None)

        gbl.COLOR_SCHEME = gbl.SKINS[gbl.pick_scheme()]

        with patch('dal.dao.Dao._Dao__read') as mock_db:
            mock_db.side_effect = [
                test_db.employees,
                test_db.all_departments,
                test_db.all_grant_admins,
                test_db.ledger_rex
            ]
            gbl.dataset = LedgerDataSet(None)

        self.presenter = ImportPresenter(self.frame)
        self.view = self.presenter.view

    def tearDown(self):
        self.frame.Destroy()
        self.app.Destroy()

    def testGetData(self):
        expected_items = sorted(test_xl_data.ss_rex, key=lambda k: k.name)
        expected_mismatches = {
            'EMPL 56': [('EMP 56', 92), ('EMP 15', 77), ('EMP 52', 77), ('EMP 61', 77), ('EMP 62', 77)],
            'EMPL 61': [('EMP 61', 92), ('EMP 15', 77), ('EMP 56', 77), ('EMP 62', 77), ('EMP 76', 77)],
            'VA EMP 73': [('EMP 73', 90), ('EMP 15', 86), ('EMP 20', 86), ('EMP 52', 86), ('EMP 56', 86)]
        }

        with patch('lib.excel_lib.get_file') as mock_get_file_dlg:
            mock_get_file_dlg.return_value = 'c:/bench/allocat/data/test_salary_notes.xls'
            click_button(self.view.import_btn)

        assertEqualListOfObjects(expected_items, self.view.list_ctrl.GetObjects())
        assert expected_mismatches.keys() == self.presenter.mismatches.keys()
        assert list(expected_mismatches.values()) == list(self.presenter.mismatches.values())

    def testLoadMismatchList_NoListOnMatch(self):
        with patch('lib.excel_lib.get_file') as mock_get_file_dlg:
            mock_get_file_dlg.return_value = 'c:/bench/allocat/data/test_salary_notes.xls'
            click_button(self.view.import_btn)

        # first item is a match
        click_list_ctrl(self.view.list_ctrl, 0)

        assert self.view.matches_ctrl.GetObjects() == []

    def testLoadMismatchList_NonMatch(self):
        with patch('lib.excel_lib.get_file') as mock_get_file_dlg:
            mock_get_file_dlg.return_value = 'c:/bench/allocat/data/test_salary_notes.xls'
            click_button(self.view.import_btn)

        expected = [
            {'name': 'EMP 73', 'score': 90},
            {'name': 'EMP 15', 'score': 86},
            {'name': 'EMP 20', 'score': 86},
            {'name': 'EMP 52', 'score': 86},
            {'name': 'EMP 56', 'score': 86}
        ]

        # last item is a mismatch
        click_list_ctrl(self.view.list_ctrl, 12)

        assert self.view.matches_ctrl.GetObjects() == expected

    def testMatch_NoSelection(self):
        with patch('lib.excel_lib.get_file') as mock_get_file_dlg:
            mock_get_file_dlg.return_value = 'c:/bench/allocat/data/test_salary_notes.xls'
            click_button(self.view.import_btn)

        click_list_ctrl(self.view.list_ctrl, 12)

        # No match list selection

        with patch('lib.ui_lib.show_error') as mock_popup:
            mock_popup.return_value = None
            with patch('models.employee.Employee.update_name') as mock_emp_update:
                click_button(self.view.match_btn)

        mock_popup.assert_called_once_with('No match selected!')
        mock_emp_update.assert_not_called()

    def testMatch_WrongSelection(self):
        with patch('lib.excel_lib.get_file') as mock_get_file_dlg:
            mock_get_file_dlg.return_value = 'c:/bench/allocat/data/test_salary_notes.xls'
            click_button(self.view.import_btn)

        click_list_ctrl(self.view.list_ctrl, 12)

        # Select not best match
        click_list_ctrl(self.view.matches_ctrl, 1)

        with patch('lib.ui_lib.confirm') as mock_popup:
            mock_popup.return_value = False
            with patch('models.employee.Employee.update_name') as mock_emp_update:
                click_button(self.view.match_btn)

        mock_popup.assert_called_once_with(self.view, 'Not the highest score! Are you sure?')
        mock_emp_update.assert_not_called()

    def testMatch_TopSelection(self):
        with patch('lib.excel_lib.get_file') as mock_get_file_dlg:
            mock_get_file_dlg.return_value = 'c:/bench/allocat/data/test_salary_notes.xls'
            click_button(self.view.import_btn)

        click_list_ctrl(self.view.list_ctrl, 12)

        # Select best match
        click_list_ctrl(self.view.matches_ctrl, 0)

        with patch('lib.ui_lib.show_error') as mock_err_popup:
            with patch('lib.ui_lib.confirm') as mock_confirm_popup:
                with patch('dal.dao.Dao._Dao__write') as mock_emp_update:
                    mock_emp_update.return_value = 1
                    click_button(self.view.match_btn)

        mock_err_popup.assert_not_called()
        mock_confirm_popup.assert_not_called()

        assert mock_emp_update.call_count == 1
        args, kwargs = mock_emp_update.call_args
        assert len(args) == 2
        assert len(kwargs) == 0
        assert args[0] == "UPDATE employees SET name=? WHERE name=?"
        assert args[1] == ('VA EMP 73', 'EMP 73')

        assertEqualObjects(self.view.list_ctrl.GetObjectAt(12), test_xl_data.matched_rec)