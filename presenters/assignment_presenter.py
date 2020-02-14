import lib.month_lib as ml
import globals as gbl
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
        self.view.set_owner(self.owner)
        self.view.set_assignee(self.assignee)
        if self.asn:
            self.view.set_frum(ml.prettify(self.asn.frum))
            self.view.set_thru(ml.prettify(self.asn.thru))
            self.view.set_effort(self.asn.effort)
            self.view.set_notes(self.asn.notes)
            self.view.frum_ctrl.SetFocus()

    def save(self):
        formValues = self.getFormValues()
        # validate


    def cancel(self):
        self.view.Parent.Close()

    def getFormValues(self):
        return {
            'frum': self.view.get_frum(),
            'thru': self.view.get_thru(),
            'effort': self.view.get_effort(),
            'notes': self.view.get_notes()
        }