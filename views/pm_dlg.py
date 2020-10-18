import wx
import globals as gbl
import lib.ui_lib as uil


class PmDlg(wx.Dialog):

    def __init__(self, parent, emp):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, size=(500, 250))
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        self.emp = emp

        tb_panel = self.build_toolbar_panel(panel)
        frm_panel = self.build_form_panel(panel)

        layout.Add(tb_panel, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(frm_panel, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizerAndFit(layout)

    def build_toolbar_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        title_lbl = uil.get_toolbar_label(panel, self.emp.name)
        title_lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(title_lbl, 0, wx.ALL, 5)

        self.ok_btn = uil.toolbar_button(panel, 'OK')
        layout.Add(self.ok_btn, 0, wx.ALL, 5)
        self.ok_btn.Bind(wx.EVT_BUTTON, self.on_ok_click)

        self.cancel_btn = uil.toolbar_button(panel, 'Cancel')
        layout.Add(self.cancel_btn, 0, wx.ALL, 5)
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel_click)

        panel.SetSizer(layout)

        return panel

    def build_form_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        email_lbl = uil.get_toolbar_label(panel, 'VA Email:')
        self.email_ctrl = wx.TextCtrl(panel, wx.ID_ANY, self.emp.va_email)
        layout.Add(email_lbl, 0, wx.ALL, 5)
        layout.Add(self.email_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        nonva_email_lbl = uil.get_toolbar_label(panel, 'Non-VA Email:')
        self.nonva_email_ctrl = wx.TextCtrl(panel, wx.ID_ANY, self.emp.nonva_email)
        layout.Add(nonva_email_lbl, 0, wx.ALL, 5)
        layout.Add(self.nonva_email_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def on_ok_click(self, evt):
        import lib.validator_lib as vl

        va_email = self.email_ctrl.GetValue()
        err_msg = vl.validate_email(va_email)
        if not err_msg:
            uil.show_error(err_msg)
            return
        self.emp.va_email = va_email

        nonva_email = self.email_ctrl.GetValue()
        err_msg = vl.validate_email(nonva_email)
        if not err_msg:
            uil.show_error(err_msg)
            return
        self.emp.nonva_email = nonva_email

        self.emp.pm = True

        self.Hide()

    def on_cancel_click(self, evt):
        self.Hide()

    def get_data(self):
        self.nonva_email_ctrl.GetValue()
