import wx
import globals as gbl
import lib.ui_lib as uil
import lib.month_lib as ml


class AssignmentPanel(wx.Panel):

    def __init__(self, dlg):
        wx.Panel.__init__(self, dlg)
        self.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_toolbar_panel(self)
        frm_panel = self.build_form_panel(self)

        layout.Add(tb_panel, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(frm_panel, 0, wx.ALL | wx.EXPAND, 5)

        self.Name = 'AssignmentPanel'
        self.SetSizer(layout)

    def build_toolbar_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.save_btn = uil.toolbar_button(panel, 'Save Assignment')
        self.cancel_btn = uil.toolbar_button(panel, 'Cancel')

        layout.Add(self.save_btn, 0, wx.ALL, 5)
        layout.Add(self.cancel_btn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def build_form_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, size=(-1, 375)
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.frmBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        owner_layout = wx.BoxSizer(wx.HORIZONTAL)
        self.owner_lbl = wx.StaticText(panel, wx.ID_ANY, '')
        owner_layout.Add(self.owner_lbl, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(owner_layout, 0, wx.ALL | wx.EXPAND, 5)

        self.assignee_layout = wx.BoxSizer(wx.HORIZONTAL)
        self.assignee_lbl = wx.StaticText(panel, wx.ID_ANY, '')
        self.assignee_layout.Add(self.assignee_lbl, 0, wx.ALL, 5)
        layout.Add(self.assignee_layout, 0, wx.ALL | wx.EXPAND, 5)

        interval_layout = wx.BoxSizer(wx.HORIZONTAL)

        frum_lbl = wx.StaticText(panel, wx.ID_ANY, 'From: *')
        interval_layout.Add(frum_lbl, 0, wx.ALL, 5)
        self.frum_ctrl = uil.get_month_ctrl(panel, '')
        interval_layout.Add(self.frum_ctrl, 0, wx.ALL, 5)

        thru_lbl = wx.StaticText(panel, wx.ID_ANY, 'Thru: *')
        interval_layout.Add(thru_lbl, 0, wx.ALL, 5)
        self.thru_ctrl = uil.get_month_ctrl(panel, '')
        interval_layout.Add(self.thru_ctrl, 0, wx.ALL, 5)

        layout.Add(interval_layout)

        eff_layout = wx.BoxSizer(wx.HORIZONTAL)
        effort_lbl = wx.StaticText(panel, wx.ID_ANY, '% Effort: *')
        eff_layout.Add(effort_lbl, 0, wx.ALL, 5)
        self.effort_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '', size=(50, -1))
        eff_layout.Add(self.effort_ctrl, 0, wx.ALL, 5)
        layout.Add(eff_layout)

        notes_layout = wx.BoxSizer(wx.VERTICAL)
        notes_lbl = wx.StaticText(panel, wx.ID_ANY, 'Notes:')
        notes_layout.Add(notes_lbl, 0, wx.ALL, 5)
        self.notes_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '',
                                      style=wx.TE_MULTILINE, size=(500, 200))
        notes_layout.Add(self.notes_ctrl, 0, wx.ALL, 5)
        layout.Add(notes_layout)

        panel.SetSizer(layout)

        self.form_panel = panel

        return panel

    def set_owner(self, value):
        self.owner_lbl.SetLabelText(value)

    def set_assignee(self, assignee):
        self.assignee = assignee
        if isinstance(assignee, str):
            self.assignee_lbl.SetLabelText(assignee)
        else:
            self.assignee.Reparent(self.form_panel)
            self.assignee_lbl.SetLabelText(assignee.LabelText)
            self.assignee_layout.Add(assignee, 0, wx.ALL | wx.EXPAND, 5)

    def get_assignee(self):
        return None if type(self.assignee) == str else self.assignee.get_selection()

    def set_frum(self, value):
        self.frum_ctrl.SetValue(value)

    def get_frum(self):
        value = ml.uglify(self.frum_ctrl.GetValue())
        if value == '0000':
            value = ''
        return value

    def set_thru(self, value):
        self.thru_ctrl.SetValue(value)

    def get_thru(self):
        value = ml.uglify(self.thru_ctrl.GetValue())
        if value == '0000':
            value = ''
        return value

    def set_effort(self, value):
        value = str(value) if value else ''
        self.effort_ctrl.SetValue(value)

    def get_effort(self):
        return self.effort_ctrl.GetValue()

    def set_notes(self, value):
        if not value:
            value = ''
        self.notes_ctrl.SetValue(value)

    def get_notes(self):
        return self.notes_ctrl.GetValue().strip()
