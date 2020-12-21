import unittest
from unittest.mock import patch
from tests.helpers import *
import globals as gbl
from models.dataset import AllocatDataSet
from presenters.effort_presenter import EffortPresenter


the_table = [
    ['EmpID', 'Employee', 'FTE', '12/19', '01/20', '02/20', '03/20', '04/20', '05/20', '06/20', '07/20', '08/20', '09/20', '10/20', '11/20'],
    ['44', 'AARON,HENRY', '100', '50', '50', '65', '65', '65', '65', '65', '65', '65', '65', '0', '0'],
    ['14', 'BANKS,ERNEST', '100', '65', '20', '20', '20', '20', '20', '20', '20', '20', '20', '0', '0'],
    ['8', 'BERRA,YOGI', '80', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['5', 'DIMAGGIO,JOSEPH P', '100', '3', '3', '48', '48', '3', '3', '3', '3', '3', '3', '0', '0'],
    ['16', 'FORD,WHITEY', '100', '10', '10', '10', '10', '10', '10', '10', '10', '10', '10', '0', '0'],
    ['4', 'GEHRIG,HENRY LOUIS', '50', '10', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['2', 'JETER,DEREK', '100', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0'],
    ['6', 'KALINE,ALBERT W', '100', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '0', '0'],
    ['32', 'KOUFAX,SANFORD', '100', '40', '40', '40', '40', '40', '40', '40', '40', '40', '40', '0', '0'],
    ['7', 'MANTLE,MICKEY', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['24', 'MAYS,WILLIE HOWARD JR', '63', '25', '25', '35', '25', '25', '25', '25', '25', '25', '25', '0', '0'],
    ['3', 'RUTH,BABE', '100', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '0', '0'],
    ['9', 'WILLIAMS,THEODORE', '62', '55', '55', '55', '45', '45', '45', '45', '45', '45', '45', '0', '0']
]

the_colors = [
    [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
]


class TestEffortPresenter(unittest.TestCase):

    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None)

        gbl.COLOR_SCHEME = gbl.SKINS[gbl.pick_scheme()]
        gbl.DB_PATH = 'c:/bench/allocat/tests/allocat.db'

        gbl.dataset = AllocatDataSet(None)

        with patch('presenters.effort_presenter.EffortPresenter.get_init_dates') as mock_dates:
            mock_dates.return_value = ('1912', '2011')
            self.presenter = EffortPresenter(self.frame)

    def tearDown(self):
        self.frame.Destroy()
        self.app.Destroy()

    def get_vars(self):
        return self.presenter.view, self.presenter.model, self.presenter.view.grid_ctrl

    def testViewLoaded(self):
        view, model, grid_ctrl = self.get_vars()

        # Check default dateframe
        self.assertEqual(view.get_frum(), '1912')
        self.assertEqual(view.frum_ctrl.GetValue(), '12/19')
        self.assertEqual(view.get_thru(), '2011')
        self.assertEqual(view.thru_ctrl.GetValue(), '11/20')

        # Check the grid
        self.assertEqual(grid_to_list(grid_ctrl), the_table)
        self.assertEqual(get_grid_colors(grid_ctrl), the_colors)

    def testNamePopupNoAsns(self):
        view, model, grid_ctrl = self.get_vars()

        # Select employee with no assignments
        with patch('lib.ui_lib.show_msg') as mock_msg_popup:
            mock_msg_popup.return_value = None
            with patch('views.emp_brkdwn_dlg.EmployeeBreakdownDialog.ShowModal') as mock_emp_popup:
                mock_emp_popup.return_value = None
                click_grid_cell(grid_ctrl, 2, 1)

        mock_emp_popup.assert_not_called()
        mock_msg_popup.assert_called_once_with('No assignments!', 'allocat')

    def testNamePopupHasAsns(self):
        view, model, grid_ctrl = self.get_vars()

        # Select employee with assignments
        with patch('views.emp_brkdwn_dlg.EmployeeBreakdownDialog.ShowModal') as mock_popup:
            mock_popup.return_value = None
            click_grid_cell(grid_ctrl, 0, 1)

        mock_popup.assert_called_once()

        dlg = view.Children[2]
        self.assertEqual(dlg.name_lbl.GetLabelText(), '2 assignments for AARON,HENRY')
        self.assertEqual(dlg.total_lbl.GetLabelText(), 'Total effort: 65')
        expected = [
            ['Prj 298', '07/19', '09/20', '50'],
            ['Prj 309', '02/20', '09/20', '15']
        ]
        self.assertEqual(get_list_items(dlg.the_list), expected)

    def testFteNoPopup(self):
        view, model, grid_ctrl = self.get_vars()

        # Select fte of employee with assignments
        with patch('lib.ui_lib.show_msg') as mock_msg_popup:
            mock_msg_popup.return_value = None
            with patch('views.emp_brkdwn_dlg.EmployeeBreakdownDialog.ShowModal') as mock_emp_popup:
                mock_emp_popup.return_value = None
                click_grid_cell(grid_ctrl, 2, 2)

        mock_emp_popup.assert_not_called()
        mock_msg_popup.assert_not_called()

    def testMonthPopupNoAsns(self):
        view, model, grid_ctrl = self.get_vars()

        # Select month with assignments
        with patch('lib.ui_lib.show_msg') as mock_msg_popup:
            mock_msg_popup.return_value = None
            with patch('views.month_brkdwn_dlg.MonthBreakdownDialog.ShowModal') as mock_month_popup:
                mock_month_popup.return_value = None
                click_grid_cell(grid_ctrl, 2, 3)

        mock_month_popup.assert_not_called()
        mock_msg_popup.assert_called_once_with('No assignments!', 'allocat')

    def testMonthPopupHasAsns(self):
        view, model, grid_ctrl = self.get_vars()

        # Select month with assignments
        with patch('views.month_brkdwn_dlg.MonthBreakdownDialog.ShowModal') as mock_month_popup:
            mock_month_popup.return_value = None
            click_grid_cell(grid_ctrl, 1, 3)

        mock_month_popup.assert_called_once()

        dlg = view.Children[2]
        self.assertEqual(dlg.lbl.GetLabelText(), 'BANKS,ERNEST @ 12/19')
        expected = [
            ['Prj 297', '45'],
            ['Prj 315', '20']
        ]
        self.assertEqual(get_list_items(dlg.the_list), expected)

    def testInvalidTimeframes(self):
        view, model, grid_ctrl = self.get_vars()

        pass

    def testRunQuery(self):
        view, model, grid_ctrl = self.get_vars()

        view.set_frum('1909')

        click_button(view.run_btn)

        # Check the grid
        expected = [
            ['EmpID', 'Employee', 'FTE', '09/19', '10/19', '11/19', '12/19', '01/20', '02/20', '03/20', '04/20', '05/20', '06/20', '07/20', '08/20', '09/20', '10/20', '11/20'],
            ['44', 'AARON,HENRY', '100', '50', '50', '50', '50', '50', '65', '65', '65', '65', '65', '65', '65', '65', '0', '0'],
            ['14', 'BANKS,ERNEST', '100', '0', '65', '65', '65', '20', '20', '20', '20', '20', '20', '20', '20', '20', '0', '0'],
            ['8', 'BERRA,YOGI', '80', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['5', 'DIMAGGIO,JOSEPH P', '100', '0', '3', '3', '3', '3', '48', '48', '3', '3', '3', '3', '3', '3', '0', '0'],
            ['16', 'FORD,WHITEY', '100', '10', '10', '10', '10', '10', '10', '10', '10', '10', '10', '10', '10', '10', '0', '0'],
            ['4', 'GEHRIG,HENRY LOUIS', '50', '0', '10', '10', '10', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['2', 'JETER,DEREK', '100', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '0'],
            ['6', 'KALINE,ALBERT W', '100', '0', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '5', '0', '0'],
            ['32', 'KOUFAX,SANFORD', '100', '0', '40', '40', '40', '40', '40', '40', '40', '40', '40', '40', '40', '40', '0', '0'],
            ['7', 'MANTLE,MICKEY', '0', '10', '10', '10', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['24', 'MAYS,WILLIE HOWARD JR', '63', '25', '25', '25', '25', '25', '35', '25', '25', '25', '25', '25', '25', '25', '0', '0'],
            ['3', 'RUTH,BABE', '100', '0', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '0', '0'],
            ['9', 'WILLIAMS,THEODORE', '62', '0', '45', '45', '55', '55', '55', '45', '45', '45', '45', '45', '45', '45', '0', '0']
        ]
        self.assertEqual(grid_to_list(grid_ctrl), expected)
        expected = [
            [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
            [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
            [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
            [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
            [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
            [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
            [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
            [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
            [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
            [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
            [0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
        ]
        self.assertEqual(get_grid_colors(grid_ctrl), expected)
