import wx
from views.assignment_panel import AssignmentPanel
from interactors.assignment_interactor import AssignmentInteractor
from presenters.assignment_presenter import AssignmentPresenter


class AsnDlg(wx.Dialog):
    def __init__(self, parent, winId, title, owner, assignee, asn=None):
        wx.Dialog.__init__(self, parent, winId, title, size=(500, 400))
        layout = wx.BoxSizer(wx.VERTICAL)

        view = AssignmentPanel(self, owner, assignee)
        actor = AssignmentInteractor()
        presenter = AssignmentPresenter(asn, view, actor)
        presenter.go()

        layout.Add(view, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(layout)
