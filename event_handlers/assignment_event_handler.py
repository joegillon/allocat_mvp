import wx


class AssignmentInteractor(object):

    def Install(self, presenter, view):
        self.presenter = presenter
        self.view = view

        view.save_btn.Bind(wx.EVT_BUTTON, self.on_save)
        view.cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)

    def on_save(self, evt):
        self.presenter.save()

    def on_cancel(self, evt):
        self.presenter.cancel()
