import wx
import wx.adv
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
        layout.Add(name_layout, 0, wx.ALL, 0)

        full_name_layout = wx.BoxSizer(wx.HORIZONTAL)
        full_name_lbl = wx.StaticText(panel, wx.ID_ANY, 'Full Name: *')
        self.full_name_ctrl = wx.TextCtrl(panel, wx.ID_ANY, size=(500, -1))
        full_name_layout.Add(full_name_lbl, 0, wx.ALL, 5)
        full_name_layout.Add(self.full_name_ctrl, 0, wx.ALL, 5)
        layout.Add(full_name_layout, 0, wx.ALL | wx.EXPAND, 0)

        interval_layout = wx.BoxSizer(wx.HORIZONTAL)
        frum_lbl = wx.StaticText(panel, wx.ID_ANY, 'From: *')
        self.frum_ctrl = uil.get_month_ctrl(panel, '')
        interval_layout.Add(frum_lbl, 0, wx.ALL, 1)
        interval_layout.Add(self.frum_ctrl, 0, wx.ALL, 1)

        thru_lbl = wx.StaticText(panel, wx.ID_ANY, 'Thru: *')
        self.thru_ctrl = uil.get_month_ctrl(panel, '')
        interval_layout.Add(thru_lbl, 0, wx.ALL, 1)
        interval_layout.Add(self.thru_ctrl, 0, wx.ALL, 1)

        dept_layout = wx.BoxSizer(wx.HORIZONTAL)
        dept_lbl = wx.StaticText(panel, wx.ID_ANY, 'Dept:')
        self.dept_ctrl = wx.ComboBox(panel, wx.ID_ANY, '')
        dept_layout.Add(dept_lbl, 0, wx.ALL, 1)
        dept_layout.Add(self.dept_ctrl, 0, wx.ALL, 1)
        interval_layout.Add(dept_layout, 0, wx.ALL, 1)

        short_code_layout = wx.BoxSizer(wx.HORIZONTAL)
        short_code_lbl = wx.StaticText(panel, wx.ID_ANY, ' Short Code:')
        self.short_code_ctrl = wx.TextCtrl(panel, wx.ID_ANY, size=(55, -1))
        short_code_layout.Add(short_code_lbl, 0, wx.ALL, 1)
        short_code_layout.Add(self.short_code_ctrl, 0, wx.ALL | wx.EXPAND, 1)
        interval_layout.Add(short_code_layout, 0, wx.ALIGN_RIGHT, 5)

        layout.Add(interval_layout, 0, wx.ALL, 0)

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

        layout.Add(persons_layout, 0, wx.ALL, 0)

        grant_layout = wx.BoxSizer(wx.HORIZONTAL)

        grant_admin_lbl = wx.StaticText(panel, wx.ID_ANY, 'Grant Admin:')
        self.grant_admin_ctrl = wx.ComboBox(panel, wx.ID_ANY, '')
        grant_layout.Add(grant_admin_lbl, 0, wx.ALL, 5)
        grant_layout.Add(self.grant_admin_ctrl, 0, wx.ALL, 5)

        grant_admin_email_lbl = wx.StaticText(panel, wx.ID_ANY, 'Email:')
        self.grant_admin_email_ctrl = wx.TextCtrl(panel, wx.ID_ANY, size=(200, -1))
        grant_layout.Add(grant_admin_email_lbl, 0, wx.ALL, 5)
        grant_layout.Add(self.grant_admin_email_ctrl, 0, wx.ALL, 5)

        layout.Add(grant_layout, 0, wx.ALL, 0)

        billing_layout1 = wx.BoxSizer(wx.HORIZONTAL)
        q1_lbl = wx.StaticText(panel, wx.ID_ANY, 'Billing Dates Q1:')
        self.q1_ctrl = wx.adv.DatePickerCtrl(panel, wx.ID_ANY,
                             style=wx.adv.DP_DROPDOWN|wx.adv.DP_ALLOWNONE)
        billing_layout1.Add(q1_lbl, 0, wx.ALL, 5)
        billing_layout1.Add(self.q1_ctrl, 0, wx.ALL, 5)
        q2_lbl = wx.StaticText(panel, wx.ID_ANY, 'Q2:')
        self.q2_ctrl = wx.adv.DatePickerCtrl(panel, wx.ID_ANY,
                             style=wx.adv.DP_DROPDOWN|wx.adv.DP_ALLOWNONE)
        billing_layout1.Add(q2_lbl, 0, wx.ALL, 5)
        billing_layout1.Add(self.q2_ctrl, 0, wx.ALL, 5)
        layout.Add(billing_layout1, 0, wx.ALL, 5)

        billing_layout2 = wx.BoxSizer(wx.HORIZONTAL)
        q3_lbl = wx.StaticText(panel, wx.ID_ANY, 'Billing Dates Q3:')
        self.q3_ctrl = wx.adv.DatePickerCtrl(panel, wx.ID_ANY,
                             style=wx.adv.DP_DROPDOWN|wx.adv.DP_ALLOWNONE)
        billing_layout2.Add(q3_lbl, 0, wx.ALL, 5)
        billing_layout2.Add(self.q3_ctrl, 0, wx.ALL, 5)
        q4_lbl = wx.StaticText(panel, wx.ID_ANY, 'Q4:')
        self.q4_ctrl = wx.adv.DatePickerCtrl(panel, wx.ID_ANY,
                             style=wx.adv.DP_DROPDOWN|wx.adv.DP_ALLOWNONE)
        billing_layout2.Add(q4_lbl, 0, wx.ALL, 5)
        billing_layout2.Add(self.q4_ctrl, 0, wx.ALL, 5)
        layout.Add(billing_layout2, 0, wx.ALL, 0)

    def get_owner_column(self):
        return olv.ColumnDefn('Employee', 'left', 200, 'employee')

    def set_full_name(self, value):
        self.full_name_ctrl.SetValue(value)

    def get_full_name(self):
        return self.full_name_ctrl.GetValue()

    def set_frum(self, value):
        self.frum_ctrl.SetValue(ml.prettify(value))

    def get_frum(self):
        value = ml.uglify(self.frum_ctrl.GetValue())
        if value == '0000':
            value = ''
        return value

    def set_thru(self, value):
        self.thru_ctrl.SetValue(ml.prettify(value))

    def get_thru(self):
        value = ml.uglify(self.thru_ctrl.GetValue())
        if value == '0000':
            value = ''
        return value

    def load_depts(self, depts):
        choices = [dept.name for dept in depts]
        choices.insert(0, '')
        self.dept_ctrl.Items = choices

    def set_dept(self, value):
        self.dept_ctrl.SetValue(value)

    def get_dept(self):
        return self.dept_ctrl.GetValue()

    def set_short_code(self, value):
        if not value:
            value = ''
        self.short_code_ctrl.SetValue(value)

    def get_short_code(self):
        return self.short_code_ctrl.GetValue()

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

    def load_grant_admins(self, admins):
        choices = [admin.name for admin in admins]
        choices.insert(0, '')
        self.grant_admin_ctrl.Items = choices

    def set_grant_admin(self, value):
        self.grant_admin_ctrl.SetValue(value)

    def get_grant_admin(self):
        return self.grant_admin_ctrl.GetValue()

    def set_grant_admin_email(self, value):
        if not value:
            value = ''
        self.grant_admin_email_ctrl.SetValue(value)

    def get_grant_admin_email(self):
        return self.grant_admin_email_ctrl.GetValue()
