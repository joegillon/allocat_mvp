import unittest
import unittest.mock
from unittest.mock import patch
from datetime import datetime
from tests.helpers import *
import globals as gbl
from models.ledger_dataset import LedgerDataSet
from models.ledger import Ledger
from presenters.ledger_presenter import LedgerPresenter
import tests.ledger_data.records as test_data
import lib.month_lib as ml


class TestLedgerPresenter(unittest.TestCase):

    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None)

        gbl.COLOR_SCHEME = gbl.SKINS[gbl.pick_scheme()]
        gbl.DB_PATH = 'c:/bench/allocat/tests/allocat.db'
        gbl.dataset = LedgerDataSet(gbl.DB_PATH)

        self.presenter = LedgerPresenter(self.frame)

    def tearDown(self):
        self.frame.Destroy()
        self.app.Destroy()

    def run_query(self, yr, qtr):
        self.presenter.view.set_year(yr)
        self.presenter.view.set_qtr(qtr)
        self.presenter.run_query()

    def add_ledger_rex_db_only(self):
        pass

    def remove_ledger_rex_db_only(self):
        pass

    def testInitView(self):
        self.presenter.init_view()
        self.assertEqual(self.presenter.view.dept_ctrl.GetItems(), test_data.department_items)
        self.assertEqual(self.presenter.view.grant_admin_ctrl.GetItems(), test_data.grant_admin_items)
        today = datetime.today()
        quarter = ml.get_quarter(today.month)
        self.assertEqual(self.presenter.view.get_year(), today.year)
        self.assertEqual(self.presenter.view.get_qtr(), quarter)
        self.assertEqual(self.presenter.quarter, '')

    def testRunQueryDefaultSelectionNoLedgerRex(self):
        self.presenter.run_query()
        items = self.presenter.view.list_ctrl.GetObjects()
        self.assertEqual(len(items), 2)

    def testRunQueryDefaultSelectionWithLedgerRex(self):
        # self.add_ledger_rex()
        # asserts
        # self.remove_ledger_rex()
        pass

    def testLoadDetails_No_Salary(self):
        # run a query
        self.run_query(2020, 10)

        # select an entry
        with patch('lib.ui_lib.show_error', return_value=None) as popup_mock:
            click_list_ctrl(self.presenter.view.list_ctrl, 1)

        # verify selection in the list
        item = self.presenter.view.get_selection()
        self.assertEqual(item.employee, 'CHEN,CHARITY')

        # verify no salary popup
        popup_mock.assert_called_once_with('CHEN,CHARITY has no salary! Not imported?')

        # verify details have been loaded
        self.assertEqual(self.presenter.view.get_employee(), 'CHEN,CHARITY')

    def testLoadDetails(self):
        # run a query
        self.run_query(2020, 10)

        # select an entry
        click_list_ctrl(self.presenter.view.list_ctrl, 0)

        # verify selection in the list
        item = self.presenter.view.get_selection()
        self.assertEqual(item.employee, 'GILLON,LEAH R')

        # verify the details have been loaded
        self.assertEqual(self.presenter.view.get_employee(), 'GILLON,LEAH R')

    def testUpdateEntry(self):
        # run a query
        self.run_query(2020, 10)

        # select an entry
        click_list_ctrl(self.presenter.view.list_ctrl, 0)

        # verify selection in the list
        item = self.presenter.view.get_selection()
        self.assertEqual(item.employee, 'GILLON,LEAH R')

        # verify the details have been loaded
        self.assertEqual(self.presenter.view.get_employee(), 'GILLON,LEAH R')

        # edit details
        click_combobox_ctrl(self.presenter.view.dept_ctrl, 2)
        check_checkbox_ctrl(self.presenter.view.admin_approved_ctrl)
        check_checkbox_ctrl(self.presenter.view.va_approved_ctrl)
        enter_in_textbox_ctrl(self.presenter.view.invoice_ctrl, 'K0H0001')
        enter_in_textbox_ctrl(self.presenter.view.short_code_ctrl, '123456')
        click_combobox_ctrl(self.presenter.view.grant_admin_ctrl, 3)

        # verify grant admin email is done
        self.assertEqual(self.presenter.view.get_grant_admin_email(), 'bdensen@umich.edu')

        with patch('dal.dao.Dao._Dao__write') as write_mock:
            write_mock.return_value = 1
            with patch('lib.ui_lib.show_msg') as popup_mock:
                popup_mock.return_value = None
                click_button(self.presenter.view.update_entry_btn)

        # verify the DB call
        assert write_mock.call_count == 1
        args, kwargs = write_mock.call_args
        assert len(args) == 2
        assert len(kwargs) == 0
        sql = ("INSERT INTO ledger "
               "(quarter,dept,admin_approved,va_approved,invoice_num,"
               "asn_id,salary,fringe,total_day,days,amount,paid,balance,short_code,"
               "grant_admin,grant_admin_email) "
               "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)")
        assert args[0] == sql
        assert args[1] == [
            '20201', 'CARDIOLOGY', True, True, 'K0H0001', '2271', '110234', '31.7',
            '13817.54', '92', '127121.41', False, '127121.41', '123456',
            'DENSEN,BRAD', 'bdensen@umich.edu'
        ]

        # verify user notification
        assert popup_mock.call_count == 1
        args, kwargs = popup_mock.call_args
        assert len(args) == 2
        assert len(kwargs) == 0
        assert args[0] == 'Ledger updated!'
        assert args[1] == 'Hooray'

        # verify list updated
        expected_item = Ledger({
            'admin_approved': True,
            'amount': 127121.41,
            'asn_id': 2271,
            'balance': '127121.41',
            'days': 92,
            'dept': 'CARDIOLOGY',
            'effort': 10,
            'employee': 'GILLON,LEAH R',
            'fringe': 31.7,
            'frum': '10/1/19',
            'grant_admin': 'DENSEN,BRAD',
            'grant_admin_email': 'bdensen@umich.edu',
            'id': 1,
            'invoice_num': 'K0H0001',
            'paid': False,
            'project': 'UM DOAC (Barnes/Sussman)',
            'quarter': '20201',
            'salary': 110234,
            'short_code': '123456',
            'thru': '12/31/19',
            'total_day': 13817.54,
            'va_approved': True
        })
        assertEqualObjects(expected_item, self.presenter.view.get_selection())

    def testCalculateCost(self):
        salary = 123554
        fringe = .41
        effort = 10
        ndays = 91
        cost = self.presenter.calculate_cost(salary, fringe, effort, ndays)
        self.assertEquals(cost, (6076.94, 667.8))
