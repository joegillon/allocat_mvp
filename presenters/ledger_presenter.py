import globals as gbl
import lib.month_lib as ml
import lib.ui_lib as uil
from dal.dao import Dao
from models.ledger import Ledger
from models.assignment import Assignment
from views.ledger_panel import LedgerPanel
from event_handlers.ledger_event_handler import LedgerInteractor


class LedgerPresenter(object):

    def __init__(self, panel):
        self.view = LedgerPanel(panel)
        self.model = gbl.dataset
        actor = LedgerInteractor()
        actor.install(self, self.view)

        self.quarter = ''

        self.init_view()

    def init_view(self):
        from datetime import datetime

        today = datetime.today()
        self.view.set_year(today.year)
        self.view.set_qtr(today.month)

        self.view.load_depts([d.name for d in self.model.get_dept_data()])
        self.view.load_grant_admins([a.name for a in self.model.get_grant_admin_data()])

    def get_query_params(self):
        yr = self.view.get_year()
        qtr = self.view.get_qtr()
        self.quarter = '%d%d' % (yr, qtr)
        frum, thru = ml.get_quarter_interval(yr, qtr)
        return self.quarter, frum, thru

    def run_query(self):
        qtr, frum, thru = self.get_query_params()

        dao = Dao(stateful=True)
        rex = Ledger.get_rex(dao, qtr)

        ledger_ids = [rec.id for rec in rex]

        asns = Assignment.get_billables(dao, frum, thru)
        dao.close()

        asns = [a for a in asns if a['id'] not in ledger_ids]
        new_rex = [
            {
                'id': None,
                'quarter': self.quarter,
                'dept': '',
                'admin_approved': False,
                'va_approved': False,
                'invoice_num': '',
                'project': a['project'],
                'employee': a['employee'],
                'effort': a['effort'],
                'salary': None,
                'fringe': None,
                'total_day': None,
                'days': self.get_total_days_asn(frum, thru, a['frum'], a['thru']),
                'amount': None,
                'frum': ml.frum2str(a['frum']),
                'thru': ml.thru2str(a['thru']),
                'paid': False,
                'balance': None,
                'short_code': '',
                'grant_admin': '',
                'grant_admin_email': '',
                'asn_id': a['id']
            } for a in asns
        ]

        rex = rex + new_rex
        model = [Ledger(rec) for rec in rex] if rex else []
        gbl.dataset.set_ledger_data(model)
        self.view.load_grid(model)

    def reload(self):
        new_data = Ledger.get_rex(Dao())
        gbl.dataset.set_ledger_data(new_data)
        self.view.load_grid(self.model.get_ledger_data())
        uil.show_msg('Reloaded!','Try Again')

    def load_details(self):
        item = self.view.get_selection()
        if not item:
            return
        if not item.salary or not item.fringe:
            emp_rec = gbl.dataset.get_emp_rec(item.employee)
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
        frum = asn_frum if  asn_frum > qtr_frum else qtr_frum
        thru = asn_thru if asn_frum < qtr_thru else qtr_frum
        return ml.get_total_days(frum, thru)

    def set_grant_admin_email(self, name):
        grant_admins = self.model.get_grant_admin_data()
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
            'paid', 'balance', 'short_code', 'grant_admin', 'grant_admin_email'
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
        from models.ledger import Ledger

        dao = Dao(stateful=True)

        billing_rex = self.import_spreadsheet()

        for billing_rec in list(billing_rex):
            ledger_rec = Ledger.get_by_invoice(dao, billing_rec.invoice_num)
            if ledger_rec:
                ledger_rec.update_balance(dao, billing_rec.amount)

        new_rex = Ledger.get_rex(dao)

        dao.close()

        gbl.dataset.set_ledger_data(new_rex)
        self.init_view()

    def import_spreadsheet(self):
        import lib.excel_lib as xl
        from models.billing_record import BillingRecord
        from views.billing_ss_dlg import BillingSSDlg

        file = xl.get_file(self.view)
        if not file:
            return

        wb = xl.open_wb(file)
        sheets = wb.sheet_names()

        dlg = BillingSSDlg(self.view, -1, sheets)
        dlg.ShowModal()
        stop_at = dlg.result
        dlg.Destroy()

        rex = []
        last_idx = sheets.index(stop_at)
        for idx in range(0, last_idx + 1):
            sh = wb.sheet_by_index(idx)

            nrows = sum(1 for _ in sh.get_rows())
            for rownum in range(0, nrows):
                if sh.cell_value(rownum, 1).startswith('506'):
                    rex.append(BillingRecord(sh.row_values(rownum)))

        return rex
