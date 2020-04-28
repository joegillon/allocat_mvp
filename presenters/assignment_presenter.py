import lib.month_lib as ml
import lib.validator_lib as vl
from views.assignment_panel import AssignmentPanel
from event_handlers.assignment_event_handler import AssignmentInteractor


class AssignmentPresenter(object):

    def __init__(self, dlg, owner, assignee, asn=None):
        self.view = AssignmentPanel(dlg)
        self.actor = AssignmentInteractor()
        self.owner = owner
        self.assignee = assignee
        self.asn = asn

    def go(self):
        self.actor.install(self, self.view)
        self.is_listening = True
        self.init_view()

    def init_view(self):
        self.view.set_owner(self.owner.name)
        self.view.set_assignee(self.assignee)
        if self.asn:
            self.view.set_frum(ml.prettify(self.asn.frum))
            self.view.set_thru(ml.prettify(self.asn.thru))
            self.view.set_effort(self.asn.effort)
            self.view.set_notes(self.asn.notes)
            self.view.frum_ctrl.SetFocus()

    def is_valid(self, form_values):
        import globals as gbl

        if not form_values['employee_id']:
            vl.showErrMsg(None, 'Employee is required!')
            return False

        if not form_values['project_id']:
            vl.showErrMsg(None, 'Project is required!')
            return False

        prj = [p for p in gbl.dataset._prj_rex if p.id == form_values['project_id']][0]
        err_msg = vl.validate_asn_timeframe(
            form_values['frum'], form_values['thru'], prj)
        if err_msg:
            ctrl = self.view.frum_ctrl
            if err_msg.startswith('Thru'):
                ctrl = self.view.thru_ctrl
            vl.showErrMsg(ctrl, err_msg)
            return False
        err_msg = vl.validate_effort(form_values['effort'])
        if err_msg:
            vl.showErrMsg(self.view.effort_ctrl, err_msg)
            return False

        return True

    def save(self):
        from dal.dao import Dao
        from models.assignment import Assignment
        import wx
        import globals as gbl

        form_values = self.get_form_values()
        if self.is_valid(form_values):
            try:
                if self.asn:
                    self.asn.from_dict(form_values)
                    self.asn.update(Dao())
                else:
                    self.asn = Assignment(form_values)
                    self.asn.add(Dao())
            except Exception as ex:
                vl.showErrMsg(None, str(ex))
                return

            wx.MessageBox('Assignment saved!', 'Hallelujah!', wx.OK)
            self.view.Parent.Close()

    def cancel(self):
        self.view.Parent.Close()

    def get_form_values(self):
        if hasattr(self.owner, 'fte'):
            employee_id = self.owner.id
            prj = self.assignee.get_selection()
            project_id = prj.id if prj else None
        else:
            if type(self.assignee) == str:
                employee_id = self.asn.employee_id
            else:
                employee_id = self.assignee.get_selection().id
            project_id = self.owner.id
        return {
            'employee_id': employee_id,
            'project_id': project_id,
            'frum': self.view.get_frum(),
            'thru': self.view.get_thru(),
            'effort': self.view.get_effort(),
            'notes': self.view.get_notes()
        }