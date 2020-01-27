import wx
from presenters.assignment_presenter import AssignmentPresenter


class AsnDlg(wx.Dialog):

    def __init__(self, parent, winId, title, owner, assignee, asn=None):
        wx.Dialog.__init__(self, parent, winId, title, size=(500, 400))
        layout = wx.BoxSizer(wx.VERTICAL)

        self.presenter = AssignmentPresenter(self, owner, assignee, asn)

        layout.Add(self.presenter.view, 0, wx.ALL | wx.EXPAND, 5)

        self.Name = 'AsnDlg'
        self.SetSizer(layout)

        self.presenter.go()
