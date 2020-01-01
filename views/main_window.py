import wx
import globals as gbl
from dal.dao import Dao
from event_handlers.project_event_handler import ProjectEventHandler
from models.employee import Employee
from models.project import Project
from models.assignment import Assignment
from presenters.project_presenter import ProjectPresenter
from views.project_panel import ProjectPanel
import lib.ui_lib as uil


# from views.employees.tab_panel import EmpTabPanel
# from views.efforts.eff_tab import EffTab


class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='allocat', size=(1200, 800))
        panel = wx.Panel(self)
        layout = wx.BoxSizer()

        panel.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        notebook = wx.Notebook(panel)
        layout.Add(notebook, 0, wx.EXPAND, 5)

        prj_view = ProjectPanel(notebook)
        prj_actor = ProjectEventHandler()
        prj_presenter = ProjectPresenter(prj_view, prj_actor)

        notebook.AddPage(prj_view, 'Projects')
        # notebook.AddPage(EmpTabPanel(notebook), 'Employees')
        # notebook.AddPage(EffTab(notebook), 'Scoreboard')

        panel.SetSizer(layout)

        prj_presenter.initView()
