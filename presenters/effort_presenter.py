from datetime import date
import globals as gbl
import lib.month_lib as ml
import lib.ui_lib as uil
from views.effort_tab_panel import EffTab
from event_handlers.effort_event_handler import EffortEventHandler


class PercentEffort(object):
    def __init__(self, prj, percent):
        self.prj = prj
        self.percent = percent


class EffCell(object):
    def __init__(self, month):
        self.month = month
        self.total = 0
        self.efforts = []


class EffRow(object):
    def __init__(self, employee):
        self.employee = employee
        self.cells = []


class EffortPresenter(object):

    def __init__(self, frame):
        self.model = gbl.dataset.asn_rex
        self.view = EffTab(frame)
        actor = EffortEventHandler()
        actor.install(self, self.view)
        self.emp_dict = {emp.id: emp for emp in gbl.dataset.emp_rex}
        self.init_view()

    def init_view(self):
        frum, thru = self.get_init_dates()
        self.view.set_frum(frum)
        self.view.set_thru(thru)
        self.run_query()

    def get_init_dates(self):
        frum = date.today()
        thru = ml.date_plus(frum, 11)
        return ml.d2month(frum), ml.d2month(thru)

    def run_query(self):
        frum = self.view.get_frum()
        thru = self.view.get_thru()
        months = ml.get_months(frum, thru)
        rows, self.breakdowns = self.build_dataset(frum, thru, months)
        self.view.load_grid(months, rows)

    def build_dataset(self, frum, thru, months):
        rows = []
        ugly_months = [ml.uglify(month) for month in months]
        for emp in gbl.dataset.emp_rex:
            row = EffRow(emp)
            for month in ugly_months:
                cell = EffCell(month)
                for asn in emp.asns:
                    if month >= asn.frum and month <= asn.thru:
                        cell.total += asn.effort
                        cell.efforts.append(PercentEffort(asn.project, asn.effort))
                row.cells.append(cell)
            rows.append(row)

        breakdowns = self.build_breakdowns(rows)

        return rows, breakdowns

    def build_breakdowns(self, rows):
        d = {}
        for row in rows:
            for cell in row.cells:
                k = '%s:%s' % (row.employee.id, cell.month)
                d[k] = [(pe.prj, pe.percent) for pe in cell.efforts]
                # d[k] = [{'project': pe.prj, 'percent': pe.percent} for pe in cell.efforts]
        return d

    def show_emp_breakdown(self, row):
        from views.emp_brkdwn_dlg import EmployeeBreakdownDlg

        emp_id = self.view.get_emp_id(row)
        if not self.emp_dict[emp_id].asns:
            uil.show_error('No assignments!')
            return
        if gbl.active_only:
            asns = [asn for asn in self.emp_dict[emp_id].asns if asn.active]
        else:
            asns = self.emp_dict[emp_id].asns

        total = 0
        items = []
        for asn in asns:
            items.append((
                asn.project,
                ml.prettify(asn.frum),
                ml.prettify(asn.thru),
                asn.effort))
            total += asn.effort

        dlg = EmployeeBreakdownDlg(self.view, -1, items)
        s = '%d assignments for %s' % (len(asns), self.emp_dict[emp_id].name)
        dlg.set_name_lbl(s)

        s = 'Total effort: %d' % total
        dlg.set_total_lbl(s)

        dlg.ShowModal()

    def show_month_breakdown(self, col, row):
        from views.month_brkdwn_dlg import MonthBreakdownDialog

        emp_id = self.view.get_emp_id(row)
        empName = self.view.get_emp_name(row)
        month = self.view.get_selected_month(col)
        key = str(emp_id) + ':' + month
        dlg = MonthBreakdownDialog(self.view, -1, empName, ml.prettify(month), self.breakdowns[key])
        dlg.ShowModal()
