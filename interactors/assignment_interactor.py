import wx


class AssignmentInteractor(object):

    def Install(self, presenter, view):
        self.presenter = presenter
        self.view = view

        view.saveBtn.Bind(wx.EVT_BUTTON, self.OnSave)
        view.cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancel)

    def OnSave(self, evt):
        self.presenter.save()

    def OnCancel(self, evt):
        self.presenter.cancel()
