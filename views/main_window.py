import wx
import globals as gbl
from presenters.project_presenter import ProjectPresenter
from presenters.employee_presenter import EmployeePresenter
from presenters.effort_presenter import EffortPresenter


class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='allocat', size=(1300, 800))
        panel = wx.Panel(self)
        layout = wx.BoxSizer()

        panel.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        notebook = wx.Notebook(panel)
        layout.Add(notebook, 0, wx.EXPAND, 5)

        prj_presenter = ProjectPresenter(notebook)
        emp_presenter = EmployeePresenter(notebook)
        eff_presenter = EffortPresenter(notebook)

        notebook.AddPage(prj_presenter.view, 'Projects')
        notebook.AddPage(emp_presenter.view, 'Employees')
        notebook.AddPage(eff_presenter.view, 'Scoreboard')

        panel.SetSizer(layout)

        prj_presenter.init_view()
        emp_presenter.init_view()
