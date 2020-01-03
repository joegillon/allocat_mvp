import wx
import globals as gbl
from event_handlers.project_event_handler import ProjectEventHandler
from presenters.project_presenter import ProjectPresenter
from views.project_tab_panel import ProjectTabPanel


class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='allocat', size=(1200, 800))
        panel = wx.Panel(self)
        layout = wx.BoxSizer()

        panel.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        notebook = wx.Notebook(panel)
        layout.Add(notebook, 0, wx.EXPAND, 5)

        prj_presenter = ProjectPresenter(notebook)

        notebook.AddPage(prj_presenter.view, 'Projects')
        # notebook.AddPage(EmpTabPanel(notebook), 'Employees')
        # notebook.AddPage(EffTab(notebook), 'Scoreboard')

        panel.SetSizer(layout)

        prj_presenter.init_view()
