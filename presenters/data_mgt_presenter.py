from views.data_mgt_panel import DataMgtPanel
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
        self.view.set_dept_list(gbl.dataset.get_dept_data())
        self.view.set_admin_list(gbl.dataset.get_grant_admin_data())

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
