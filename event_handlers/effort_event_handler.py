import wx
import wx.grid


class EffortEventHandler(object):

    def install(self, presenter, view):
        self.presenter = presenter

        view.run_btn.Bind(wx.EVT_BUTTON, self.on_run_click)
        view.grid_ctrl.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.on_left_click)
        view.help_btn.Bind(wx.EVT_BUTTON, self.on_help_click)

    def on_run_click(self, evt):
        self.presenter.run_query()

    def on_left_click(self, evt):
        if evt.Col == 1:
            self.presenter.show_emp_breakdown(evt.Row)
        elif evt.Col ==2:
            return
        else:
            self.presenter.show_month_breakdown(evt.Col, evt.Row)

    def on_help_click(self, evt):
        self.presenter.show_help()
