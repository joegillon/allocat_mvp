import unittest
import unittest.mock
from unittest.mock import patch
from tests.helpers import *
import globals as gbl
from models.ledger_dataset import LedgerDataSet
from presenters.import_presenter import ImportPresenter
import tests.ledger_data.test_salary_import as test_xl_data
import tests.ledger_data.test_data as test_data


class TestImportPresenter(unittest.TestCase):

    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None)

        gbl.COLOR_SCHEME = gbl.SKINS[gbl.pick_scheme()]
        gbl.DB_PATH = 'c:/bench/allocat/tests/allocat.db'

        gbl.dataset = LedgerDataSet(None)

        self.presenter = ImportPresenter(self.frame)
        self.view = self.presenter.view

    def tearDown(self):
        self.frame.Destroy()
        self.app.Destroy()

    def testDataset(self):
        # verify global dataset set populated
        self.assertEqual(gbl.dataset.get_emp_data(), test_data.employees)
        self.assertEqual(gbl.dataset.get_dept_data(), test_data.dept_objs)
        self.assertEqual(gbl.dataset.get_grant_admin_data(), test_data.grant_admin_objs)
        # self.assertEqual(gbl.dataset.get_ledger_data(), test_data.ledger_objs)

    def testGetData(self):
        expected_items = sorted(test_xl_data.ss_rex, key=lambda k: k.name)
        expected_mismatches = {
            'BERRA,LAWRENCE P': [
                ('BERRA,YOGI', 86),
                ('KALINE,ALBERT W', 49),
                ('BANKS,ERNEST', 43),
                ('RUTH,BABE', 40),
                ('AARON,HENRY', 37)
            ],
            'FORD,EDWARD C': [
                ('FORD,WHITEY', 50),
                ('KOUFAX,SANFORD', 42),
                ('MAYS,WILLIE HOWARD JR', 41),
                ('AARON,HENRY', 33),
                ('BERRA,YOGI', 33)
            ],
            'RUTH,GEORGE HERMAN': [
                ('RUTH,BABE', 86),
                ('GEHRIG,HENRY LOUIS', 53),
                ('JETER,DEREK', 47),
                ('AARON,HENRY', 41),
                ('FORD,WHITEY', 40)
            ]
        }

        with patch('lib.excel_lib.get_file') as mock_get_file_dlg:
            mock_get_file_dlg.return_value = 'c:/bench/allocat/data/test_salary_notes.xls'
            click_button(self.view.import_btn)

        # Don't know why this doesn't work
        # self.assertEqual(self.view.list_ctrl.GetObjects(), expected_items)
        assertEqualListOfObjects(self.view.list_ctrl.GetObjects(), expected_items)

        self.assertEqual(self.presenter.mismatches.keys(), expected_mismatches.keys())
        self.assertEqual(list(self.presenter.mismatches.values()), list(expected_mismatches.values()))

    def testLoadMismatchList_NoListOnMatch(self):
        with patch('lib.excel_lib.get_file') as mock_get_file_dlg:
            mock_get_file_dlg.return_value = 'c:/bench/allocat/data/test_salary_notes.xls'
            click_button(self.view.import_btn)

        # first item is a match
        click_list_ctrl(self.view.list_ctrl, 0)

        self.assertEqual(self.view.matches_ctrl.GetObjects(), [])

    def testLoadMismatchList_NonMatch(self):
        with patch('lib.excel_lib.get_file') as mock_get_file_dlg:
            mock_get_file_dlg.return_value = 'c:/bench/allocat/data/test_salary_notes.xls'
            click_button(self.view.import_btn)

        expected = [
            {'name': 'BERRA,YOGI', 'score': 86},
            {'name': 'KALINE,ALBERT W', 'score': 49},
            {'name': 'BANKS,ERNEST', 'score': 43},
            {'name': 'RUTH,BABE', 'score': 40},
            {'name': 'AARON,HENRY', 'score': 37}
        ]

        # last item is a mismatch
        click_list_ctrl(self.view.list_ctrl, 2)

        self.assertEqual(self.view.matches_ctrl.GetObjects(), expected)

    def testMatch_NoSelection(self):
        with patch('lib.excel_lib.get_file') as mock_get_file_dlg:
            mock_get_file_dlg.return_value = 'c:/bench/allocat/data/test_salary_notes.xls'
            click_button(self.view.import_btn)

        click_list_ctrl(self.view.list_ctrl, 2)

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

        click_list_ctrl(self.view.list_ctrl, 2)

        # Select not best match
        click_list_ctrl(self.view.matches_ctrl, 1)

        with patch('lib.ui_lib.confirm') as mock_popup:
            mock_popup.return_value = False
            with patch('models.employee.Employee.update_name') as mock_emp_update:
                click_button(self.view.match_btn)

        mock_popup.assert_called_once_with(self.view, 'Not the highest score! Are you sure?')
        mock_emp_update.assert_not_called()

    def testMatch_TopSelection(self):
        from models.spreadsheet_record import SpreadsheetRecord

        with patch('lib.excel_lib.get_file') as mock_get_file_dlg:
            mock_get_file_dlg.return_value = 'c:/bench/allocat/data/test_salary_notes.xls'
            click_button(self.view.import_btn)

        click_list_ctrl(self.view.list_ctrl, 2)

        # Select best match
        click_list_ctrl(self.view.matches_ctrl, 0)

        with patch('lib.ui_lib.show_error') as mock_err_popup:
            with patch('lib.ui_lib.confirm') as mock_confirm_popup:
                with patch('dal.dao.Dao._Dao__write') as mock_emp_update:
                    mock_emp_update.return_value = 1
                    click_button(self.view.match_btn)

        mock_err_popup.assert_not_called()
        mock_confirm_popup.assert_not_called()

        self.assertEqual(mock_emp_update.call_count, 1)
        args, kwargs = mock_emp_update.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 0)
        self.assertEqual(args[0], "UPDATE employees SET name=? WHERE name=?")
        self.assertEqual(args[1], ('BERRA,LAWRENCE P', 'BERRA,YOGI'))

        new_rec = SpreadsheetRecord({
            'name': 'BERRA,LAWRENCE P',
            'salary': 53822,
            'fringe': .077,
            'step_date': None,
            'matched': True
        })

        # Again, self.assertEqual doesn't work
        assertEqualObjects(self.view.list_ctrl.GetObjectAt(2), new_rec)
