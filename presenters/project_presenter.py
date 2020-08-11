import globals as gbl
import lib.ui_lib as uil
from dal.dao import Dao
from presenters.presenter import Presenter
from views.project_tab_panel import ProjectTabPanel
from event_handlers.event_handler import EventHandler
from event_handlers.grant_admin_event_handler import GrantAdminInteractor


class ProjectPresenter(Presenter):

    def __init__(self, frame):
        get_model = gbl.dataset.get_prj_data
        view = ProjectTabPanel(frame)
        actor = EventHandler()
        super().__init__(get_model, view, actor, 'Project')
        gbl.dataset.bind_to('projects', self.refresh_list)
        grant_admin_actor = GrantAdminInteractor()
        grant_admin_actor.install(self, view)

    def load_combos(self):
        emp_rex = gbl.dataset.get_emp_data()
        investigators = [rec for rec in emp_rex if rec.investigator]
        managers = [rec for rec in emp_rex if not rec.investigator]
        depts = gbl.dataset.get_dept_data()
        self.grant_admins = gbl.dataset.get_grant_admin_data()
        self.view.load_pi(investigators)
        self.view.load_pm(managers)
        self.view.load_depts(depts)
        self.view.load_grant_admins(self.grant_admins)

    def load_details(self):
        item = self.view.get_selection()
        if item:
            self.view.set_name(item.name)
            self.view.set_full_name(item.full_name)
            self.view.set_frum(item.frum)
            self.view.set_thru(item.thru)
            self.view.set_dept(item.dept)
            self.view.set_short_code(item.short_code)
            self.view.set_pi(item.investigator)
            self.view.set_pm(item.manager)
            self.view.set_grant_admin(item.grant_admin)
            self.view.set_grant_admin_email(item.grant_admin_email)
            self.view.set_notes(item.notes)
            self.view.set_asn_list(item.asns)
            self.view.set_save_button_label('Update Project')
            self.view.set_details_active(item.active, 'Project')

    def clear_model_values(self):
        self.view.set_full_name('')
        self.view.set_frum('')
        self.view.set_thru('')
        self.view.set_dept('')
        self.view.set_short_code('')
        self.view.set_pi('')
        self.view.set_pm('')
        self.view.set_grant_admin('')
        self.view.set_grant_admin_email('')

    def get_form_values(self):
        return {
            'name': self.view.get_name(),
            'full_name': self.view.get_full_name(),
            'frum': self.view.get_frum(),
            'thru': self.view.get_thru(),
            'dept': self.view.get_dept(),
            'short_code': self.view.get_short_code(),
            'pi': self.view.get_pi(),
            'pm': self.view.get_pm(),
            'grant_admin': self.view.get_grant_admin(),
            'grant_admin_email': self.view.get_grant_admin_email(),
            'notes': self.view.get_notes()
        }

    def validate(self):
        import lib.validator_lib as vl
        import lib.month_lib as ml

        values = self.get_form_values()
        prj = self.view.get_selection()
        prj_id = prj.id if prj else 0

        prj_match = vl.ProjectMatch(prj_id, gbl.dataset.prj_names)
        err_msg = vl.validate_prj_name(values['name'], prj_match)
        if err_msg:
            return err_msg

        prj_match = vl.ProjectMatch(prj_id, gbl.dataset.prj_full_names)
        err_msg = vl.validate_prj_full_name(values['full_name'], prj_match)
        if err_msg:
            return err_msg

        err_msg = vl.validate_timeframe(values['frum'], values['thru'])
        if err_msg:
            return err_msg

        if prj and prj.asns:
            if values['frum'] < prj.frum or \
                            values['thru'] > prj.thru:
                min, max = ml.get_timeframe_edges(prj.asns)
                if values['frum'] > min or values['thru'] < max:
                    err_msg = 'Assignment(s) out of new timeframe!'
        if err_msg:
            return err_msg

        err_msg = vl.validate_email(values['grant_admin_email'])
        if err_msg:
            return 'Invalid Grant Admin Email!'

        if values['grant_admin_email'] and not values['grant_admin']:
            return 'Grant Admin Email Without a Grant Admin!'

        err_msg = vl.validate_short_code(values['short_code'])
        if err_msg:
            return err_msg

        return None

    def get_new_model_values(self, form_values):
        form_values['investigator_id'] = None
        form_values['investigator'] = None
        if form_values['pi']:
            form_values['investigator_id'] = form_values['pi'].id
            form_values['investigator'] = form_values['pi'].name
        del form_values['pi']

        form_values['manager_id'] = None
        form_values['manager'] = None
        if form_values['pm']:
            form_values['manager_id'] = form_values['pm'].id
            form_values['manager'] = form_values['pm'].name
        del form_values['pm']
        return form_values

    def update_model_values(self, prj, form_values):
        prj.full_name = form_values['full_name']
        prj.frum = form_values['frum']
        prj.thru = form_values['thru']
        prj.investigator_id = form_values['pi'].id
        prj.investigator = form_values['pi'].name
        prj.manager_id = form_values['pm'].id
        prj.manager = form_values['pm'].name

    def get_assignee_ctrl(self):
        import lib.ui_lib as uil

        return uil.ObjComboBox(self.view,
                               gbl.dataset.get_emp_data(),
                               'name',
                               'Employee',
                               style=16)

    def get_assignee_str(self, asn):
        return 'Employee: %s' % asn.employee

    def add_model(self, form_values):
        from models.project import Project

        new_model = Project(self.get_new_model_values(form_values))

        try:
            new_model.id = new_model.add(Dao())
        except Exception as ex:
            uil.show_error(str(ex))
            return

        uil.show_msg('Project added!', 'Hallelujah!')

    def update_model(self, form_values):
        model = self.model[self.view.get_selected_idx()]
        try:
            model.update(Dao(), form_values)
        except Exception as ex:
            uil.show_error(str(ex))
            return

        uil.show_msg('Project updated!', 'Hallelujah!')

    def set_grant_admin_email(self, name):
        email = [x.email for x in self.grant_admins if x.name == name]
        email = email[0] if email else ''
        self.view.set_grant_admin_email(email)