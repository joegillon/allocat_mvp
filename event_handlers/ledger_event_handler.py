import wx
import wx.grid


class LedgerEventHandler(object):

    def install(self, presenter, view):
        self.presenter = presenter

        view.qry_btn.Bind(wx.EVT_BUTTON, self.on_qry_click)
        view.reload_btn.Bind(wx.EVT_BUTTON, self.on_reload_click)
        view.work_list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_work_list_select)
        view.save_form_btn.Bind(wx.EVT_BUTTON, self.on_save_form_click)
        view.done_btn.Bind(wx.EVT_BUTTON, self.on_mark_done_click)
        view.grant_admin_ctrl.Bind(wx.EVT_COMBOBOX, self.on_ga_select)
        view.amount_ctrl.Bind(wx.EVT_KILL_FOCUS, self.on_amt_changed)
        view.filter_ctrl.Bind(wx.EVT_COMBOBOX, self.on_filter_select)
        view.undo_btn.Bind(wx.EVT_BUTTON, self.on_undo_click)
        view.import_btn.Bind(wx.EVT_BUTTON, self.on_import_click)

    def on_qry_click(self, evt):
        self.presenter.run_query()

    def on_reload_click(self, evt):
        self.presenter.reload()

    def on_work_list_select(self, evt):
        self.presenter.load_form()

    def on_save_form_click(self, evt):
        self.presenter.save_form()

    def on_mark_done_click(self, evt):
        self.presenter.mark_done()

    def on_ga_select(self, evt):
        self.presenter.set_grant_admin_email(evt.EventObject.GetValue())

    def on_amt_changed(self, evt):
        self.presenter.update_amount_balance(evt.EventObject.GetValue())

    def on_filter_select(self, evt):
        self.presenter.set_total(evt.EventObject.GetValue())

    def on_undo_click(self, evt):
        self.presenter.undo()

    def on_import_click(self, evt):
        self.presenter.import_deposits()

