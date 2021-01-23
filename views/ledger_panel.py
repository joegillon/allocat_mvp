import wx
import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil
import lib.month_lib as ml


class LedgerPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.pnlBg))
        layout = wx.BoxSizer(wx.HORIZONTAL)

        work_panel = self.build_work_panel(self)
        done_panel = self.build_done_panel(self)

        layout.Add(work_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(done_panel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)

    def build_work_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, size=(1000, 410)
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        work_list_panel = self.build_work_list_panel(panel)
        work_form_panel = self.build_work_form_panel(panel)

        layout.Add(work_list_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(work_form_panel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)
        return panel

    def build_work_list_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_work_list_toolbar_panel(panel)
        list_panel = self.build_work_list_list_panel(panel, tb_panel.GetSize().Width)

        layout.Add(tb_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(list_panel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)
        return panel

    def build_work_list_toolbar_panel(self, parent):
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

        self.qry_btn = uil.toolbar_button(panel, 'Query')
        layout.Add(self.qry_btn, 0, wx.ALL, 5)

        self.reload_btn = uil.toolbar_button(panel, 'Reload')
        layout.Add(self.reload_btn, 0, wx.ALL, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def build_work_list_list_panel(self, parent, width):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.work_list_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                                 size=wx.Size(980, 350),
                                                 style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        ok_img = wx.Bitmap('images/Good mark.bmp', wx.BITMAP_TYPE_BMP)
        not_ok_img = wx.Bitmap('images/Bad mark.bmp', wx.BITMAP_TYPE_BMP)
        self.work_list_ctrl.AddNamedImages('approved', ok_img)
        self.work_list_ctrl.AddNamedImages('not_approved', not_ok_img)

        self.work_list_ctrl.SetColumns([
            olv.ColumnDefn('Project', 'left', wx.LIST_AUTOSIZE, 'project',
                           minimumWidth=80),
            olv.ColumnDefn('Staff', 'left', wx.LIST_AUTOSIZE, 'employee',
                           minimumWidth=80),
            olv.ColumnDefn('GA\u2713', 'left', 70, '',
                           imageGetter=self.admin_approve_image_getter),
            olv.ColumnDefn('VA\u2713', 'right', 70, '',
                           imageGetter=self.va_approve_image_getter),
            olv.ColumnDefn('Inv #', 'right', 70, 'invoice_num'),
            olv.ColumnDefn('Grant Admin', 'left', wx.LIST_AUTOSIZE, 'grant_admin',
                           minimumWidth=120),
        ])

        layout.Add(self.work_list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        # These 2 lines are required to get scroll bars on subsequent grids
        panel.SetSizerAndFit(layout)
        self.Layout()

        return panel

    def admin_approve_image_getter(self, obj):
        if obj.admin_approved:
            return 'approved'
        return 'not_approved'

    def va_approve_image_getter(self, obj):
        if obj.va_approved:
            return 'approved'
        return 'not_approved'

    def paid_image_getter(self, obj):
        if obj.paid:
            return 'approved'
        return 'not_approved'

    def build_work_form_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_work_form_toolbar_panel(panel)
        self.work_form_panel = self.build_work_form_form_panel(panel)

        layout.Add(tb_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(self.work_form_panel, 0, wx.EXPAND | wx.ALL, 5)

        panel.SetSizerAndFit(layout)
        return panel

    def build_work_form_toolbar_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        name_lbl = uil.get_toolbar_label(panel, 'Details')
        name_lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(name_lbl, 0, wx.ALL, 5)

        btn_layout = wx.BoxSizer(wx.HORIZONTAL)
        self.save_form_btn = uil.toolbar_button(panel, 'Save')
        btn_layout.Add(self.save_form_btn, 0, wx.ALL, 5)
        layout.Add(btn_layout, 0, wx.ALIGN_RIGHT, 5)

        self.done_btn = uil.toolbar_button(panel, 'Mark Done')
        btn_layout.Add(self.done_btn, 0, wx.ALL, 5)
        layout.Add(btn_layout, 0, wx.ALIGN_RIGHT, 5)

        panel.SetSizer(layout)

        return panel

    def build_work_form_form_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.frmBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        prj_layout = wx.BoxSizer(wx.HORIZONTAL)
        self.prj_lbl = wx.StaticText(panel, wx.ID_ANY, '')
        prj_layout.Add(self.prj_lbl, 0, wx.ALL, 5)
        layout.Add(prj_layout, 0, wx.ALL, 5)

        asn_layout = wx.BoxSizer(wx.HORIZONTAL)
        self.asn_lbl = wx.StaticText(panel, wx.ID_ANY, '')
        asn_layout.Add(self.asn_lbl, 0, wx.ALL, 5)
        layout.Add(asn_layout, 0, wx.ALL, 5)

        cost_layout = wx.BoxSizer(wx.HORIZONTAL)
        self.cost_lbl = wx.StaticText(panel, wx.ID_ANY, '')
        cost_layout.Add(self.cost_lbl, 0, wx.ALL, 5)
        layout.Add(cost_layout, 0, wx.ALL, 5)

        id_layout = wx.BoxSizer(wx.HORIZONTAL)

        invoice_lbl = wx.StaticText(panel, wx.ID_ANY, 'Invoice #:')
        self.invoice_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '', size=(60, -1))
        id_layout.Add(invoice_lbl, 0, wx.ALL, 5)
        id_layout.Add(self.invoice_ctrl, 0, wx.ALL, 5)

        amount_lbl = wx.StaticText(panel, wx.ID_ANY, 'Amount:')
        self.amount_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '', size=(60, -1))
        id_layout.Add(amount_lbl, 0, wx.ALL, 5)
        id_layout.Add(self.amount_ctrl, 0, wx.ALL, 5)

        short_code_lbl = wx.StaticText(panel, wx.ID_ANY, 'Short Code:')
        self.short_code_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '', size=(100, -1))
        id_layout.Add(short_code_lbl, 0, wx.ALL, 5)
        id_layout.Add(self.short_code_ctrl, 0, wx.ALL, 5)

        layout.Add(id_layout, 0, wx.ALL, 5)

        approval_layout = wx.BoxSizer(wx.HORIZONTAL)

        admin_approved_lbl = wx.StaticText(panel, wx.ID_ANY, 'Admin Approved:')
        self.admin_approved_ctrl = wx.CheckBox(panel, wx.ID_ANY)
        approval_layout.Add(admin_approved_lbl, 0, wx.ALL, 5)
        approval_layout.Add(self.admin_approved_ctrl, 0, wx.ALL, 5)

        va_approved_lbl = wx.StaticText(panel, wx.ID_ANY, 'VA Approved:')
        self.va_approved_ctrl = wx.CheckBox(panel, wx.ID_ANY)
        approval_layout.Add(va_approved_lbl, 0, wx.ALL, 5)
        approval_layout.Add(self.va_approved_ctrl, 0, wx.ALL, 5)

        dept_lbl = wx.StaticText(panel, wx.ID_ANY, 'Dept:')
        self.dept_ctrl = wx.ComboBox(panel, wx.ID_ANY, '', size=(200, -1))
        approval_layout.Add(dept_lbl, 0, wx.ALL, 5)
        approval_layout.Add(self.dept_ctrl, 0, wx.ALL, 5)

        layout.Add(approval_layout, 0, wx.ALL, 5)

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

    def build_done_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, size=(450, 250)
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_done_toolbar_panel(panel)
        list_panel = self.build_done_list_panel(panel)

        layout.Add(tb_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(list_panel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)
        return panel

    def build_done_toolbar_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        top_line = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.get_toolbar_label(panel, 'Outstanding')
        lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        top_line.Add(lbl, wx.ALL, 5)

        total_lbl = uil.get_toolbar_label(panel, 'Total: ')
        lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        top_line.Add(total_lbl, 0, wx.ALL, 5)

        self.total_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '')
        top_line.Add(self.total_ctrl, 0, wx.ALL, 5)

        flt_lbl = uil.get_toolbar_label(panel, 'By: ')
        top_line.Add(flt_lbl, 0, wx.ALL, 5)

        self.filter_ctrl = wx.ComboBox(panel, wx.ID_ANY,
                                       choices=['All', 'Grant Admin', 'Quarter'])
        top_line.Add(self.filter_ctrl, 0, wx.ALL, 5)

        layout.Add(top_line, 0, wx.ALL, 5)

        bottom_line = wx.BoxSizer(wx.HORIZONTAL)

        self.undo_btn = uil.toolbar_button(panel, 'Undo')
        bottom_line.Add(self.undo_btn, 0, wx.ALL, 5)

        self.import_btn = uil.toolbar_button(panel, 'Import Deposits')
        bottom_line.Add(self.import_btn, 0, wx.ALL, 5)

        layout.Add(bottom_line, 0, wx.ALL, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def build_done_list_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.done_list_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                                 size=wx.Size(740, 775),
                                                 style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        self.done_list_ctrl.SetColumns([
            olv.ColumnDefn('Inv #', 'right', 70, 'invoice_num'),
            olv.ColumnDefn('Grant Admin', 'left', wx.LIST_AUTOSIZE, 'grant_admin'),
            olv.ColumnDefn('Amount', 'right', -1, 'amount',
                           fixedWidth=85,
                           stringConverter=uil.to_money),
            olv.ColumnDefn('Balance', 'right', -1, 'balance',
                           fixedWidth=85,
                           stringConverter=uil.to_money),
            olv.ColumnDefn('Qtr', 'left', 70, 'quarter'),
        ])
        self.done_list_ctrl.AutoSizeColumns()

        layout.Add(self.done_list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        # These 2 lines are required to get scroll bars on subsequent grids
        panel.SetSizerAndFit(layout)
        self.Layout()

        return panel

    def set_year(self, value):
        self.yr_ctrl.SetValue(str(value))

    def get_year(self):
        value = self.yr_ctrl.GetValue()
        return int(value) if value else None

    def set_qtr(self, choice):
        if choice:
            self.qtr_ctrl.set_selection(choice - 1, True)

    def get_qtr(self):
        return int(self.qtr_ctrl.get_selection()) + 1

    def load_work_grid(self, model):
        model.sort(key=lambda x: x.project)
        self.work_list_ctrl.SetObjects(model)

    def reload_work_grid(self, entry):
        self.work_list_ctrl.RefreshObject(entry)

    def get_work_list_selection(self):
        return self.work_list_ctrl.GetSelectedObject()

    def set_work_list_selection(self, idx):
        self.work_list_ctrl.Select(idx, on=1)
        self.work_list_ctrl.EnsureVisible(idx)

    def load_depts(self, depts):
        choices = depts
        choices.insert(0, '')
        self.dept_ctrl.Items = choices

    def set_prj_label(self, value):
        self.prj_lbl.SetLabel(value)

    def set_asn_label(self, employee, effort, frum, thru, days):
        s = '%s: %s%% effort, from %s thru %s (%s days)' % (
            employee, effort, ml.prettify(frum), ml.prettify(thru), days
        )
        self.asn_lbl.SetLabel(s)

    def set_money_label(self, salary, fringe, total_day, amount):
        if not fringe:
            fringe = '0.0'
        s = 'Salary: $%s, Fringe: %s%%, Total/Day: $%s' % (
            uil.to_money(salary),
            fringe,
            uil.to_money(total_day),
        )
        self.cost_lbl.SetLabel(s)

    def set_dept(self, value):
        if not value:
            value = ''
        self.dept_ctrl.SetValue(value)

    def get_dept(self):
        value = self.dept_ctrl.GetValue()
        return value if value else None

    def set_admin_approved(self, value):
        if value == 'Y':
            value = True
        elif value == 'N':
            value = False
        self.admin_approved_ctrl.SetValue(value)

    def get_admin_approved(self):
        return self.admin_approved_ctrl.GetValue()

    def set_va_approved(self, value):
        if value == 'Y':
            value = True
        elif value == 'N':
            value = False
        self.va_approved_ctrl.SetValue(value)

    def get_va_approved(self):
        return self.va_approved_ctrl.GetValue()

    def set_invoice_num(self, value):
        if not value:
            value = ''
        self.invoice_ctrl.SetValue(value)

    def get_invoice_num(self):
        value = self.invoice_ctrl.GetValue()
        return value if value else None

    def set_amount(self, value):
        value = uil.to_money(value) if value else ''
        self.amount_ctrl.SetValue(value)

    def get_amount(self):
        value = uil.frum_money(self.amount_ctrl.GetValue())
        return float(value) if value else None

    # def set_balance(self, value):
    #     value = uil.to_money(value) if value else ''
    #     self.balance_ctrl.SetValue(value)
    #
    # def get_balance(self):
    #     value = self.balance_ctrl.GetValue()
    #     return float(value) if value else None
    #
    # def reset_balance(self):
    #     self.set_balance(self.get_invoice_selection().balance)

    def set_short_code(self, value):
        if not value:
            value = ''
        self.short_code_ctrl.SetValue(value)

    def get_short_code(self):
        value = self.short_code_ctrl.GetValue()
        return value if value else None

    def load_grant_admins(self, admins):
        choices = admins
        choices.insert(0, '')
        self.grant_admin_ctrl.Items = choices

    def set_grant_admin(self, value):
        if not value:
            value = ''
        self.grant_admin_ctrl.SetValue(value)

    def get_grant_admin(self):
        value = self.grant_admin_ctrl.GetValue()
        return value if value else None

    def set_grant_admin_email(self, value):
        if not value:
            value = ''
        self.grant_admin_email_ctrl.SetValue(value)

    def get_grant_admin_email(self):
        value = self.grant_admin_email_ctrl.GetValue()
        return value if value else None

    def get_form_values(self):
        return {
            'dept': self.get_dept(),
            'admin_approved': self.get_admin_approved(),
            'va_approved': self.get_va_approved(),
            'invoice_num': self.get_invoice_num(),
            'amount': self.get_amount(),
            'short_code': self.get_short_code(),
            'grant_admin': self.get_grant_admin(),
            'grant_admin_email': self.get_grant_admin_email()
        }

    def load_form(self, model):
        self.set_prj_label(model.project)
        self.set_asn_label(
            model.employee, model.effort, model.frum, model.thru, model.days
        )
        self.set_money_label(
            model.salary, model.fringe, model.total_day, model.amount
        )
        self.set_dept(model.dept)
        self.set_admin_approved(model.admin_approved)
        self.set_va_approved(model.va_approved)
        self.set_invoice_num(model.invoice_num)
        self.set_amount(model.amount)
        self.set_short_code(model.short_code)
        self.set_grant_admin(model.grant_admin)
        self.set_grant_admin_email(model.grant_admin_email)

    def send_invoice(self):
        invoice = self.work_list_ctrl.GetSelectedObject()
        self.work_list_ctrl.RemoveObject(invoice)
        self.done_list_ctrl.AddObject(invoice)

    def load_done_list(self, invoices):
        self.done_list_ctrl.SetObjects(invoices)
