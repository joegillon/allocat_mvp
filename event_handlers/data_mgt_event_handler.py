import wx
import wx.grid


class DataMgtInteractor(object):

    def install(self, presenter, view):
        self.presenter = presenter

        view.dept_add_btn.Bind(wx.EVT_BUTTON, self.on_dept_add_click)
        view.dept_drop_btn.Bind(wx.EVT_BUTTON, self.on_dept_drop_click)
        view.admin_add_btn.Bind(wx.EVT_BUTTON, self.on_admin_add_click)
        view.admin_drop_btn.Bind(wx.EVT_BUTTON, self.on_admin_drop_click)

    def on_dept_add_click(self, evt):
        self.presenter.add_dept()

    def on_dept_drop_click(self, evt):
        self.presenter.drop_dept()

    def on_admin_add_click(self, evt):
        self.presenter.add_admin()

    def on_admin_drop_click(self, evt):
        self.presenter.drop_admin()
