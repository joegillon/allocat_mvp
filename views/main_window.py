import wx
import globals as gbl
from views.project.project_view import ProjectPanel
from interactors.project_interactor import ProjectInteractor
from presenters.project_presenter import ProjectPresenter
from dal.dao import Dao
from models.project import Project
from models.employee import Employee
# from views.employees.tab_panel import EmpTabPanel
# from views.efforts.eff_tab import EffTab


class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='allocat', size=(1200, 800))
        panel = wx.Panel(self)
        layout = wx.BoxSizer()

        panel.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        notebook = wx.Notebook(panel)

        dao = Dao(stateful=True)
        prj_model = Project.get_all(dao)
        emp_model = Employee.get_all(dao)
        dao.close()

        prj_view = ProjectPanel(notebook)
        prj_actor = ProjectInteractor()
        presenter = ProjectPresenter(prj_model, prj_view, prj_actor, emp_model)

        notebook.AddPage(prj_view, 'Projects')
        # notebook.AddPage(EmpTabPanel(notebook), 'Employees')
        # notebook.AddPage(EffTab(notebook), 'Scoreboard')
        layout.Add(notebook, 0, wx.EXPAND, 5)

        panel.SetSizer(layout)
