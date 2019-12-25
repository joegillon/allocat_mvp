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
        pass

    def cancel(self):
        self.view.Parent.Close()
