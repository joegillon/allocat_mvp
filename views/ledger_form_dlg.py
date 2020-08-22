import wx
import wx.adv
import globals as gbl
import lib.ui_lib as uil


class LedgerFormDlg(wx.Dialog):

    def __init__(self, parent, winId):
        wx.Dialog.__init__(self, parent, winId, size=(800, 275))
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_toolbar_panel(panel)
        frm_panel = self.build_form_panel(panel)

        layout.Add(tb_panel, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(frm_panel, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizerAndFit(layout)

    def build_toolbar_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.name_lbl = uil.get_toolbar_label(panel, 'Ledger Record')
        self.name_lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(self.name_lbl, 0, wx.ALL, 5)

        btn_layout = wx.BoxSizer(wx.HORIZONTAL)
        self.cancel_btn = uil.toolbar_button(panel, 'Cancel')
        btn_layout.Add(self.cancel_btn, 0, wx.ALL, 5)
        self.save_btn = uil.toolbar_button(panel, 'Save')
        btn_layout.Add(self.save_btn, 0, wx.ALL, 5)
        layout.Add(btn_layout, 0, wx.ALIGN_RIGHT, 5)

        panel.SetSizer(layout)

        return panel

    def build_form_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.frmBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        grant_layout = wx.BoxSizer(wx.HORIZONTAL)

        dept_lbl = wx.StaticText(panel, wx.ID_ANY, 'Dept:')
        self.dept_ctrl = wx.ComboBox(panel, wx.ID_ANY, '')
        grant_layout.Add(dept_lbl, 0, wx.ALL, 5)
        grant_layout.Add(self.dept_ctrl, 0, wx.ALL, 5)

        admin_approved_lbl = wx.StaticText(panel, wx.ID_ANY, 'Admin Approved:')
        self.admin_approved_ctrl = wx.CheckBox(panel, wx.ID_ANY)
        grant_layout.Add(admin_approved_lbl, 0, wx.ALL, 5)
        grant_layout.Add(self.admin_approved_ctrl, 0, wx.ALL, 5)

        va_approved_lbl = wx.StaticText(panel, wx.ID_ANY, 'VA Approved:')
        self.va_approved_ctrl = wx.CheckBox(panel, wx.ID_ANY)
        grant_layout.Add(va_approved_lbl, 0, wx.ALL, 5)
        grant_layout.Add(self.va_approved_ctrl, 0, wx.ALL, 5)

        invoice_lbl = wx.StaticText(panel, wx.ID_ANY, 'Invoice #:')
        self.invoice_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '')
        grant_layout.Add(invoice_lbl, 0, wx.ALL, 5)
        grant_layout.Add(self.invoice_ctrl, 0, wx.ALL, 5)

        layout.Add(grant_layout, 0, wx.ALL, 5)

        staff_layout = wx.BoxSizer(wx.HORIZONTAL)

        salary_lbl = wx.StaticText(panel, wx.ID_ANY, 'Base Salary:')
        self.salary_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '', size=(50, -1))
        staff_layout.Add(salary_lbl, 0, wx.ALL, 5)
        staff_layout.Add(self.salary_ctrl, 0, wx.ALL, 5)

        fringe_lbl = wx.StaticText(panel, wx.ID_ANY, 'Fringe:')
        self.fringe_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '', size=(50, -1))
        staff_layout.Add(fringe_lbl, 0, wx.ALL, 5)
        staff_layout.Add(self.fringe_ctrl, 0, wx.ALL, 5)

        total_lbl = wx.StaticText(panel, wx.ID_ANY, 'Total/Day:')
        self.total_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '', size=(50, -1))
        staff_layout.Add(total_lbl, 0, wx.ALL, 5)
        staff_layout.Add(self.total_ctrl, 0, wx.ALL, 5)

        layout.Add(staff_layout, 0, wx.ALL, 5)

        amt_layout = wx.BoxSizer(wx.HORIZONTAL)

        amt_lbl = wx.StaticText(panel, wx.ID_ANY, 'Amount:')
        self.amt_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '', size=(50, -1))
        amt_layout.Add(amt_lbl, 0, wx.ALL, 5)
        amt_layout.Add(self.amt_ctrl, 0, wx.ALL, 5)

        paid_lbl = wx.StaticText(panel, wx.ID_ANY, 'Paid:')
        self.paid_ctrl = wx.CheckBox(panel, wx.ID_ANY)
        amt_layout.Add(paid_lbl, 0, wx.ALL, 5)
        amt_layout.Add(self.paid_ctrl, 0, wx.ALL, 5)

        balance_lbl = wx.StaticText(panel, wx.ID_ANY, 'Balance:')
        self.balance_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '', size=(50, -1))
        amt_layout.Add(balance_lbl, 0, wx.ALL, 5)
        amt_layout.Add(self.balance_ctrl, 0, wx.ALL, 5)

        layout.Add(amt_layout, 0, wx.ALL, 5)

        admin_layout = wx.BoxSizer(wx.HORIZONTAL)

        short_code_lbl = wx.StaticText(panel, wx.ID_ANY, 'Short Code:')
        self.short_code_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '', size=(50, -1))
        admin_layout.Add(short_code_lbl, 0, wx.ALL, 5)
        admin_layout.Add(self.short_code_ctrl, 0, wx.ALL, 5)

        grant_admin_lbl = wx.StaticText(panel, wx.ID_ANY, 'Grant Admin:')
        self.grant_admin_ctrl = wx.ComboBox(panel, wx.ID_ANY, '')
        admin_layout.Add(grant_admin_lbl, 0, wx.ALL, 5)
        admin_layout.Add(self.grant_admin_ctrl, 0, wx.ALL, 5)

        grant_admin_email_lbl = wx.StaticText(panel, wx.ID_ANY, 'Email:')
        self.grant_admin_email_ctrl = wx.TextCtrl(panel, wx.ID_ANY, size=(200, -1))
        admin_layout.Add(grant_admin_email_lbl, 0, wx.ALL, 5)
        admin_layout.Add(self.grant_admin_email_ctrl, 0, wx.ALL, 5)

        layout.Add(admin_layout, 0, wx.ALL, 0)

        panel.SetSizerAndFit(layout)

        return panel

    def load_data(self, data):
        self.set_dept(data[0])
        self.set_admin_approved(data[1])
        self.set_va_approved(data[2])
        self.set_invoice_num(data[3])
        self.set_salary(data[7])
        self.set_fringe(data[8])
        self.set_total(data[9])
        self.set_amount(data[11])
        self.set_paid(data[14])
        self.set_balance(data[15])
        self.set_short_code(data[16])
        self.set_grant_admin(data[17])
        self.set_grant_admin_email(data[18])

    def load_depts(self, depts):
        choices = depts
        choices.insert(0, '')
        self.dept_ctrl.Items = choices

    def set_dept(self, value):
        if not value:
            value = ''
        self.dept_ctrl.SetValue(value)

    def get_dept(self):
        return self.dept_ctrl.GetValue()

    def set_admin_approved(self, value):
        value = True if value == 'Y' else False
        self.admin_approved_ctrl.SetValue(value)

    def get_admin_approved(self):
        return True if self.admin_approved_ctrl.GetValue() == 'Y' else False

    def set_va_approved(self, value):
        value = True if value == 'Y' else False
        self.va_approved_ctrl.SetValue(value)

    def get_va_approved(self):
        return True if self.va_approved_ctrl.GetValue() == 'Y' else False

    def set_invoice_num(self, value):
        if not value:
            value = ''
        self.invoice_ctrl.SetValue(value)

    def get_invoice_num(self):
        return self.invoice_ctrl.GetValue()

    def set_project(self, value):
        self.prj_
    def set_salary(self, value):
        if not value:
            value = ''
        self.salary_ctrl.SetValue(str(value))

    def get_salary(self):
        return self.salary_ctrl.GetValue()

    def set_fringe(self, value):
        if not value:
            value = ''
        self.fringe_ctrl.SetValue(str(value))

    def get_fringe(self):
        return self.fringe_ctrl.GetValue()

    def set_total(self, value):
        if not value:
            value = ''
        self.total_ctrl.SetValue(str(value))

    def get_total(self):
        return self.total_ctrl.GetValue()

    def set_amount(self, value):
        if not value:
            value = ''
        self.amt_ctrl.SetValue(str(value))

    def get_amount(self):
        return self.amt_ctrl.GetValue()

    def set_paid(self, value):
        value = True if value == 'Y' else False
        self.paid_ctrl.SetValue(value)

    def get_paid(self):
        return True if self.paid_ctrl.GetValue() == 'Y' else False

    def set_balance(self, value):
        if not value:
            value = ''
        self.balance_ctrl.SetValue(str(value))

    def get_balance(self):
        return self.balance_ctrl.GetValue()

    def set_short_code(self, value):
        if not value:
            value = ''
        self.short_code_ctrl.SetValue(value)

    def get_short_code(self):
        return self.short_code_ctrl.GetValue()

    def load_grant_admins(self, admins):
        choices = admins
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

    def get_form_values(self):
        return {
            'dept': self.get_dept(),
            'admin_approved': self.get_admin_approved(),
            'va_approved': self.get_va_approved(),
            'invoice_num': self.get_invoice_num(),
            'salary': self.get_salary(),
            'fringe': self.get_fringe(),
            'paid': self.get_paid(),
            'balance': self.get_balance(),
            'short_code': self.get_short_code(),
            'grant_admin': self.get_grant_admin(),
            'grant_admin_email': self.get_grant_admin_email()
        }
