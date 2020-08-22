import wx
import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil
from presenters.ledger_presenter import LedgerPresenter


class LedgerWindow(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self, None, title='allocat ledger',
                          style=wx.DEFAULT_FRAME_STYLE)
        self.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        list_panel = self.build_list_panel(self)
        detail_panel = self.build_detail_panel(self)

        layout.Add(list_panel, 0, wx.EXPAND|wx.ALL, 5)
        layout.Add(detail_panel, 0, wx.EXPAND|wx.ALL, 5)

        self.SetSizerAndFit(layout)

        presenter = LedgerPresenter(self)
        presenter.init_view()

    def build_list_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_list_toolbar_panel(panel)
        list_panel = self.build_list_list_panel(panel, tb_panel.GetSize().Width)

        layout.Add(tb_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(list_panel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)
        return panel

    def build_list_toolbar_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        yr_lbl = uil.get_toolbar_label(panel, 'Year:')
        yr_lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        self.yr_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '', size=(50, -1))
        layout.Add(yr_lbl, 0, wx.ALL, 5)
        layout.Add(self.yr_ctrl, 0, wx.ALL, 5)

        self.qtr_ctrl = uil.RadioGroup(panel, 'Qtr:', ['1', '2', '3', '4'])
        layout.Add(self.qtr_ctrl, 0, wx.ALL, 5)

        self.run_btn = uil.toolbar_button(panel, 'Query')
        layout.Add(self.run_btn, 0, wx.ALL, 5)

        self.import_btn = uil.toolbar_button(panel, 'Import')
        layout.Add(self.import_btn, 0, wx.ALL, 5)

        self.invoice_btn = uil.toolbar_button(panel, 'VA\u2713')
        layout.Add(self.invoice_btn, 0, wx.ALL, 5)

        self.invoice_btn = uil.toolbar_button(panel, 'GA\u2713')
        layout.Add(self.invoice_btn, 0, wx.ALL, 5)

        self.invoice_btn = uil.toolbar_button(panel, 'Script')
        layout.Add(self.invoice_btn, 0, wx.ALL, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def build_list_list_panel(self, parent, width):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.list_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                            size=wx.Size(width, 375),
                                            style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.list_ctrl.SetColumns([
            olv.ColumnDefn('Project', 'left', wx.LIST_AUTOSIZE, 'project'),
            olv.ColumnDefn('Staff', 'left', wx.LIST_AUTOSIZE, 'staff'),
            # olv.ColumnDefn('%', 'right', wx.LIST_AUTOSIZE, 'pct_effort'),
            # olv.ColumnDefn('Department', 'left', wx.LIST_AUTOSIZE, 'department'),
            olv.ColumnDefn('GA\u2713', 'right', 70, 'admin_approved',
                           stringConverter=uil.toYN),
            olv.ColumnDefn('VA\u2713', 'right', 70, 'va_approved',
                           stringConverter=uil.toYN),
            olv.ColumnDefn('Invoice #', 'right', 100, 'invoice_num'),
            # olv.ColumnDefn('Salary', 'right', wx.LIST_AUTOSIZE, 'base_salary'),
            # olv.ColumnDefn('Fringe', 'right', wx.LIST_AUTOSIZE, 'fringe'),
            # olv.ColumnDefn('Total/Day', 'right', wx.LIST_AUTOSIZE, 'total_day'),
            # olv.ColumnDefn('Days', 'right', wx.LIST_AUTOSIZE, 'days'),
            # olv.ColumnDefn('Amount', 'right', wx.LIST_AUTOSIZE, 'amount'),
            # olv.ColumnDefn('From', 'left', wx.LIST_AUTOSIZE, 'frum'),
            # olv.ColumnDefn('Thru', 'left', wx.LIST_AUTOSIZE, 'thru'),
            # olv.ColumnDefn('Paid', 'left', wx.LIST_AUTOSIZE, 'paid'),
            # olv.ColumnDefn('Balance', 'left', wx.LIST_AUTOSIZE, 'balance'),
            # olv.ColumnDefn('Short Code', 'left', wx.LIST_AUTOSIZE, 'short_code'),
            olv.ColumnDefn('Grant Admin', 'left', wx.LIST_AUTOSIZE, 'grant_admin'),
            # olv.ColumnDefn('GA Email', 'left', wx.LIST_AUTOSIZE, 'grant_admin_email'),
        ])
        self.list_ctrl.AutoSizeColumns()

        layout.Add(self.list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        # These 2 lines are required to get scroll bars on subsequent grids
        panel.SetSizerAndFit(layout)
        self.Layout()

        return panel

    def build_detail_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_detail_toolbar_panel(panel)
        self.fm_panel = self.build_detail_form_panel(panel)

        layout.Add(tb_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(self.fm_panel, 0, wx.EXPAND | wx.ALL, 5)

        panel.SetSizerAndFit(layout)
        return panel

    def build_detail_toolbar_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.name_lbl = uil.get_toolbar_label(panel, 'Details')
        self.name_lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(self.name_lbl, 0, wx.ALL, 5)

        btn_layout = wx.BoxSizer(wx.HORIZONTAL)
        self.clear_btn = uil.toolbar_button(panel, 'Clear Entry')
        btn_layout.Add(self.clear_btn, 0, wx.ALL, 5)
        self.drop_btn = uil.toolbar_button(panel, 'Drop Entry')
        btn_layout.Add(self.drop_btn, 0, wx.ALL, 5)
        self.update_btn = uil.toolbar_button(panel, 'Update Entry')
        btn_layout.Add(self.update_btn, 0, wx.ALL, 5)
        layout.Add(btn_layout, 0, wx.ALIGN_RIGHT, 5)

        panel.SetSizer(layout)

        return panel

    def build_detail_form_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.frmBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        grant_layout = wx.BoxSizer(wx.HORIZONTAL)

        dept_lbl = wx.StaticText(panel, wx.ID_ANY, 'Dept:')
        self.dept_ctrl = wx.ComboBox(panel, wx.ID_ANY, '', size=(200, -1))
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
        self.invoice_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '', size=(60, -1))
        grant_layout.Add(invoice_lbl, 0, wx.ALL, 5)
        grant_layout.Add(self.invoice_ctrl, 0, wx.ALL, 5)

        layout.Add(grant_layout, 0, wx.ALL, 5)

        prj_layout = wx.BoxSizer(wx.HORIZONTAL)
        prj_lbl = wx.StaticText(panel, wx.ID_ANY, 'Project:')
        self.prj_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '',
                                    size=(500, -1),
                                    style=wx.TE_READONLY)
        prj_layout.Add(prj_lbl, 0, wx.ALL, 5)
        prj_layout.Add(self.prj_ctrl, 0, wx.ALL, 5)
        layout.Add(prj_layout, 0, wx.ALL, 5)

        emp_layout = wx.BoxSizer(wx.HORIZONTAL)

        emp_lbl = wx.StaticText(panel, wx.ID_ANY, 'Staff:')
        self.emp_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '',
                                    size=(300, -1),
                                    style=wx.TE_READONLY)
        emp_layout.Add(emp_lbl, 0, wx.ALL, 5)
        emp_layout.Add(self.emp_ctrl, 0, wx.ALL, 5)

        frum_lbl = wx.StaticText(panel, wx.ID_ANY, 'From:')
        self.frum_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '',
                                     size=(50, -1),
                                     style=wx.TE_READONLY)
        emp_layout.Add(frum_lbl, 0, wx.ALL, 5)
        emp_layout.Add(self.frum_ctrl, 0, wx.ALL, 5)

        thru_lbl = wx.StaticText(panel, wx.ID_ANY, 'Thru:')
        self.thru_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '',
                                     size=(50, -1),
                                     style=wx.TE_READONLY)
        emp_layout.Add(thru_lbl, 0, wx.ALL, 5)
        emp_layout.Add(self.thru_ctrl, 0, wx.ALL, 5)

        eff_lbl = wx.StaticText(panel, wx.ID_ANY, '% Effort:')
        self.eff_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '',
                                    size=(30, -1),
                                    style=wx.TE_READONLY)
        emp_layout.Add(eff_lbl, 0, wx.ALL, 5)
        emp_layout.Add(self.eff_ctrl, 0, wx.ALL, 5)

        layout.Add(emp_layout, 0, wx.ALL, 5)

        cost_layout = wx.BoxSizer(wx.HORIZONTAL)

        salary_lbl = wx.StaticText(panel, wx.ID_ANY, 'Salary:')
        self.salary_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '', size=(60, -1))
        cost_layout.Add(salary_lbl, 0, wx.ALL, 5)
        cost_layout.Add(self.salary_ctrl, 0, wx.ALL, 5)

        fringe_lbl = wx.StaticText(panel, wx.ID_ANY, 'Fringe:')
        self.fringe_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '', size=(50, -1))
        cost_layout.Add(fringe_lbl, 0, wx.ALL, 5)
        cost_layout.Add(self.fringe_ctrl, 0, wx.ALL, 5)

        total_lbl = wx.StaticText(panel, wx.ID_ANY, 'Total/Day:')
        self.total_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '', size=(50, -1))
        cost_layout.Add(total_lbl, 0, wx.ALL, 5)
        cost_layout.Add(self.total_ctrl, 0, wx.ALL, 5)

        days_lbl = wx.StaticText(panel, wx.ID_ANY, 'Days:')
        self.days_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '', size=(30, -1))
        cost_layout.Add(days_lbl, 0, wx.ALL, 5)
        cost_layout.Add(self.days_ctrl, 0, wx.ALL, 5)

        amt_lbl = wx.StaticText(panel, wx.ID_ANY, 'Amount:')
        self.amt_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '', size=(150, -1))
        cost_layout.Add(amt_lbl, 0, wx.ALL, 5)
        cost_layout.Add(self.amt_ctrl, 0, wx.ALL, 5)

        layout.Add(cost_layout, 0, wx.ALL, 5)

        due_layout = wx.BoxSizer(wx.HORIZONTAL)

        paid_lbl = wx.StaticText(panel, wx.ID_ANY, 'Paid:')
        self.paid_ctrl = wx.CheckBox(panel, wx.ID_ANY)
        due_layout.Add(paid_lbl, 0, wx.ALL, 5)
        due_layout.Add(self.paid_ctrl, 0, wx.ALL, 5)

        balance_lbl = wx.StaticText(panel, wx.ID_ANY, 'Balance:')
        self.balance_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '', size=(150, -1))
        due_layout.Add(balance_lbl, 0, wx.ALL, 5)
        due_layout.Add(self.balance_ctrl, 0, wx.ALL, 5)

        short_code_lbl = wx.StaticText(panel, wx.ID_ANY, 'Short Code:')
        self.short_code_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '', size=(100, -1))
        due_layout.Add(short_code_lbl, 0, wx.ALL, 5)
        due_layout.Add(self.short_code_ctrl, 0, wx.ALL, 5)

        layout.Add(due_layout, 0, wx.ALL, 5)

        admin_layout = wx.BoxSizer(wx.HORIZONTAL)

        grant_admin_lbl = wx.StaticText(panel, wx.ID_ANY, 'Grant Admin:')
        self.grant_admin_ctrl = wx.ComboBox(panel, wx.ID_ANY, '', size=(200, -1))
        admin_layout.Add(grant_admin_lbl, 0, wx.ALL, 5)
        admin_layout.Add(self.grant_admin_ctrl, 0, wx.ALL, 5)

        grant_admin_email_lbl = wx.StaticText(panel, wx.ID_ANY, 'Email:')
        self.grant_admin_email_ctrl = wx.TextCtrl(panel, wx.ID_ANY, size=(300, -1))
        admin_layout.Add(grant_admin_email_lbl, 0, wx.ALL, 5)
        admin_layout.Add(self.grant_admin_email_ctrl, 0, wx.ALL, 5)

        layout.Add(admin_layout, 0, wx.ALL, 0)

        panel.SetSizerAndFit(layout)

        return panel

    def set_year(self, value):
        self.yr_ctrl.SetValue(str(value))

    def get_year(self):
        return self.yr_ctrl.GetValue()

    def set_qtr(self, value):
        if value in [10, 11, 12]:
            choice = 0
        elif value in [1, 2, 3]:
            choice = 1
        elif value in [4, 5, 6]:
            choice = 2
        else:
            choice = 3
        self.qtr_ctrl.SetSelection(choice)

    def get_qtr(self):
        option = self.qtr_ctrl.get_selection()
        if option:
            return int(option) - 1
        return -1

    def load_grid(self, model):
        self.list_ctrl.SetObjects(model)

    def get_selection(self):
        return self.list_ctrl.GetSelectedObject()

    def set_row(self, rownum, values):
        self.grid_ctrl.SetCellValue(rownum, 0, values['dept'])
        self.grid_ctrl.SetCellValue(rownum, 7, values['salary'])
        self.grid_ctrl.SetCellValue(rownum, 8, values['fringe'])

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
        if value == 'Y':
            value = True
        elif value == 'N':
            value = False
        self.admin_approved_ctrl.SetValue(value)

    def get_admin_approved(self):
        return True if self.admin_approved_ctrl.GetValue() == 'Y' else False

    def set_va_approved(self, value):
        if value == 'Y':
            value = True
        elif value == 'N':
            value = False
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
        self.prj_ctrl.SetValue(value)

    def set_employee(self, value):
        self.emp_ctrl.SetValue(value)

    def set_frum(self, value):
        self.frum_ctrl.SetValue(value)

    def set_thru(self, value):
        self.thru_ctrl.SetValue(value)

    def set_effort(self, value):
        self.eff_ctrl.SetValue(str(value))

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

    def set_days(self, value):
        self.days_ctrl.SetValue(str(value))

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

    def load_form(self, model):
        self.set_dept(model.department)
        self.set_admin_approved(model.admin_approved)
        self.set_va_approved(model.va_approved)
        self.set_invoice_num(model.invoice_num)
        self.set_project(model.project)
        self.set_employee(model.staff)
        self.set_frum(model.frum)
        self.set_thru(model.thru)
        self.set_effort(model.pct_effort)
        self.set_salary(model.base_salary)
        self.set_fringe(model.fringe)
        self.set_total(model.total_day)
        self.set_days(model.days)
        self.set_amount(model.amount)
        self.set_paid(model.paid)
        self.set_balance(model.balance)
        self.set_short_code(model.short_code)
        self.set_grant_admin(model.grant_admin)
        self.set_grant_admin_email(model.grant_admin_email)
