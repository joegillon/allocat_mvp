import wx
import ObjectListView as olv
from views.tab_panel import TabPanel
import lib.ui_lib as uil


class EmployeeTabPanel(TabPanel):

    def __init__(self, parent):
        super().__init__(parent, 'Employee')

    def set_columns(self, list_ctrl):
        list_ctrl.SetColumns([
            olv.ColumnDefn('Name', 'left', 200, 'name'),
            olv.ColumnDefn('FTE', 'right', wx.LIST_AUTOSIZE_USEHEADER, 'fte'),
            olv.ColumnDefn('Investigator', 'right', wx.LIST_AUTOSIZE_USEHEADER, 'investigator',
                           stringConverter=uil.toYN),
            olv.ColumnDefn('Intern', 'right', wx.LIST_AUTOSIZE_USEHEADER, 'intern',
                           stringConverter=uil.toYN),
            olv.ColumnDefn('Org', 'left', 100, 'org'),
            olv.ColumnDefn('Notes', 'left', 0, 'notes'),
        ])

    def add_model_layout(self, panel, layout):
        import wx.lib.masked as masked

        form_layout = wx.BoxSizer(wx.HORIZONTAL)
        fte_lbl = wx.StaticText(panel, wx.ID_ANY, 'FTE: ')
        self.fte_ctrl = masked.TextCtrl(panel, wx.ID_ANY,
                                       mask='###',
                                       size=(50, -1))
        form_layout.Add(fte_lbl, 0, wx.ALL, 5)
        form_layout.Add(self.fte_ctrl, 0, wx.ALL, 5)

        investigator_lbl = wx.StaticText(panel, wx.ID_ANY, 'Investigator:')
        self.investigator_ctrl = wx.CheckBox(panel, wx.ID_ANY)
        form_layout.Add(investigator_lbl, 0, wx.ALL, 5)
        form_layout.Add(self.investigator_ctrl, 0, wx.ALL, 5)

        intern_lbl = wx.StaticText(panel, wx.ID_ANY, 'Intern:')
        self.intern_ctrl = wx.CheckBox(panel, wx.ID_ANY)
        form_layout.Add(intern_lbl, 0, wx.ALL, 5)
        form_layout.Add(self.intern_ctrl, 0, wx.ALL, 5)

        org_lbl = wx.StaticText(panel, wx.ID_ANY, 'Org:')
        self.org_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '')
        form_layout.Add(org_lbl, 0, wx.ALL, 5)
        form_layout.Add(self.org_ctrl, 0, wx.ALL, 5)

        layout.Add(form_layout, 0, wx.ALL, 5)

    def get_owner_column(self):
        return olv.ColumnDefn('Project', 'left', 200, 'project')

    def set_fte(self, value):
        self.fte_ctrl.SetValue(str(value))

    def get_fte(self):
        val = self.fte_ctrl.GetValue().strip()
        if val:
            return int(self.fte_ctrl.GetValue())
        else:
            return None

    def set_investigator(self, value):
        self.investigator_ctrl.SetValue(value)

    def get_investigator(self):
        return self.investigator_ctrl.GetValue()

    def set_intern(self, value):
        self.intern_ctrl.SetValue(value)

    def get_intern(self):
        return self.intern_ctrl.GetValue()

    def set_org(self, value):
        self.org_ctrl.SetValue(value)

    def get_org(self):
        return self.org_ctrl.GetValue()
