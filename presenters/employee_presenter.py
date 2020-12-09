import globals as gbl
from dal.dao import Dao
from models.employee import Employee
import lib.ui_lib as uil
from presenters.presenter import Presenter
from views.employee_tab_panel import EmployeeTabPanel
from event_handlers.event_handler import EventHandler


class EmployeePresenter(Presenter):

    def __init__(self, frame):
        get_model = gbl.dataset.get_emp_data
        view = EmployeeTabPanel(frame)
        actor = EventHandler()
        super().__init__(get_model, view, actor, 'Employee')
        gbl.dataset.bind_to('employees', self.refresh_list)

    def load_combos(self):
        pass

    def load_details(self):
        item = self.view.get_selection()
        if item:
            self.view.set_name(item.name)
            self.view.set_fte(item.fte)
            self.view.set_investigator(item.investigator)
            self.view.set_intern(item.intern)
            self.view.set_pm(item.pm)
            self.view.set_org(item.org)
            # self.view.set_va_email(item.va_email)
            # self.view.set_nonva_email(item.nonva_email)
            self.view.set_notes(item.notes)
            self.view.set_asn_list(item.asns)
            self.view.set_save_button_label('Update Employee')
            self.view.set_details_active(item.active, 'Employee')

    def clear_model_values(self):
        self.view.set_fte('')
        self.view.set_investigator(False)
        self.view.set_intern(False)
        self.view.set_org('CCMR')
        self.view.set_va_email('')
        self.view.set_nonva_email('')

    def get_form_values(self):
        return {
            'name': self.view.get_name(),
            'fte': self.view.get_fte(),
            'investigator': self.view.get_investigator(),
            'intern': self.view.get_intern(),
            'pm': self.view.get_pm(),
            'org': self.view.get_org(),
            # 'va_email': self.view.get_va_email(),
            # 'nonva_email': self.view.get_nonva_email(),
            'notes': self.view.get_notes()
        }

    def validate(self):
        import lib.validator_lib as vl

        values = self.get_form_values()
        emp = self.view.get_selection()
        emp_id = emp.id if emp else 0

        emp_match = vl.EmployeeMatch(emp_id, gbl.dataset.emp_names)
        err_msg = vl.validate_emp_name(values['name'], emp_match)
        if err_msg:
            return err_msg

        err_msg = vl.validate_fte(values['fte'])
        if err_msg:
            return err_msg

        # err_msg = vl.validate_va_email(values['va_email'])
        # if err_msg:
        #     return err_msg
        #
        # err_msg = vl.validate_email(values['nonva_email'])
        # if err_msg:
        #     return err_msg

        return None

    def get_new_model_values(self, form_values):
        return form_values

    def update_model_values(self, model, form_values):
        model.name = form_values['name']
        model.fte = form_values['fte']
        model.investigator = form_values['investigator']
        model.intern = form_values['intern']
        model.pm = form_values['pm']
        model.org = form_values['org']
        # model.va_email = form_values['va_email']
        # model.nonva_email = form_values['nonva_email']
        model.notes = form_values['notes']

    def get_assignee_ctrl(self):
        import lib.ui_lib as uil

        return uil.ObjComboBox(self.view,
                               gbl.dataset.get_prj_data(),
                               'name',
                               'Project',
                               style=16)

    def get_assignee_str(self, asn):
        return 'Project: %s' % asn.project

    def add_model(self, form_values):
        new_model = Employee(self.get_new_model_values(form_values))

        try:
            new_model.id = new_model.add(Dao())
        except Exception as ex:
            uil.show_error(str(ex))
            return

        uil.show_msg('Employee added!', 'Hallelujah!')

    def update_model(self, form_values):
        model = self.model[self.view.get_selected_idx()]
        try:
            model.update(Dao(), form_values)
        except Exception as ex:
            uil.show_error(str(ex))
            return

        uil.show_msg('Employee updated!', 'Hallelujah!')
