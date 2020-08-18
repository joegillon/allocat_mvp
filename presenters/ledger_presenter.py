from datetime import date
import globals as gbl
import lib.month_lib as ml
import lib.ui_lib as uil
from dal.dao import Dao
from models.billing_report import BillingReport
from models.assignment import Assignment
from views.billing_tab_panel import BillTab
from views.billing_form_dlg import BillingFormDlg
from event_handlers.billing_event_handler import BillingInteractor


class LedgerPresenter(object):

    def __init__(self, frame):
        self.view = frame
        self.dlg = BillingFormDlg(self.view, -1)
        actor = BillingInteractor()
        actor.install(self, self.view, self.dlg)
        self.init_view()
        self.selected_rownum = -1

    def init_view(self):
        from datetime import datetime

        today = datetime.today()
        self.view.set_year(today.year)
        self.view.set_qtr(today.month)

        self.dlg.load_depts([d for d in gbl.dataset.get_dept_data()])
        self.dlg.load_grant_admins([a for a in gbl.dataset.get_grant_admin_data()])

    def run_query(self):
        yr = self.view.get_year()
        qtr = self.view.get_qtr() + 1
        dao = Dao(stateful=True)
        rex = BillingReport.get_rex(dao, '%s%d' % (yr, qtr))
        prj_names = [r['project'] for r in rex]
        emp_names = [r['staff'] for r in rex]

        frum, thru = ml.get_quarter_interval(yr, qtr)
        asns = Assignment.get_for_timeframe(dao, frum, thru)
        dao.close()

        asns = [a for a in asns if not(a['employee'] in emp_names and a['project'] in prj_names)]
        new_rex = [
            {
                'id': None,
                'quarter': '',
                'department': '',
                'admin_approved': False,
                'va_approved': False,
                'invoice_num': '',
                'project': a['project'],
                'staff': a['employee'],
                'pct_effort': a['effort'],
                'salary': None,
                'fringe': None,
                'total_day': None,
                'days': self.get_total_days_asn(frum, thru, a['frum'], a['thru']),
                'amount': None,
                'frum': ml.frum2dt(a['frum']),
                'thru': ml.thru2dt(a['thru']),
                'paid': False,
                'balance': None,
                'short_code': '',
                'grant_admin': '',
                'grant_admin_email': ''
            } for a in asns
        ]

        rex = rex + new_rex
        self.view.load_grid(rex)

    def launch_form(self, rownum, colnum):
        self.selected_rownum = rownum
        data = self.view.get_row(rownum)
        self.dlg.load_data(data)
        self.dlg.ShowModal()
        self.dlg.Hide()

    def close_form(self):
        self.dlg.Hide()

    def save_form_data(self):
        form_values = self.dlg.get_form_values()
        self.view.set_row(self.selected_rownum, form_values)
        self.dlg.Hide()

    def get_total_days_asn(self, qtr_frum, qtr_thru, asn_frum, asn_thru):
        frum = asn_frum if  asn_frum > qtr_frum else qtr_frum
        thru = asn_thru if asn_frum < qtr_thru else qtr_frum
        return ml.get_total_days(frum, thru)


    # def set_grant_admin_email(self, name):
    #     email = [x.email for x in self.grant_admins if x.name == name]
    #     email = email[0] if email else ''
    #     self.view.set_grant_admin_email(email)
