import globals as gbl
import lib.month_lib as ml
import lib.ui_lib as uil
from dal.dao import Dao
from models.ledger import Ledger
from models.assignment import Assignment
from views.ledger_panel import LedgerPanel
from event_handlers.ledger_event_handler import LedgerInteractor


class LedgerPresenter(object):

    def __init__(self, panel=None):
        # No panel is for testing
        if panel:
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

        self.view.load_depts([d for d in self.model.get_dept_data()])
        self.view.load_grant_admins([a.name for a in self.model.get_grant_admin_data()])

    def run_query(self):
        yr = self.view.get_year()
        qtr = self.view.get_qtr() + 1
        self.quarter =  '%s%d' % (yr, qtr)
        dao = Dao(stateful=True)
        rex = Ledger.get_rex(dao, self.quarter)
        prj_names = [r['project'] for r in rex]
        emp_names = [r['employee'] for r in rex]

        frum, thru = ml.get_quarter_interval(yr, qtr)
        asns = Assignment.get_for_timeframe(dao, frum, thru)
        dao.close()

        asns = [a for a in asns if not(a['employee'] in emp_names and a['project'] in prj_names)]
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
        per_hr = salary / 2087
        per_hr = per_hr * (1 + fringe)
        per_day =per_hr * 8
        per_asn = per_day * ndays
        return round(per_asn * effort / 100, 2), round(per_day, 2)

    def set_balance(self, paid):
        if paid:
            self.view.set_balance(0.0)
        else:
            self.view.reset_balance()
