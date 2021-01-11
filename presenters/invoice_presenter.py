import globals as gbl
import lib.month_lib as ml
import lib.ui_lib as uil
from dal.dao import Dao
from models.invoice import Invoice
from views.invoice_panel import InvoicePanel
from event_handlers.invoice_event_handler import InvoiceEventHandler


class InvoicePresenter(object):

    def __init__(self, panel):
        self.view = InvoicePanel(panel)
        actor = InvoiceEventHandler()
        actor.install(self, self.view)

        self.quarter = ''

        self.init_view()

    def init_view(self):
        yr, qtr = self.get_init_quarter()
        self.view.set_year(yr)
        self.view.set_qtr(qtr)

        self.view.load_depts([d.name for d in gbl.dataset.get_dept_data()])
        self.view.load_grant_admins([a.name for a in gbl.dataset.get_grant_admin_data()])

    def get_init_quarter(self):
        from datetime import datetime

        today = datetime.today()
        return today.year, ml.get_quarter(today.month)

    def get_query_params(self):
        yr = self.view.get_year()
        qtr = self.view.get_qtr()
        frum, thru = ml.get_quarter_interval(yr, qtr)
        self.quarter = int('%d%d' % (yr, qtr))
        return frum, thru

    def run_query(self):
        qtr_frum, qtr_thru = self.get_query_params()

        # Get ledger records for quarter
        ledger_rex = gbl.dataset.get_unsent_invoices(self.quarter)

        # Get the assignment ids for the assignments already in the ledger
        ledger_asn_ids = [rec.asn_id for rec in ledger_rex]

        # Get the billable assignments for quarter
        asns = gbl.dataset.get_asn_data(self.quarter)

        # Get the assignments not already in the ledger
        asns = [a for a in asns if a.id not in ledger_asn_ids]

        # Need new ledger records for assignments not already in the ledger
        new_rex = []
        for asn in asns:
            emp = gbl.dataset.get_emp_rec(asn.employee_id)
            days = self.get_total_days_asn(qtr_frum, qtr_thru, asn.frum, asn.thru)
            amt, day_total = self.calculate_cost(emp.salary, emp.fringe, asn.effort, days)
            new_rec = Invoice({
                'id': None,
                'quarter': self.quarter,
                'dept': None,
                'admin_approved': 0,
                'va_approved': 0,
                'invoice_num': None,
                'project': asn.project,
                'employee': asn.employee,
                'effort': asn.effort,
                'salary': emp.salary,
                'fringe': emp.fringe,
                'total_day': day_total,
                'days': days,
                'amount': amt,
                'frum': asn.frum if asn.frum > qtr_frum else qtr_frum,
                'thru': asn.thru if asn.thru < qtr_thru else qtr_thru,
                'paid': 0,
                'balance': amt,
                'short_code': None,
                'grant_admin': None,
                'grant_admin_email': None,
                'asn_id': asn.id
            })
            new_rex.append(new_rec)

        # Combine the records already in ledger with the new ones
        model = ledger_rex + new_rex
        gbl.dataset.set_unsent_invoices(model)

        # Update the view
        self.view.load_grid(model)

    def load_details(self):
        item = self.view.get_selection()
        if not item:
            return
        if not item.salary or not item.fringe:
            emp_rec = gbl.dataset.get_emp_rec_by_name(item.employee)
            item.salary = emp_rec.salary
            if not item.salary:
                uil.show_error('%s has no salary! Not imported?' % (item.employee,))
            else:
                item.fringe = emp_rec.fringe
                item.amount, item.total_day = self.calculate_cost(
                    item.salary, item.fringe, item.effort, item.days
                )
                if not item.balance:
                    item.balance = item.amount
        self.view.load_form(item)

    def get_total_days_asn(self, qtr_frum, qtr_thru, asn_frum, asn_thru):
        frum = asn_frum if asn_frum > qtr_frum else qtr_frum
        thru = asn_thru if asn_thru < qtr_thru else qtr_thru
        return ml.get_total_days(frum, thru)

    def set_grant_admin_email(self, name):
        grant_admins = gbl.dataset.get_grant_admin_data()
        email = [x.email for x in grant_admins if x.name == name]
        email = email[0] if email else ''
        self.view.set_grant_admin_email(email)

    def run_import(self):
        uil.show_msg('Not yet implemented.', 'Someday!')

    def run_va_emails(self):
        uil.show_msg('Not yet implemented.', 'Someday!')

    def run_ga_emails(self):
        uil.show_msg('Not yet implemented.', 'Someday!')

    def run_script(self):
        uil.show_msg('Not yet implemented.', 'Someday!')

    def update_entry(self):
        form_vals = self.view.get_form_values()
        obj = self.view.get_selection()
        updatable_flds = [
            'dept', 'admin_approved', 'va_approved', 'invoice_num',
            'short_code', 'grant_admin', 'grant_admin_email'
        ]
        for fld in updatable_flds:
            setattr(obj, fld, form_vals[fld])

        if obj.id:
            result = obj.update(Dao())
        else:
            result = obj.add(Dao())

        self.view.reload_entry(obj)

        uil.show_msg('Ledger updated!', 'Hooray')

    def calculate_cost(self, salary, fringe, effort, ndays):
        if not salary or not fringe:
            return None, None
        if fringe > 1:
            fringe = round(fringe * .01, 3)
        per_hr = (salary / 2087) * (1 + fringe)
        per_day = per_hr * 8
        per_asn = per_day * ndays
        return round(per_asn * effort / 100, 2), round(per_day, 2)

    def set_balance(self, paid):
        if paid:
            self.view.set_balance(0.0)
        else:
            self.view.reset_balance()

    def update_entries(self):
        from dal.dao import Dao
        from models.invoice import Invoice

        dao = Dao(stateful=True)

        invoice_rex = self.import_spreadsheet()

        for invoice_rec in list(invoice_rex):
            ledger_rec = Invoice.get_by_invoice(dao, invoice_rec.invoice_num)
            if ledger_rec:
                ledger_rec.update_balance(dao, invoice_rec.amount)

        new_rex = Invoice.get_rex(dao)

        dao.close()

        gbl.dataset.set_ledger_data(new_rex)
        self.init_view()

    # def import_spreadsheet(self):
    #     import lib.excel_lib as xl
    #     from models.billing_record import BillingRecord
    #     from views.billing_ss_dlg import BillingSSDlg
    #
    #     file = xl.get_file(self.view)
    #     if not file:
    #         return
    #
    #     wb = xl.open_wb(file)
    #     sheetnames = wb.sheet_names()
    #
    #     billing_month = self.get_billing_month(sheetnames)
    #
    #     rex = []
    #     last_idx = sheetnames.index(billing_month)
    #     for idx in range(0, last_idx + 1):
    #         sh = wb.sheet_by_index(idx)
    #
    #         nrows = sum(1 for _ in sh.get_rows())
    #         for rownum in range(0, nrows):
    #             if sh.cell_value(rownum, 1).startswith('506'):
    #                 rex.append(BillingRecord(sh.row_values(rownum)))
    #
    #     return rex
    #
    def import_spreadsheet(self):
        import lib.excel_lib as xl
        from models.deposit import Deposit

        # file = xl.get_file(self.view)
        # if not file:
        #     return

        file = 'c:/bench/allocat/data/test_deposits.xls'
        wb = xl.open_wb(file)
        sheets = wb.sheet_names()

        rex = []
        dao = Dao(stateful=True)
        # last_idx = sheetnames.index(billing_month)
        for idx in reversed(range(0, len(sheets))):
            sh = wb.sheet_by_index(idx)

            nrows = sum(1 for _ in sh.get_rows())
            for rownum in range(0, nrows):
                if sh.cell_value(rownum, 1).startswith('506'):
                    ss_rec = Deposit(sh.row_values(rownum))
                    if ss_rec.invoice_num == 'K8H1025':
                        print('boo')
                    # if not ss_rec.invoice_num.startswith('K0'):
                    #     continue
                    try:
                        db_rec = Deposit.get_by_invoice_num(dao, ss_rec.invoice_num)
                    except Exception as ex:
                        print(str(ex))
                    if not db_rec:
                        ss_rec.add(dao)
                        rex.append(ss_rec)
        dao.close()
        return rex

    def get_billing_month(self, sheetnames):
        from views.billing_ss_dlg import BillingSSDlg

        dlg = BillingSSDlg(self.view, -1, sheetnames)
        dlg.ShowModal()
        month = dlg.result
        dlg.Destroy()
        return month
