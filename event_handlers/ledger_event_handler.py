import wx
import wx.grid


class LedgerInteractor(object):

    def install(self, presenter, view):
        self.presenter = presenter

        view.qry_btn.Bind(wx.EVT_BUTTON, self.on_qry_click)
        view.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_list_select)
        view.update_btn.Bind(wx.EVT_BUTTON, self.on_update_click)
        view.grant_admin_ctrl.Bind(wx.EVT_COMBOBOX, self.on_ga_select)
        view.paid_ctrl.Bind(wx.EVT_CHECKBOX, self.on_paid_check)

    def on_query_tool(self, evt):
        self.presenter.run_query()

    def on_qry_click(self, evt):
        self.presenter.run_query()

    def on_import_click(self, evt):
        self.presenter.run_import()

    def on_list_select(self, evt):
        self.presenter.load_details()

    def on_update_click(self, evt):
        self.presenter.update_entry()

    def on_ga_select(self, evt):
        self.presenter.set_grant_admin_email(evt.EventObject.GetValue())

    def on_paid_check(self, evt):
        self.presenter.set_balance(evt.EventObject.GetValue())