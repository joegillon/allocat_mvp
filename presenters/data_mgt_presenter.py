from views.data_mgt_panel import DataMgtPanel
from views.pm_dlg import PmDlg
import globals as gbl
import lib.validator_lib as vl
import lib.ui_lib as uil
from dal.dao import Dao
from models.department import Department
from event_handlers.data_mgt_event_handler import DataMgtInteractor


class DataMgtPresenter(object):

    def __init__(self, panel=None):
        # No panel is for testing
        if panel:
            self.view = DataMgtPanel(panel, self)
            self.model = gbl.dataset
            actor = DataMgtInteractor()
            actor.install(self, self.view)
            self.init_view()

    def init_view(self):
        self.set_emp_lists()
        self.view.set_dept_list(gbl.dataset.get_dept_data())
        self.view.set_admin_list(gbl.dataset.get_grant_admin_data())

    def set_emp_lists(self):
        emps = gbl.dataset.get_emp_data()
        self.view.set_emp_list(emps)
        self.view.set_pm_list([emp for emp in emps if emp.pm])

    def add_pm(self):
        emp = self.view.get_emp_selection()
        dlg = PmDlg(self.view, emp)
        dlg.ShowModal()

        if dlg.emp.pm:
            dlg.emp.update_pm(Dao())
            self.set_emp_lists()

        dlg.Destroy()
        uil.show_msg('PM updated!', 'Yippee!')

    def update_pm_va_email(self, emp, value):
        err_msg = vl.validate_va_email(value)
        if err_msg:
            uil.show_error(err_msg)
            self.view.focus_pm_va_email()
            return

        if not emp.name:
            uil.show_error('PM name missing!')
            return

        emp.va_email = value
        emp.update_pm(Dao())

    def update_pm_nonva_email(self, emp, value):
        if not vl.validate_email(value):
            uil.show_error('Invalid non-VA email!')
            return

        if not emp.name:
            uil.show_error('PM name missing!')
            return

        emp.nonva_email = value
        emp.update_pm(Dao())

    def pm_dlg(self, emp):
        dlg = PmDlg(self.view, emp)
        dlg.ShowModal()

        if dlg.emp.pm:
            dlg.emp.update_pm(Dao())
            self.set_emp_lists()

        dlg.Destroy()
        uil.show_msg('PM updated!', 'Yippee!')

    def drop_pm(self):
        pass

    def add_dept(self):
        self.view.add_dept(Department())

    def update_dept(self, obj, value):
        obj.name = value.upper()
        if not obj.name:
            uil.show_error('Department name missing!')
            return

        if obj.id:
            obj.update(Dao())
        else:
            obj.id = obj.add(Dao())

    def drop_dept(self):
        obj = self.view.get_dept_selection()
        obj.drop(Dao())
        self.view.drop_dept(obj)

    def update_admin(self, obj, value):
        err_msg = vl.validate_name(value)
        if err_msg:
            uil.show_error(err_msg)
            return

        obj.name = value.upper()
        if obj.id:
            obj.update(Dao())
        else:
            obj.add(Dao())

    def update_admin_email(self, obj, value):
        if not vl.validate_email(value):
            uil.show_error('Invalid email!')
            return

        if not obj.name:
            uil.show_error('Admin name missing!')
            return

        obj.email = value
        if obj.id:
            obj.update(Dao())
        else:
            obj.add(Dao())

    def drop_admin(self):
        obj = self.view.get_admin_selection()
        obj.drop(Dao())
        self.view.drop_admin(obj)
