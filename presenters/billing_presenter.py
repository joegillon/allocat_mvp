from datetime import date
import globals as gbl
import lib.month_lib as ml
import lib.ui_lib as uil
from dal.dao import Dao
from models.billing_report import BillingReport
from views.billing_tab_panel import BillTab
from views.billing_form_dlg import BillingFormDlg
from event_handlers.billing_event_handler import BillingInteractor


class BillingPresenter(object):

    def __init__(self, frame):
        self.view = BillTab(frame)
        self.dlg = BillingFormDlg(self.view, -1)
        actor = BillingInteractor()
        actor.install(self, self.view, self.dlg)
        self.init_view()

    def init_view(self):
        from datetime import datetime

        today = datetime.today()
        self.view.set_year(today.year)
        self.view.set_qtr(today.month)

        self.dlg.load_depts([d.name for d in gbl.dataset.get_dept_data()])
        self.dlg.load_projects([p.name for p in gbl.dataset.get_prj_data()])
        self.dlg.load_staff([e.name for e in gbl.dataset.get_emp_data()])
        self.dlg.load_grant_admins([a.name for a in gbl.dataset.get_grant_admin_data()])

    def run_query(self):
        yr = self.view.get_year()
        qtr = self.view.get_qtr() + 1
        rex = BillingReport.get_rex(Dao(), '%s%d' % (yr, qtr))
        self.view.load_grid(rex)

    def launch_form(self):
        self.dlg.ShowModal()
        self.dlg.Hide()

    def close_form(self):
        self.dlg.Hide()

    def save_form_data(self):
        self.dlg.Hide()
