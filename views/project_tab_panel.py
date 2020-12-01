import wx
import ObjectListView as olv
from views.tab_panel import TabPanel
import lib.month_lib as ml
import lib.ui_lib as uil


class ProjectTabPanel(TabPanel):

    def __init__(self, parent):
        super().__init__(parent, 'Project')

    def set_columns(self, list_ctrl):
        list_ctrl.SetColumns([
            olv.ColumnDefn('Name', 'left', 200, 'name'),
            olv.ColumnDefn('From', 'left', 105, 'frum',
                           stringConverter=ml.prettify),
            olv.ColumnDefn('Thru', 'left', 100, 'thru',
                           stringConverter=ml.prettify),
            olv.ColumnDefn('PI', 'left', 150, 'investigator'),
            olv.ColumnDefn('PM', 'left', 150, 'manager'),
            olv.ColumnDefn('Full Name', 'left', 0, 'full_name'),
            olv.ColumnDefn('Notes', 'left', 0, 'notes')
        ])

    def add_model_layout(self, panel, layout):
        name_layout = wx.BoxSizer(wx.HORIZONTAL)
        name_lbl = wx.StaticText(panel, wx.ID_ANY, self.model_name + ' Name: *')
        self.name_ctrl = wx.TextCtrl(panel, wx.ID_ANY, size=(400, -1))
        name_layout.Add(name_lbl, 0, wx.ALL, 5)
        name_layout.Add(self.name_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(name_layout, 0, wx.ALL, 5)

        full_name_layout = wx.BoxSizer(wx.HORIZONTAL)
        full_name_lbl = wx.StaticText(panel, wx.ID_ANY, 'Full Name: *')
        self.full_name_ctrl = wx.TextCtrl(panel, wx.ID_ANY, size=(500, -1))
        full_name_layout.Add(full_name_lbl, 0, wx.ALL, 5)
        full_name_layout.Add(self.full_name_ctrl, 0, wx.ALL, 5)
        layout.Add(full_name_layout, 0, wx.ALL | wx.EXPAND, 5)

        interval_layout = wx.BoxSizer(wx.HORIZONTAL)
        frum_lbl = wx.StaticText(panel, wx.ID_ANY, 'From: *')
        self.frum_ctrl = uil.get_month_ctrl(panel, '')
        interval_layout.Add(frum_lbl, 0, wx.ALL, 5)
        interval_layout.Add(self.frum_ctrl, 0, wx.ALL, 5)

        thru_lbl = wx.StaticText(panel, wx.ID_ANY, 'Thru: *')
        self.thru_ctrl = uil.get_month_ctrl(panel, '')
        interval_layout.Add(thru_lbl, 0, wx.ALL, 5)
        interval_layout.Add(self.thru_ctrl, 0, wx.ALL, 5)

        layout.Add(interval_layout, 0, wx.ALL, 5)

        persons_layout = wx.BoxSizer(wx.HORIZONTAL)

        pi_lbl = wx.StaticText(panel, wx.ID_ANY, 'PI:')
        self.pi_ctrl = uil.ObjComboBox(panel,
                                       [],
                                     'name',
                                     'Employee',
                                       style=wx.CB_READONLY)
        persons_layout.Add(pi_lbl, 0, wx.ALL, 5)
        persons_layout.Add(self.pi_ctrl, 0, wx.ALL, 5)

        pm_lbl = wx.StaticText(panel, wx.ID_ANY, 'PM:')
        self.pm_ctrl = uil.ObjComboBox(panel,
                                       [],
                                     'name',
                                     'Employee',
                                       style=wx.CB_READONLY)
        persons_layout.Add(pm_lbl, 0, wx.ALL, 5)
        persons_layout.Add(self.pm_ctrl, 0, wx.ALL, 5)

        layout.Add(persons_layout, 0, wx.ALL, 5)

    def get_owner_column(self):
        return olv.ColumnDefn('Employee', 'left', 200, 'employee')

    def set_full_name(self, value):
        if not value:
            value = ''
        self.full_name_ctrl.SetValue(value)

    def get_full_name(self):
        value = self.full_name_ctrl.GetValue()
        return value if value else None

    def set_frum(self, value):
        self.frum_ctrl.SetValue(ml.prettify(value))

    def get_frum(self):
        value = self.frum_ctrl.GetValue()
        if value == '00/00':
            return None
        return ml.uglify(value)

    def set_thru(self, value):
        self.thru_ctrl.SetValue(ml.prettify(value))

    def get_thru(self):
        value = self.thru_ctrl.GetValue()
        if value == '00/00':
            return None
        return ml.uglify(value)

    def load_pi(self, investigators):
        self.pi_ctrl.set_choices(investigators, 'name')

    def set_pi(self, value):
        self.pi_ctrl.set_selection(value)

    def get_pi(self):
        return self.pi_ctrl.get_selection()

    def load_pm(self, managers):
        self.pm_ctrl.set_choices(managers, 'name')

    def set_pm(self, value):
        self.pm_ctrl.set_selection(value)

    def get_pm(self):
        return self.pm_ctrl.get_selection()
