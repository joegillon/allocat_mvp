class AssignmentPresenter(object):

    def __init__(self, model, view, actor):
        self.model = model
        self.view = view
        self.actor = actor

    def go(self):
        self.actor.Install(self, self.view)
        self.isListening = True
        self.initView()

    def initView(self):
        if self.model:
            self.view.setFrum(self.model.frum)
            self.view.setThru(self.model.thru)
            self.view.setEffort(self.model.effort)
            self.view.setNotes(self.model.notes)
            self.view.frumCtrl.SetFocus()

    def save(self):
        formValues = self.getFormValues()
        # validate


    def cancel(self):
        self.view.Parent.Close()

    def getFormValues(self):
        return {
            'frum': self.view.getFrum(),
            'thru': self.view.getThru(),
            'effort': self.view.getEffort(),
            'notes': self.view.getNotes()
        }