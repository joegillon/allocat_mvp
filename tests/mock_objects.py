class MockProjectFrame(object):

    def __init__(self):

        # Mock controls
        self.listCtrl = []
        self.nameFltrCtrl = ''
        self.notesFltrCtrl = ''
        self.nameCtrl = ''
        self.fullNameCtrl = ''
        self.frumCtrl = ''
        self.thruCtrl = ''
        self.piCtrl = ([], '')
        self.pmCtrl = ([], '')
        self.notesCtrl = ''
        self.asnListCtrl = []

        # Properties
        self.selectedIdx = 0
        # self.selection = None
        # self.selected = -1
        # self.idx = 0

    def setList(self, model):
        self.listCtrl = model

    def setName(self, value):
        self.nameCtrl = value

    def getName(self):
        return self.nameCtrl

    def setFullName(self, value):
        self.fullNameCtrl = value

    def getFullName(self):
        return self.fullNameCtrl

    def setFrum(self, value):
        self.frumCtrl = value

    def getFrum(self):
        return self.frumCtrl

    def setThru(self, value):
        self.thruCtrl = value

    def getThru(self):
        return self.thruCtrl

    def loadPI(self, value):
        self.piCtrl = (value, self.piCtrl[1])

    def setPI(self, value):
        self.piCtrl = (self.piCtrl[0], value)

    def getPI(self):
        return self.piCtrl[1]

    def loadPM(self, value):
        self.pmCtrl = (value, self.pmCtrl[1])

    def setPM(self, value):
        self.pmCtrl = (self.pmCtrl[0], value)

    def getPM(self):
        return self.pmCtrl[1]

    def setNotes(self, value):
        self.notesCtrl = value

    def getNotes(self):
        return self.notesCtrl

    def setSelectedIdx(self, value):
        self.selectedIdx = value

    def getSelectedIdx(self):
        return self.selectedIdx

    def setSelection(self, value):
        self.selection = self.listCtrl[value]

    def getSelection(self):
        return self.listCtrl[self.idx]

    def getAsnSelections(self):
        return self.asnListCtrl

    def setAsnList(self, value):
        self.asnListCtrl = value


class MockProjectInteractor:
    def Install(self, presenter, view):
        pass
