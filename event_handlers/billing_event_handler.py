import wx
import wx.grid


class BillingInteractor(object):

    def install(self, presenter, view, dlg):
        self.presenter = presenter

        view.run_btn.Bind(wx.EVT_BUTTON, self.on_run_click)
        view.grid_ctrl.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.on_left_click)
        dlg.cancel_btn.Bind(wx.EVT_BUTTON, self.on_form_cancel)
        dlg.save_btn.Bind(wx.EVT_BUTTON, self.on_form_save)

    def on_run_click(self, evt):
        self.presenter.run_query()

    def on_left_click(self, evt):
        self.presenter.launch_form(evt.Row, evt.Col)

    def on_form_cancel(self, evt):
        self.presenter.close_form()

    def on_form_save(self, evt):
        self.presenter.save_form_data()
