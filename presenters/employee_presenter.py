import globals as gbl
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
            self.view.set_org(item.org)
            self.view.set_notes(item.notes)
            self.view.set_asn_list(item.asns)
            self.view.set_save_button_label('Update Employee')
            self.view.set_details_active(item.active, 'Employee')

    def clear_model_values(self):
        self.view.set_fte('')
        self.view.set_investigator(False)
        self.view.set_intern(False)
        self.view.set_org('CCMR')

    def get_form_values(self):
        return {
            'name': self.view.get_name(),
            'fte': self.view.get_fte(),
            'investigator': self.view.get_investigator(),
            'intern': self.view.get_intern(),
            'org': self.view.get_org(),
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

        return None

    def get_new_model_values(self, form_values):
        return form_values

    def update_model_values(self, model, form_values):
        model.name = form_values['name']
        model.fte = form_values['fte']
        model.investigator = form_values['investigator']
        model.intern = form_values['intern']
        model.org = form_values['org']
        model.notes = form_values['notes']

    def get_assignee_ctrl(self):
        import lib.ui_lib as uil

        return uil.ObjComboBox(self.view,
                               [rec for rec in gbl.dataset.prj_rex if rec.active],
                               'name',
                               'Project',
                               style=16)

    def get_assignee_str(self, asn):
        return 'Project: %s' % asn.project
