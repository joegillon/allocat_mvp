class MockProjectFrame(object):
    def __init__(self):
        self.name = ''
        self.nickname = ''
        self.frum = ''
        self.thru = ''
        self.windowTitle = ''
        self.projects = []
        self.selected = -1
        self.idx = 0

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setNickname(self, nickname):
        self.nickname = nickname

    def getNickname(self):
        return self.nickname

    def setFrum(self, frum):
        self.frum = frum

    def getFrum(self):
        return self.frum

    def setThru(self, thru):
        self.thru = thru

    def getThru(self):
        return self.thru

    def setWindowTitle(self, title):
        self.windowTitle = title

    def setList(self, projects):
        self.projects = projects

    def setSelectedIdx(self, idx):
        self.idx = idx

    def getSelectedIdx(self):
        return self.idx

    def start(self):
        pass


class MockProjectInteractor:
    def Install(self, presenter, view):
        pass
