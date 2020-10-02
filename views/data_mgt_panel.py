import wx
import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil


class DataMgtPanel(wx.Panel):

    def __init__(self, parent, presenter):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.pnlBg))
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.presenter = presenter

        dept_panel = self.build_dept_panel(self)
        admin_panel = self.build_admin_panel(self)

        layout.Add(dept_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(admin_panel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)

    def build_dept_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, size=(680, 500)
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_dept_toolbar_panel(panel)
        list_panel = self.build_dept_list_panel(panel)

        layout.Add(tb_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(list_panel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)
        return panel

    def build_dept_toolbar_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.get_toolbar_label(panel, 'Departments')
        lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(lbl, 0, wx.ALL, 5)

        self.dept_add_btn = uil.toolbar_button(panel, 'Add')
        layout.Add(self.dept_add_btn, 0, wx.ALL, 5)

        self.dept_drop_btn = uil.toolbar_button(panel, 'Drop')
        layout.Add(self.dept_drop_btn, 0, wx.ALL, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def build_dept_list_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        self.dept_list_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                                 size=wx.Size(200, 600),
                                                 style=wx.LC_REPORT | wx.SUNKEN_BORDER,
                                                 cellEditMode=olv.ObjectListView.CELLEDIT_DOUBLECLICK)

        self.dept_list_ctrl.SetColumns([
            olv.ColumnDefn('Department', 'left', wx.LIST_AUTOSIZE, 'name',
                           valueSetter=self.presenter.update_dept)
        ])

        self.dept_list_ctrl.AutoSizeColumns()

        layout.Add(self.dept_list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizerAndFit(layout)
        self.Layout()

        return panel

    def set_dept_list(self, data):
        self.dept_list_ctrl.SetObjects(data)

    def get_dept_selection(self):
        return self.dept_list_ctrl.GetSelectedObject()

    def add_dept(self, dept):
        self.dept_list_ctrl.AddObject(dept)
        self.dept_list_ctrl.SortBy(0)

    def drop_dept(self, dept):
        self.dept_list_ctrl.RemoveObject(dept)

    def build_admin_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, size=(680, 500)
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_admin_toolbar_panel(panel)
        list_panel = self.build_admin_list_panel(panel)

        layout.Add(tb_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(list_panel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)
        return panel

    def build_admin_toolbar_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.get_toolbar_label(panel, 'Grant Administrators')
        lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(lbl, 0, wx.ALL, 5)

        self.admin_add_btn = uil.toolbar_button(panel, 'Add')
        layout.Add(self.admin_add_btn, 0, wx.ALL, 5)

        self.admin_drop_btn = uil.toolbar_button(panel, 'Drop')
        layout.Add(self.admin_drop_btn, 0, wx.ALL, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def build_admin_list_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        self.admin_list_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                                 size=wx.Size(500, 600),
                                                 style=wx.LC_REPORT | wx.SUNKEN_BORDER,
                                                  cellEditMode=olv.ObjectListView.CELLEDIT_DOUBLECLICK)

        self.admin_list_ctrl.SetColumns([
            olv.ColumnDefn('Admin', 'left', wx.LIST_AUTOSIZE, 'name',
                           valueSetter=self.presenter.update_admin),
            olv.ColumnDefn('Email', 'left', wx.LIST_AUTOSIZE, 'email',
                           valueSetter=self.presenter.update_admin_email)
        ])

        self.admin_list_ctrl.AutoSizeColumns()

        layout.Add(self.admin_list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizerAndFit(layout)
        self.Layout()

        return panel

    def set_admin_list(self, data):
        self.admin_list_ctrl.SetObjects(data)

    def get_admin_selection(self):
        return self.admin_list_ctrl.GetSelectedObject()

    def add_admin(self, admin):
        self.admin_list_ctrl.AddObject(admin)
        self.admin_list_ctrl.SortBy(0)

    def drop_admin(self, admin):
        self.admin_list_ctrl.RemoveObject(admin)
