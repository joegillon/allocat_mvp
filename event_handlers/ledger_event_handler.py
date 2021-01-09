import wx
import wx.grid


class LedgerEventHandler(object):

    def install(self, presenter, view):
        self.presenter = presenter

        view.filter_ctrl.Bind(wx.EVT_COMBOBOX, self.on_filter_select)
        view.import_btn.Bind(wx.EVT_BUTTON, self.on_import_click)
        view.update_btn.Bind(wx.EVT_BUTTON, self.on_update_click)
        # view.reload_btn.Bind(wx.EVT_BUTTON, self.on_reload_click)
        # view.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_list_select)
        # view.update_btn.Bind(wx.EVT_BUTTON, self.on_update_click)
        # view.grant_admin_ctrl.Bind(wx.EVT_COMBOBOX, self.on_ga_select)
        # view.paid_ctrl.Bind(wx.EVT_CHECKBOX, self.on_paid_check)

    def on_filter_select(self, evt):
        self.presenter.set_total(evt.EventObject.GetValue())

    def on_import_click(self, evt):
        self.presenter.import_spreadsheet()

    def on_update_click(self, evt):
        self.presenter.update_ledger()

    # def on_reload_click(self, evt):
    #     self.presenter.reload()
    #
    # def on_import_click(self, evt):
    #     self.presenter.run_import()
    #
    # def on_list_select(self, evt):
    #     self.presenter.load_details()
    #
    # def on_update_click(self, evt):
    #     self.presenter.update_entry()
    #
    # def on_ga_select(self, evt):
    #     self.presenter.set_grant_admin_email(evt.EventObject.GetValue())
    #
    # def on_paid_check(self, evt):
    #     self.presenter.set_balance(evt.EventObject.GetValue())
