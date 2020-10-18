import wx
import wx.grid
import ObjectListView as olv


class DataMgtInteractor(object):

    def install(self, presenter, view):
        self.presenter = presenter

        view.emp_list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_emp_list_dbl_click)
        # view.pm_list_ctrl.Bind(olv.EVT_CELL_EDIT_FINISHING, self.on_pm_edit_end)
        view.pm_drop_btn.Bind(wx.EVT_BUTTON, self.on_pm_drop_click)
        view.dept_add_btn.Bind(wx.EVT_BUTTON, self.on_dept_add_click)
        view.dept_drop_btn.Bind(wx.EVT_BUTTON, self.on_dept_drop_click)
        view.admin_add_btn.Bind(wx.EVT_BUTTON, self.on_admin_add_click)
        view.admin_drop_btn.Bind(wx.EVT_BUTTON, self.on_admin_drop_click)

    def on_emp_list_dbl_click(self, evt):
        self.presenter.add_pm()

    def on_pm_edit_end(self, evt):
        pass

    def on_pm_drop_click(self, evt):
        self.presenter.drop_pm()

    def on_dept_add_click(self, evt):
        self.presenter.add_dept()

    def on_dept_drop_click(self, evt):
        self.presenter.drop_dept()

    def on_admin_add_click(self, evt):
        self.presenter.add_admin()

    def on_admin_drop_click(self, evt):
        self.presenter.drop_admin()
