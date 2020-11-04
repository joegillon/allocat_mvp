import unittest
import unittest.mock
from unittest.mock import patch
from datetime import datetime
from tests.helpers import *
import globals as gbl
from models.ledger_dataset import LedgerDataSet
from models.ledger import Ledger
from presenters.ledger_presenter import LedgerPresenter
import tests.ledger_data.test_db as test_db
import tests.ledger_data.test_data as test_data
import lib.month_lib as ml


class TestLedgerPresenter(unittest.TestCase):

    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None)

        gbl.COLOR_SCHEME = gbl.SKINS[gbl.pick_scheme()]
        gbl.DB_PATH = 'c:/bench/allocat/tests/allocat.db'

        with patch('dal.dao.Dao._Dao__read') as mock_db:
            mock_db.side_effect = [
                test_db.employees,
                test_db.all_departments,
                test_db.all_grant_admins,
                test_db.ledger_rex_qtr_1
            ]
            gbl.dataset = LedgerDataSet(None)

        self.presenter = LedgerPresenter(self.frame)
        self.view = self.presenter.view

    def tearDown(self):
        self.frame.Destroy()
        self.app.Destroy()

    def testInitView(self):
        # verify global dataset set populate
        assertEqualListOfObjects(gbl.dataset.get_emp_data(), test_data.employee_obs)
        assertEqualListOfObjects(gbl.dataset.get_dept_data(), test_data.dept_objs)
        assertEqualListOfObjects(gbl.dataset.get_grant_admin_data(), test_data.grant_admin_objs)
        assertEqualListOfObjects(gbl.dataset.get_ledger_data(), test_data.ledger_objs)

        # verify dropdowns loaded
        self.assertEqual(self.view.dept_ctrl.GetItems(), test_data.department_items)
        self.assertEqual(self.view.grant_admin_ctrl.GetItems(), test_data.grant_admin_items)

        # verify default query params
        today = datetime.today()
        quarter = ml.get_quarter(ml.get_quarter(today.month)) - 1
        self.assertEqual(self.view.get_year(), today.year)
        self.assertEqual(self.view.get_qtr(), quarter)
        self.assertEqual(self.presenter.quarter, '')

    def testQueryNoAsnsNoEntries(self):
        assert gbl.dataset.get_ledger_entries() == []

        self.view.set_year(2019)
        self.view.set_qtr(1)

        with patch('dal.dao.Dao._Dao__read') as mock_db:
            mock_db.return_value  = []      # no billable assignments
            self.presenter.run_query()

        # verify billables call
        assert mock_db.call_count == 1
        args, kwargs = mock_db.call_args
        assert len(args) == 2
        assert len(kwargs) == 0
        assert args[0] == ("SELECT a.*, e.name AS employee, p.name AS project "
                           "FROM assignments a "
                           "JOIN employees e ON a.employee_id=e.id "
                           "JOIN projects p ON a.project_id=p.id "
                           "WHERE a.frum >= ? AND a.thru <= ? AND p.non_va=?")
        assert args[1] == ('1810', '1812', 1)

        # verify global ledger entries is empty
        assert gbl.dataset.get_ledger_entries() == []

        # verify list has no entries
        assert self.view.list_ctrl.GetObjects() == []

        # verify there is not list selection
        assert self.view.get_selection() is None

        # verify details form is blank
        assert self.view.get_form_values() == test_data.blank_details_form

    def testRunQuerySelectionNoLedgerRex(self):
        assert gbl.dataset.get_ledger_entries() == []

        # there are no ledger records in DB for quarter 20202
        assert gbl.dataset.get_ledger_data('20202') == []

        self.view.set_year(2020)
        self.view.set_qtr(2)

        with patch('dal.dao.Dao._Dao__read') as mock_db:
            mock_db.return_value = test_db.billable_assignments_qtr_2
            self.presenter.run_query()

        # verify billables call
        assert mock_db.call_count == 1
        args, kwargs = mock_db.call_args
        assert len(args) == 2
        assert len(kwargs) == 0
        assert args[0] == ("SELECT a.*, e.name AS employee, p.name AS project "
                           "FROM assignments a "
                           "JOIN employees e ON a.employee_id=e.id "
                           "JOIN projects p ON a.project_id=p.id "
                           "WHERE a.frum >= ? AND a.thru <= ? AND p.non_va=?")
        assert args[1] == ('2001', '2003', 1)

        # verify global ledger data
        assertEqualListOfObjects(gbl.dataset.get_ledger_entries(), test_data.ledger_items_qtr_2)

        #verify global ledger data all built from billable assignments
        asn_ids = [asn.id for asn in gbl.dataset.get_asn_data()]
        ledger_asn_ids = [entry.asn_id for entry in gbl.dataset.get_ledger_entries()]
        assert asn_ids.sort() == ledger_asn_ids.sort()

        # verify list
        assertEqualListOfObjects(self.view.list_ctrl.GetObjects(), test_data.ledger_items_qtr_2)

        # verify there is not list selection
        assert self.view.get_selection() is None

        # verify details form is blank
        assert self.view.get_form_values() == test_data.blank_details_form
        items = self.view.list_ctrl.GetObjects()
        self.assertEqual(len(items), 6)

    def testRunQuerySelectionWithLedgerRex(self):
        assert gbl.dataset.get_ledger_entries() == []

        # there are ledger records in DB for quarter 20201
        ledger_data = gbl.dataset.get_ledger_data('20201')
        assertEqualListOfObjects(ledger_data, test_data.ledger_items_qtr_1)
        assert [entry.asn_id for entry in ledger_data] == [2271, 2272, 2282]

        self.view.set_year(2020)
        self.view.set_qtr(1)

        with patch('dal.dao.Dao._Dao__read') as mock_db:
            mock_db.return_value = test_db.billable_assignments_qtr_1
            self.presenter.run_query()

        # verify billables call
        assert mock_db.call_count == 1
        args, kwargs = mock_db.call_args
        assert len(args) == 2
        assert len(kwargs) == 0
        assert args[0] == ("SELECT a.*, e.name AS employee, p.name AS project "
                           "FROM assignments a "
                           "JOIN employees e ON a.employee_id=e.id "
                           "JOIN projects p ON a.project_id=p.id "
                           "WHERE a.frum >= ? AND a.thru <= ? AND p.non_va=?")
        assert args[1] == ('1910', '1912', 1)

        # verify global ledger data
        assertEqualListOfObjects(gbl.dataset.get_ledger_entries(), test_data.ledger_items_qtr_1)
        asn_ids = [asn.id for asn in gbl.dataset.get_asn_data()]
        ledger_asn_ids = [entry.asn_id for entry in gbl.dataset.get_ledger_entries()]
        assert asn_ids.sort() == ledger_asn_ids.sort()

        # verify list
        assertEqualListOfObjects(self.view.list_ctrl.GetObjects(), test_data.ledger_items_qtr_1)

        # verify there is not list selection
        assert self.view.get_selection() is None

        # verify details form is blank
        assert self.view.get_form_values() == test_data.blank_details_form
        items = self.view.list_ctrl.GetObjects()
        self.assertEqual(len(items), 6)

    def testLoadDetails_No_Salary(self):
        assert gbl.dataset.get_ledger_entries() == []

        # there are ledger records in DB for quarter 20201
        ledger_data = gbl.dataset.get_ledger_data('20201')
        assertEqualListOfObjects(ledger_data, test_data.ledger_items_qtr_1)
        assert [entry.asn_id for entry in ledger_data] == [2271, 2272, 2282]

        self.view.set_year(2020)
        self.view.set_qtr(1)

        with patch('dal.dao.Dao._Dao__read') as mock_db:
            mock_db.return_value = test_db.billable_assignments_qtr_1
            self.presenter.run_query()

        # verify billables call
        assert mock_db.call_count == 1
        args, kwargs = mock_db.call_args
        assert len(args) == 2
        assert len(kwargs) == 0
        assert args[0] == ("SELECT a.*, e.name AS employee, p.name AS project "
                           "FROM assignments a "
                           "JOIN employees e ON a.employee_id=e.id "
                           "JOIN projects p ON a.project_id=p.id "
                           "WHERE a.frum >= ? AND a.thru <= ? AND p.non_va=?")
        assert args[1] == ('1910', '1912', 1)

        # verify global ledger data
        assertEqualListOfObjects(gbl.dataset.get_ledger_entries(), test_data.ledger_items_qtr_1)
        asn_ids = [asn.id for asn in gbl.dataset.get_asn_data()]
        ledger_asn_ids = [entry.asn_id for entry in gbl.dataset.get_ledger_entries()]
        assert asn_ids.sort() == ledger_asn_ids.sort()

        # verify list
        assertEqualListOfObjects(self.view.list_ctrl.GetObjects(), test_data.ledger_items_qtr_1)

        # verify there is not list selection
        assert self.view.get_selection() is None

        # verify details form is blank
        assert self.view.get_form_values() == test_data.blank_details_form
        items = self.view.list_ctrl.GetObjects()
        self.assertEqual(len(items), 6)

        # select an entry
        with patch('lib.ui_lib.show_error', return_value=None) as popup_mock:
            click_list_ctrl(self.view.list_ctrl, 3)

        # verify selection in the list
        item = self.view.get_selection()
        self.assertEqual(item.employee, 'Emp 61')
        self.assertEqual(item.asn_id, 2282)

        # verify no salary popup
        popup_mock.assert_called_once_with('Emp 61 has no salary! Not imported?')

        # verify details have been loaded
        self.assertEqual(self.view.get_employee(), 'Emp 61')

    def testLoadDetailsWithSalary(self):
        assert gbl.dataset.get_ledger_entries() == []

        # there are ledger records in DB for quarter 20201
        ledger_data = gbl.dataset.get_ledger_data('20201')
        assertEqualListOfObjects(ledger_data, test_data.ledger_items_qtr_1)
        assert [entry.asn_id for entry in ledger_data] == [2271, 2272, 2282]

        self.view.set_year(2020)
        self.view.set_qtr(1)

        with patch('dal.dao.Dao._Dao__read') as mock_db:
            mock_db.return_value = test_db.billable_assignments_qtr_1
            self.presenter.run_query()

        # verify billables call
        assert mock_db.call_count == 1
        args, kwargs = mock_db.call_args
        assert len(args) == 2
        assert len(kwargs) == 0
        assert args[0] == ("SELECT a.*, e.name AS employee, p.name AS project "
                           "FROM assignments a "
                           "JOIN employees e ON a.employee_id=e.id "
                           "JOIN projects p ON a.project_id=p.id "
                           "WHERE a.frum >= ? AND a.thru <= ? AND p.non_va=?")
        assert args[1] == ('1910', '1912', 1)

        # verify global ledger data
        assertEqualListOfObjects(gbl.dataset.get_ledger_entries(), test_data.ledger_items_qtr_1)
        asn_ids = [asn.id for asn in gbl.dataset.get_asn_data()]
        ledger_asn_ids = [entry.asn_id for entry in gbl.dataset.get_ledger_entries()]
        assert asn_ids.sort() == ledger_asn_ids.sort()

        # verify list
        assertEqualListOfObjects(self.view.list_ctrl.GetObjects(), test_data.ledger_items_qtr_1)

        # verify there is not list selection
        assert self.view.get_selection() is None

        # verify details form is blank
        assert self.view.get_form_values() == test_data.blank_details_form
        items = self.view.list_ctrl.GetObjects()
        self.assertEqual(len(items), 6)

        # select an entry
        with patch('lib.ui_lib.show_error', return_value=None) as popup_mock:
            click_list_ctrl(self.view.list_ctrl, 2)

        # verify selection in the list
        item = self.view.get_selection()
        self.assertEqual(item.employee, 'Emp 52')

        # verify no salary popup not called
        popup_mock.assert_not_called()

        # verify details have been loaded
        self.assertEqual(self.view.get_employee(), 'Emp 52')

    def testUpdateEntry(self):
        assert gbl.dataset.get_ledger_entries() == []

        # there are ledger records in DB for quarter 20201
        ledger_data = gbl.dataset.get_ledger_data('20201')
        assertEqualListOfObjects(ledger_data, test_data.ledger_items_qtr_1)
        assert [entry.asn_id for entry in ledger_data] == [2271, 2272, 2282]

        self.view.set_year(2020)
        self.view.set_qtr(1)

        with patch('dal.dao.Dao._Dao__read') as mock_db:
            mock_db.return_value = test_db.billable_assignments_qtr_1
            self.presenter.run_query()

        # verify billables call
        assert mock_db.call_count == 1
        args, kwargs = mock_db.call_args
        assert len(args) == 2
        assert len(kwargs) == 0
        assert args[0] == ("SELECT a.*, e.name AS employee, p.name AS project "
                           "FROM assignments a "
                           "JOIN employees e ON a.employee_id=e.id "
                           "JOIN projects p ON a.project_id=p.id "
                           "WHERE a.frum >= ? AND a.thru <= ? AND p.non_va=?")
        assert args[1] == ('1910', '1912', 1)

        # verify global ledger data
        assertEqualListOfObjects(gbl.dataset.get_ledger_entries(), test_data.ledger_items_qtr_1)
        asn_ids = [asn.id for asn in gbl.dataset.get_asn_data()]
        ledger_asn_ids = [entry.asn_id for entry in gbl.dataset.get_ledger_entries()]
        assert asn_ids.sort() == ledger_asn_ids.sort()

        # verify list
        assertEqualListOfObjects(self.view.list_ctrl.GetObjects(), test_data.ledger_items_qtr_1)

        # verify there is not list selection
        assert self.view.get_selection() is None

        # verify details form is blank
        assert self.view.get_form_values() == test_data.blank_details_form
        items = self.view.list_ctrl.GetObjects()
        self.assertEqual(len(items), 6)

        # select an entry
        with patch('lib.ui_lib.show_error', return_value=None) as popup_mock:
            click_list_ctrl(self.view.list_ctrl, 2)

        # verify selection in the list
        item = self.view.get_selection()
        self.assertEqual(item.employee, 'Emp 52')
        self.assertEqual(item.asn_id, 2283)

        # verify no salary popup not called
        popup_mock.assert_not_called()

        # verify details have been loaded
        self.assertEqual(self.view.get_employee(), 'Emp 52')

        # edit details
        click_combobox_ctrl(self.view.dept_ctrl, 2)
        check_checkbox_ctrl(self.view.admin_approved_ctrl)
        check_checkbox_ctrl(self.view.va_approved_ctrl)
        enter_in_textbox_ctrl(self.view.invoice_ctrl, 'K0H0002')
        enter_in_textbox_ctrl(self.view.short_code_ctrl, '123456')
        click_combobox_ctrl(self.view.grant_admin_ctrl, 3)

        # verify grant admin email is done
        self.assertEqual(self.view.get_grant_admin_email(), 'chico@umich.edu')

        with patch('dal.dao.Dao._Dao__write') as write_mock:
            write_mock.return_value = 1
            with patch('lib.ui_lib.show_msg') as popup_mock:
                popup_mock.return_value = None
                click_button(self.view.update_entry_btn)

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
            '20201', 'CARDIOLOGY', True, True, 'K0H0002', '2283', '104971', '33.5',
            '13817.54', '92', '127121.41', False, '127121.41', '123456',
            'MARX,CHICO', 'chico@umich.edu'
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
        assertEqualObjects(expected_item, self.view.get_selection())

    def testGetTotalDays(self):
        q_frum = '1910'
        q_thru = '1912'
        assert self.presenter.get_total_days_asn(q_frum, q_thru, q_frum, q_thru) == 92
        assert self.presenter.get_total_days_asn(q_frum, q_thru, q_frum, '1911') == 61
        assert self.presenter.get_total_days_asn(q_frum, q_thru, q_frum, '2001') == 92
        assert self.presenter.get_total_days_asn(q_frum, q_thru, '1909', q_thru) == 92
        assert self.presenter.get_total_days_asn(q_frum, q_thru, '1909', '1910') == 31
        assert self.presenter.get_total_days_asn(q_frum, q_thru, '1909', '1911') == 61
        assert self.presenter.get_total_days_asn(q_frum, q_thru, '1909', '2001') == 92
        assert self.presenter.get_total_days_asn(q_frum, q_thru, '1911', q_thru) == 61
        assert self.presenter.get_total_days_asn(q_frum, q_thru, '1911', '1911') == 30
        assert self.presenter.get_total_days_asn(q_frum, q_thru, '1911', '2001') == 61
        print('\n' + str(self.presenter.get_total_days_asn('2001', '2003', '2002', '2003')))

    def testCalculateCost(self):
        salary = 123554
        fringe = .41
        effort = 10
        ndays = 91
        cost = self.presenter.calculate_cost(salary, fringe, effort, ndays)
        self.assertEqual(cost, (6076.94, 667.8))

        salary = 44444
        fringe = .044
        effort = 45
        ndays = 60
        cost = self.presenter.calculate_cost(salary, fringe, effort, ndays)
        self.assertEqual(cost, (4802.25, 177.86))

        salary = 104971
        fringe = .335
        effort = 10
        ndays = 58
        cost = self.presenter.calculate_cost(salary, fringe, effort, ndays)
        self.assertEqual(cost, (3115.63, 537.18))

        salary = 123554
        fringe = .42
        effort = 10
        ndays = 90
        cost = self.presenter.calculate_cost(salary, fringe, effort, ndays)
        self.assertEqual(cost, (6052.78, 672.53))

        salary = 123554
        fringe = .42
        effort = 10
        ndays = 28
        cost = self.presenter.calculate_cost(salary, fringe, effort, ndays)
        self.assertEqual(cost, (1883.09, 672.53))
