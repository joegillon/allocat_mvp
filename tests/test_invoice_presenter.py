import unittest
import unittest.mock
from unittest.mock import patch
from tests.helpers import *
import globals as gbl
from models.ledger_dataset import LedgerDataSet
from models.invoice import Invoice
from presenters.invoice_presenter import InvoicePresenter
import tests.ledger_data.test_data as test_data


class TestInvoicePresenter(unittest.TestCase):

    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None)

        gbl.COLOR_SCHEME = gbl.SKINS[gbl.pick_scheme()]

        gbl.dataset = LedgerDataSet(None)

        with patch('presenters.invoice_presenter.InvoicePresenter.get_init_quarter') as mock_qtr:
            mock_qtr.return_value = (2020, 1)
            self.presenter = InvoicePresenter(self.frame)
            self.view = self.presenter.view

    def tearDown(self):
        self.frame.Destroy()
        self.app.Destroy()

    def testInitView(self):
        # verify global dataset set populated
        self.assertEqual(gbl.dataset.get_emp_data(), test_data.employees)
        self.assertEqual(gbl.dataset.get_dept_data(), test_data.dept_objs)
        self.assertEqual(gbl.dataset.get_grant_admin_data(), test_data.grant_admin_objs)
        # self.assertEqual(gbl.dataset.get_ledger_data(), test_data.ledger_objs)
        self.assertEqual(gbl.dataset.get_asn_data(), test_data.assignments)

        # verify dropdowns loaded
        self.assertEqual(self.view.dept_ctrl.GetItems(), test_data.department_items)
        self.assertEqual(self.view.grant_admin_ctrl.GetItems(), test_data.grant_admin_items)

        # verify default query params
        self.assertEqual(self.view.get_year(), 2020)
        self.assertEqual(self.view.get_qtr(), 1)
        self.assertEqual(self.presenter.quarter, '')

    def testQueryNoAsnsNoLedger(self):
        self.view.set_year(2019)
        self.view.set_qtr(2)

        click_button(self.view.qry_btn)

        # verify global ledger entries is empty
        self.assertEqual(gbl.dataset.get_ledger_entries(), [])

        # verify list has no entries
        self.assertEqual(self.view.list_ctrl.GetObjects(), gbl.dataset.get_ledger_entries())

        # verify there is not list selection
        self.assertIsNone(self.view.get_selection())

        # verify details form is blank
        expected = {
            'dept': None,
            'admin_approved': False,
            'va_approved': False,
            'invoice_num': None,
            'short_code': None,
            'grant_admin': None,
            'grant_admin_email': None
        }
        self.assertEqual(self.view.get_form_values(), expected)

    def testRunQueryWithAsnsNoLedgerRex(self):
        self.view.set_year(2020)
        self.view.set_qtr(2)

        click_button(self.view.qry_btn)

        # verify global ledger data all built from billable assignments
        self.assertEqual(gbl.dataset.get_ledger_entries(), test_data.invoice_items_qtr_2)

        # verify display updated
        self.assertEqual(self.view.list_ctrl.GetObjects(), gbl.dataset.get_ledger_entries())

        # verify there is not list selection
        self.assertIsNone(self.view.get_selection())

        # verify details form is blank
        expected = {
            'dept': None,
            'admin_approved': False,
            'va_approved': False,
            'invoice_num': None,
            'short_code': None,
            'grant_admin': None,
            'grant_admin_email': None
        }
        self.assertEqual(self.view.get_form_values(), expected)

    def testRunQueryWithAsnsAndLedgerRex(self):
        self.view.set_year(2020)
        self.view.set_qtr(1)

        click_button(self.view.qry_btn)

        # verify global ledger data all built from billable assignments
        self.assertEqual(gbl.dataset.get_ledger_entries(), test_data.invoice_items_qtr_1)

        # verify display updated
        self.assertEqual(self.view.list_ctrl.GetObjects(), gbl.dataset.get_ledger_entries())

        # verify there is not list selection
        self.assertIsNone(self.view.get_selection())

        # verify details form is blank
        expected = {
            'dept': None,
            'admin_approved': False,
            'va_approved': False,
            'invoice_num': None,
            'short_code': None,
            'grant_admin': None,
            'grant_admin_email': None
        }
        self.assertEqual(self.view.get_form_values(), expected)

    def testLoadDetails_No_Salary(self):
        self.view.set_year(2020)
        self.view.set_qtr(1)

        click_button(self.view.qry_btn)

        with patch('lib.ui_lib.show_error') as mock_popup:
            mock_popup.return_value = None
            click_list_ctrl(self.view.list_ctrl, 2)

        # verify popup
        mock_popup.assert_called_once_with('MANTLE,MICKEY has no salary! Not imported?')

        # verify details
        expected = {
            'dept': 'EPIDEMIOLOGY',
            'admin_approved': False,
            'va_approved': False,
            'invoice_num': 'K0H1003',
            'short_code': '556677',
            'grant_admin': 'MARX,CHICO',
            'grant_admin_email': 'chico@umich.edu'
        }
        self.assertEqual(self.view.get_form_values(), expected)

        # verify display only items
        self.assertEqual(self.view.prj_ctrl.GetValue(), 'Prj 299')
        self.assertEqual(self.view.emp_ctrl.GetValue(), 'MANTLE,MICKEY')
        self.assertEqual(self.view.eff_ctrl.GetValue(), '10')
        self.assertEqual(self.view.frum_ctrl.GetValue(), '10/19')
        self.assertEqual(self.view.thru_ctrl.GetValue(), '11/19')
        self.assertEqual(self.view.salary_ctrl.GetValue(), '')
        self.assertEqual(self.view.fringe_ctrl.GetValue(), '')
        self.assertEqual(self.view.total_ctrl.GetValue(), '')
        self.assertEqual(self.view.days_ctrl.GetValue(), '61')
        self.assertEqual(self.view.amt_ctrl.GetValue(), '')
        self.assertEqual(self.view.paid_ctrl.GetValue(), False)
        self.assertEqual(self.view.balance_ctrl.GetValue(), '')

    def testLoadDetailsWithSalaryNoUserInput(self):
        self.view.set_year(2020)
        self.view.set_qtr(1)

        click_button(self.view.qry_btn)

        with patch('lib.ui_lib.show_error') as mock_popup:
            mock_popup.return_value = None
            click_list_ctrl(self.view.list_ctrl, 1)

        # verify popup
        mock_popup.assert_not_called()

        # verify details
        expected = {
            'dept': None,
            'admin_approved': False,
            'va_approved': False,
            'invoice_num': None,
            'short_code': None,
            'grant_admin': None,
            'grant_admin_email': None
        }
        self.assertEqual(self.view.get_form_values(), expected)

        # verify display only items
        self.assertEqual(self.view.prj_ctrl.GetValue(), 'Prj 297')
        self.assertEqual(self.view.emp_ctrl.GetValue(), 'GEHRIG,HENRY LOUIS')
        self.assertEqual(self.view.eff_ctrl.GetValue(), '10')
        self.assertEqual(self.view.frum_ctrl.GetValue(), '10/19')
        self.assertEqual(self.view.thru_ctrl.GetValue(), '12/19')
        self.assertEqual(self.view.salary_ctrl.GetValue(), '104,971')
        self.assertEqual(self.view.fringe_ctrl.GetValue(), '33.5')
        self.assertEqual(self.view.total_ctrl.GetValue(), '537.18')
        self.assertEqual(self.view.days_ctrl.GetValue(), '92')
        self.assertEqual(self.view.amt_ctrl.GetValue(), '4,942.04')
        self.assertEqual(self.view.paid_ctrl.GetValue(), False)
        self.assertEqual(self.view.balance_ctrl.GetValue(), '4,942.04')

    def testLoadDetailsWithSalaryAndUserInput(self):
        self.view.set_year(2020)
        self.view.set_qtr(1)

        click_button(self.view.qry_btn)

        with patch('lib.ui_lib.show_error') as mock_popup:
            mock_popup.return_value = None
            click_list_ctrl(self.view.list_ctrl, 0)

        # verify popup
        mock_popup.assert_not_called()

        # verify details
        expected = {
            'dept': 'HEMATOLOGY',
            'admin_approved': False,
            'va_approved': True,
            'invoice_num': 'K0H1001',
            'short_code': '123456',
            'grant_admin': 'MARX,GROUCHO',
            'grant_admin_email': 'groucho@umich.edu'
        }
        self.assertEqual(self.view.get_form_values(), expected)

        # verify display only items
        self.assertEqual(self.view.prj_ctrl.GetValue(), 'Prj 297')
        self.assertEqual(self.view.emp_ctrl.GetValue(), 'BANKS,ERNEST')
        self.assertEqual(self.view.eff_ctrl.GetValue(), '45')
        self.assertEqual(self.view.frum_ctrl.GetValue(), '10/19')
        self.assertEqual(self.view.thru_ctrl.GetValue(), '12/19')
        self.assertEqual(self.view.salary_ctrl.GetValue(), '44,444')
        self.assertEqual(self.view.fringe_ctrl.GetValue(), '4.4')
        self.assertEqual(self.view.total_ctrl.GetValue(), '177.86')
        self.assertEqual(self.view.days_ctrl.GetValue(), '92')
        self.assertEqual(self.view.amt_ctrl.GetValue(), '7,363.45')
        self.assertEqual(self.view.paid_ctrl.GetValue(), False)
        self.assertEqual(self.view.balance_ctrl.GetValue(), '7,363.45')

    def testAddEntry(self):
        self.view.set_year(2020)
        self.view.set_qtr(1)

        self.presenter.run_query()

        # select an entry
        with patch('lib.ui_lib.show_error', return_value=None) as popup_mock:
            click_list_ctrl(self.view.list_ctrl, 5)

        # verify no salary popup not called
        popup_mock.assert_not_called()

        # verify details
        expected = {
            'dept': None,
            'admin_approved': False,
            'va_approved': False,
            'invoice_num': None,
            'short_code': None,
            'grant_admin': None,
            'grant_admin_email': None
        }
        self.assertEqual(self.view.get_form_values(), expected)

        # verify display only items
        self.assertEqual(self.view.prj_ctrl.GetValue(), 'Prj 315')
        self.assertEqual(self.view.emp_ctrl.GetValue(), 'BANKS,ERNEST')
        self.assertEqual(self.view.eff_ctrl.GetValue(), '20')
        self.assertEqual(self.view.frum_ctrl.GetValue(), '10/19')
        self.assertEqual(self.view.thru_ctrl.GetValue(), '12/19')
        self.assertEqual(self.view.salary_ctrl.GetValue(), '44,444')
        self.assertEqual(self.view.fringe_ctrl.GetValue(), '4.4')
        self.assertEqual(self.view.total_ctrl.GetValue(), '177.86')
        self.assertEqual(self.view.days_ctrl.GetValue(), '92')
        self.assertEqual(self.view.amt_ctrl.GetValue(), '3,272.65')
        self.assertEqual(self.view.paid_ctrl.GetValue(), False)
        self.assertEqual(self.view.balance_ctrl.GetValue(), '3,272.65')

        # edit details
        click_combobox_ctrl(self.view.dept_ctrl, 2)
        check_checkbox_ctrl(self.view.admin_approved_ctrl)
        check_checkbox_ctrl(self.view.va_approved_ctrl)
        enter_in_textbox_ctrl(self.view.invoice_ctrl, 'K0H0002')
        enter_in_textbox_ctrl(self.view.short_code_ctrl, '123456')
        click_combobox_ctrl(self.view.grant_admin_ctrl, 3)

        # verify grant admin email is done
        self.assertEqual(self.view.get_grant_admin_email(), 'harpo@umich.edu')

        with patch('dal.dao.Dao._Dao__write') as write_mock:
            write_mock.return_value = 4
            with patch('lib.ui_lib.show_msg') as popup_mock:
                popup_mock.return_value = None
                click_button(self.view.update_entry_btn)

        # verify the DB call
        self.assertEqual(write_mock.call_count, 1)
        args, kwargs = write_mock.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 0)
        sql = ("INSERT INTO ledger "
               "(quarter,dept,admin_approved,va_approved,invoice_num,"
               "asn_id,project,employee,salary,fringe,total_day,frum,thru,"
               "effort,days,amount,paid,balance,short_code,"
               "grant_admin,grant_admin_email) "
               "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)")
        vals = ['20201', 'CARDIOLOGY', '1', '1', 'K0H0002',
                '2396', 'Prj 315', 'BANKS,ERNEST', '44444', '4.4',
                '177.86', '1910', '1912', '20', '92', '3272.65',
                '0', '3272.65', '123456', 'MARX,HARPO', 'harpo@umich.edu'
        ]
        self.assertEqual(args[0], sql)
        self.assertEqual(args[1], vals)

        # verify user notification
        popup_mock.assert_called_once_with('Ledger updated!', 'Hooray')

        # verify list updated
        expected_item = Invoice({
            'admin_approved': True,
            'amount': 3272.65,
            'asn_id': 2396,
            'balance': 3272.65,
            'days': 92,
            'dept': 'CARDIOLOGY',
            'effort': 20,
            'employee': 'BANKS,ERNEST',
            'fringe': 4.4,
            'frum': '1910',
            'grant_admin': 'MARX,HARPO',
            'grant_admin_email': 'harpo@umich.edu',
            'id': 4,
            'invoice_num': 'K0H0002',
            'paid': False,
            'project': 'Prj 315',
            'quarter': 20201,
            'salary': 44444,
            'short_code': '123456',
            'thru': '1912',
            'total_day': 177.86,
            'va_approved': True
        })
        self.assertEqual(self.view.get_selection(), expected_item)

    def testUpdateEntry(self):
        self.view.set_year(2020)
        self.view.set_qtr(1)

        self.presenter.run_query()

        # select an entry
        with patch('lib.ui_lib.show_error', return_value=None) as popup_mock:
            click_list_ctrl(self.view.list_ctrl, 1)

        # verify no salary popup not called
        popup_mock.assert_not_called()

        # verify details
        expected = {
            'dept': None,
            'admin_approved': False,
            'va_approved': False,
            'invoice_num': None,
            'short_code': None,
            'grant_admin': None,
            'grant_admin_email': None
        }
        self.assertEqual(self.view.get_form_values(), expected)

        # verify display only items
        self.assertEqual(self.view.prj_ctrl.GetValue(), 'Prj 297')
        self.assertEqual(self.view.emp_ctrl.GetValue(), 'GEHRIG,HENRY LOUIS')
        self.assertEqual(self.view.eff_ctrl.GetValue(), '10')
        self.assertEqual(self.view.frum_ctrl.GetValue(), '10/19')
        self.assertEqual(self.view.thru_ctrl.GetValue(), '12/19')
        self.assertEqual(self.view.salary_ctrl.GetValue(), '104,971')
        self.assertEqual(self.view.fringe_ctrl.GetValue(), '33.5')
        self.assertEqual(self.view.total_ctrl.GetValue(), '537.18')
        self.assertEqual(self.view.days_ctrl.GetValue(), '92')
        self.assertEqual(self.view.amt_ctrl.GetValue(), '4,942.04')
        self.assertEqual(self.view.paid_ctrl.GetValue(), False)
        self.assertEqual(self.view.balance_ctrl.GetValue(), '4,942.04')

        # edit details
        click_combobox_ctrl(self.view.dept_ctrl, 2)
        check_checkbox_ctrl(self.view.admin_approved_ctrl)
        check_checkbox_ctrl(self.view.va_approved_ctrl)
        enter_in_textbox_ctrl(self.view.invoice_ctrl, 'K0H0002')
        enter_in_textbox_ctrl(self.view.short_code_ctrl, '123456')
        click_combobox_ctrl(self.view.grant_admin_ctrl, 3)

        # verify grant admin email is done
        self.assertEqual(self.view.get_grant_admin_email(), 'harpo@umich.edu')

        with patch('dal.dao.Dao._Dao__write') as write_mock:
            write_mock.return_value = 1
            with patch('lib.ui_lib.show_msg') as popup_mock:
                popup_mock.return_value = None
                click_button(self.view.update_entry_btn)

        # verify the DB call
        self.assertEqual(write_mock.call_count, 1)
        args, kwargs = write_mock.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 0)
        sql = ("UPDATE ledger "
               "SET dept=?,admin_approved=?,va_approved=?,invoice_num=?,short_code=?,grant_admin=?,grant_admin_email=? "
               "WHERE id=?;")
        vals = ['CARDIOLOGY', '1', '1', 'K0H0002', '123456', 'MARX,HARPO', 'harpo@umich.edu', 2]
        self.assertEqual(args[0], sql)
        self.assertEqual(args[1], vals)

        # verify user notification
        popup_mock.assert_called_once_with('Ledger updated!', 'Hooray')

        # verify list updated
        expected_item = Invoice({
            'admin_approved': True,
            'amount': 4942.04,
            'asn_id': 2272,
            'balance': 4942.04,
            'days': 92,
            'dept': 'CARDIOLOGY',
            'effort': 10,
            'employee': 'GEHRIG,HENRY LOUIS',
            'fringe': 33.5,
            'frum': '1910',
            'grant_admin': 'MARX,HARPO',
            'grant_admin_email': 'harpo@umich.edu',
            'id': 2,
            'invoice_num': 'K0H0002',
            'paid': False,
            'project': 'Prj 297',
            'quarter': 20201,
            'salary': 104971,
            'short_code': '123456',
            'thru': '1912',
            'total_day': 537.18,
            'va_approved': True
        })
        self.assertEqual(self.view.get_selection(), expected_item)

    def testGetTotalDays(self):
        # Quarter 1, 2020
        q_frum = '1910'
        q_thru = '1912'

        # First month only
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1910', '1910'), 31)

        # Second month only
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1911', '1911'), 30)

        # Third month only
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1912', '1912'), 31)

        # First 2 months
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1910', '1911'), 61)

        # Last 2 months
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1911', '1912'), 61)

        # Full quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1910', '1912'), 92)

        # Assignment starts before quarter, ends after first month
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1909', '1910'), 31)

        # Assignment starts before quarter, ends after second month
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1909', '1911'), 61)

        # Assignment starts before quarter, ends with quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1909', '1912'), 92)

        # Assignment starts in first month, ends past quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1910', '2001'), 92)

        # Assignment starts in second month, ends past quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1911', '2001'), 61)

        # Assignment starts in third month, ends past quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1912', '2001'), 31)

        # Assignment starts before quarter, ends after quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1909', '2001'), 92)

        # Quarter 2, 2020 (leap year)
        q_frum = '2001'
        q_thru = '2003'

        # First month only
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '2001', '2001'), 31)

        # Second month only
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '2002', '2002'), 29)

        # Third month only
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '2003', '2003'), 31)

        # First 2 months
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '2001', '2002'), 60)

        # Last 2 months
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '2002', '2003'), 60)

        # Full quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '2001', '2003'), 91)

        # Assignment starts before quarter, ends after first month
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1912', '2001'), 31)

        # Assignment starts before quarter, ends after second month
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1912', '2002'), 60)

        # Assignment starts before quarter, ends with quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1912', '2003'), 91)

        # Assignment starts in first month, ends past quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '2001', '2004'), 91)

        # Assignment starts in second month, ends past quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '2002', '2004'), 60)

        # Assignment starts in third month, ends past quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '2003', '2004'), 31)

        # Assignment starts before quarter, ends after quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1912', '2004'), 91)

        # Quarter 2, 2019 (non-leap year)
        q_frum = '1901'
        q_thru = '1903'

        # First month only
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1901', '1901'), 31)

        # Second month only
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1902', '1902'), 28)

        # Third month only
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1903', '1903'), 31)

        # First 2 months
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1901', '1902'), 59)

        # Last 2 months
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1902', '1903'), 59)

        # Full quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1901', '1903'), 90)

        # Assignment starts before quarter, ends after first month
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1812', '1901'), 31)

        # Assignment starts before quarter, ends after second month
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1812', '1902'), 59)

        # Assignment starts before quarter, ends with quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1812', '1903'), 90)

        # Assignment starts in first month, ends past quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1901', '1904'), 90)

        # Assignment starts in second month, ends past quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1902', '1904'), 59)

        # Assignment starts in third month, ends past quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1903', '1904'), 31)

        # Assignment starts before quarter, ends after quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '1812', '1904'), 90)

        # Quarter 3, 2020
        q_frum = '2004'
        q_thru = '2006'

        # First month only
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '2004', '2004'), 30)

        # Second month only
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '2005', '2005'), 31)

        # Third month only
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '2006', '2006'), 30)

        # First 2 months
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '2004', '2005'), 61)

        # Last 2 months
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '2005', '2006'), 61)

        # Full quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '2004', '2006'), 91)

        # Assignment starts before quarter, ends after first month
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '2003', '2004'), 30)

        # Assignment starts before quarter, ends after second month
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '2003', '2005'), 61)

        # Assignment starts before quarter, ends with quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '2003', '2006'), 91)

        # Assignment starts in first month, ends past quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '2004', '2007'), 91)

        # Assignment starts in second month, ends past quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '2005', '2007'), 61)

        # Assignment starts in third month, ends past quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '2006', '2007'), 30)

        # Assignment starts before quarter, ends after quarter
        self.assertEqual(self.presenter.get_total_days_asn(q_frum, q_thru, '2003', '2007'), 91)

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

        salary = 74971
        fringe = .439
        effort = 45
        ndays = 59
        cost = self.presenter.calculate_cost(salary, fringe, effort, ndays)
        self.assertEqual(cost, (10979.59, 413.54))
    #
    # def testImportSpreadsheet(self):
    #
    #     with patch('lib.excel_lib.get_file') as mock_get_file_dlg:
    #         mock_get_file_dlg.return_value = 'c:/bench/allocat/data/test_vista_billing.xls'
    #         with patch('presenters.ledger_presenter.LedgerPresenter.get_billing_month') as mock_popup:
    #             mock_popup.return_value = 'April FY20'
    #             click_button(self.view.update_entries_btn)
    #
    #     mock_get_file_dlg.assert_called_once_with(self.presenter.view)
    #
    #     sheet_names = [
    #         'May FY20', 'April FY20', 'March FY20', 'February FY20', 'January FY20',
    #         'December FY20', 'November FY20', 'October FY20', '4th QTR FY19', '3rd QTR FY19',
    #         '2nd QTR FY19', '1st QTR FY19', '4th QTR FY18', '3rd QTR FY18', '2nd QTR FY18',
    #         '1st QTR FY18'
    #     ]
    #     mock_popup.assert_called_once_with(sheet_names)
    #
    # def testImportSS(self):
    #     self.presenter.import_spreadsheet()
    #     pass
