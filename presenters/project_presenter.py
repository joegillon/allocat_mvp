import globals as gbl
from presenters.presenter import Presenter
from views.project_tab_panel import ProjectTabPanel
from event_handlers.event_handler import EventHandler


class ProjectPresenter(Presenter):

    def __init__(self, frame):
        model = gbl.dataset.prj_rex
        view = ProjectTabPanel(frame)
        actor = EventHandler()
        super().__init__(model, view, actor, 'Project')

    def load_combos(self):
            investigators = [rec for rec in gbl.dataset.emp_rex if rec.investigator]
            managers = [rec for rec in gbl.dataset.emp_rex if not rec.investigator]
            self.view.load_pi(investigators)
            self.view.load_pm(managers)

    def load_details(self):
        from dal.dao import Dao

        item = self.view.get_selection()
        if item:
            self.view.set_name(item.name)
            self.view.set_full_name(item.full_name)
            self.view.set_frum(item.frum)
            self.view.set_thru(item.thru)
            self.view.set_pi(item.investigator)
            self.view.set_pm(item.manager)
            self.view.set_notes(item.notes)
            if not item.asns:
                item.asns = item.get_asns(Dao())
            self.view.set_asn_list(item.asns)
            self.view.set_button_label('Update Project')

    def clear_model_values(self):
        self.view.set_full_name('')
        self.view.set_frum('')
        self.view.set_thru('')
        self.view.set_pi('')
        self.view.set_pm('')

    def get_form_values(self):
        return {
            'name': self.view.get_name(),
            'full_name': self.view.get_full_name(),
            'frum': self.view.get_frum(),
            'thru': self.view.get_thru(),
            'pi': self.view.get_pi(),
            'pm': self.view.get_pm(),
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
                if values['frum'] < min or values['thru'] > max:
                    err_msg = 'Assignment(s) out of new timeframe!'
        if err_msg:
            return err_msg

        return None

    def get_new_model_values(self, form_values):
        form_values['investigator_id'] = form_values['pi'].id
        form_values['investigator'] = form_values['pi'].name
        del form_values['pi']
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
