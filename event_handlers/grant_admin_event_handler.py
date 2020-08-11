import wx


class GrantAdminInteractor(object):

    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view

        view.grant_admin_ctrl.Bind(wx.EVT_COMBOBOX, self.on_select)

    def on_select(self, evt):
        self.presenter.set_grant_admin_email(evt.EventObject.StringSelection)
