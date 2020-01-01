class MainWindowPresenter(object):

    def __init__(self, view):
        self.view = view
        self.buildDataSet()
        self.view.show()

