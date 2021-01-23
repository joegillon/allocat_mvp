import wx
import wx.grid


class LedgerEventHandler(object):

    def install(self, presenter, view):
        self.presenter = presenter

        view.filter_ctrl.Bind(wx.EVT_COMBOBOX, self.on_filter_select)
        view.import_btn.Bind(wx.EVT_BUTTON, self.on_import_click)
        view.update_btn.Bind(wx.EVT_BUTTON, self.on_update_click)

    def on_filter_select(self, evt):
        self.presenter.set_total(evt.EventObject.GetValue())

    def on_import_click(self, evt):
        self.presenter.import_spreadsheet()

    def on_update_click(self, evt):
        self.presenter.update_ledger()
