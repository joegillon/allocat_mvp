import wx
import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil


class LedgerPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.pnlBg))
        layout = wx.BoxSizer(wx.HORIZONTAL)

        unpaid_panel = self.build_unpaid_panel(self)
        deposits_panel = self.build_deposits_panel(self)

        layout.Add(unpaid_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(deposits_panel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)

    def build_unpaid_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, size=(740, 500)
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_unpaid_toolbar_panel(panel)
        list_panel = self.build_unpaid_list_panel(panel)

        layout.Add(tb_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(list_panel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)
        return panel

    def build_unpaid_toolbar_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.get_toolbar_label(panel, 'Outstanding Bills')
        lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(lbl, 0, wx.ALL, 5)

        total_lbl = uil.get_toolbar_label(panel, 'Total: ')
        lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(total_lbl, 0, wx.ALL, 5)

        self.total_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '')
        layout.Add(self.total_ctrl, 0, wx.ALL, 5)

        flt_lbl = uil.get_toolbar_label(panel, 'By: ')
        layout.Add(flt_lbl, 0, wx.ALL, 5)

        self.filter_ctrl = wx.ComboBox(panel, wx.ID_ANY,
                                       choices=['All', 'Project', 'Grant Admin', 'Quarter'])
        layout.Add(self.filter_ctrl, 0, wx.ALL, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def build_unpaid_list_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.unpaid_list_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                            size=wx.Size(740, 775),
                                            style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        self.unpaid_list_ctrl.SetColumns([
            olv.ColumnDefn('Project', 'left', wx.LIST_AUTOSIZE, 'project'),
            olv.ColumnDefn('Staff', 'left', wx.LIST_AUTOSIZE, 'employee'),
            olv.ColumnDefn('Inv #', 'right', 70, 'invoice_num'),
            olv.ColumnDefn('Grant Admin', 'left', wx.LIST_AUTOSIZE, 'grant_admin'),
            olv.ColumnDefn('Grant Admin Email', 'left', wx.LIST_AUTOSIZE, 'grant_admin_email'),
            olv.ColumnDefn('Amount', 'right', -1, 'amount',
                           fixedWidth=85,
                           stringConverter=uil.to_money),
            olv.ColumnDefn('Balance', 'right', -1, 'balance',
                           fixedWidth=85,
                           stringConverter=uil.to_money),
            olv.ColumnDefn('Qtr', 'left', 70, 'quarter'),
        ])
        self.unpaid_list_ctrl.AutoSizeColumns()

        layout.Add(self.unpaid_list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        # These 2 lines are required to get scroll bars on subsequent grids
        panel.SetSizerAndFit(layout)
        self.Layout()

        return panel

    def build_deposits_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, size=(680, 500)
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_deposits_toolbar_panel(panel)
        list_panel = self.build_deposits_list_panel(panel)

        layout.Add(tb_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(list_panel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)
        return panel

    def build_deposits_toolbar_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.get_toolbar_label(panel, 'Deposits')
        lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(lbl, 0, wx.ALL, 5)

        self.import_btn = uil.toolbar_button(panel, 'Import')
        layout.Add(self.import_btn, 0, wx.ALL, 5)

        self.update_btn = uil.toolbar_button(panel, 'Update')
        layout.Add(self.update_btn, 0, wx.ALL, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def build_deposits_list_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.deposits_list_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                            size=wx.Size(680, 775),
                                            style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        self.deposits_list_ctrl.SetColumns([
            olv.ColumnDefn('Invoice', 'left', wx.LIST_AUTOSIZE, 'invoice_num'),
            olv.ColumnDefn('Deposit', 'left', wx.LIST_AUTOSIZE, 'deposit_num'),
            olv.ColumnDefn('Date', 'right', 70, 'date'),
            olv.ColumnDefn('Amount', 'left', wx.LIST_AUTOSIZE, 'amount',
                           stringConverter=uil.to_money),
            olv.ColumnDefn('FY', 'left', wx.LIST_AUTOSIZE, 'fy'),
            olv.ColumnDefn('Qtr', 'left', 70, 'qtr'),
        ])
        self.deposits_list_ctrl.AutoSizeColumns()

        layout.Add(self.deposits_list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        # These 2 lines are required to get scroll bars on subsequent grids
        panel.SetSizerAndFit(layout)
        self.Layout()

        return panel

    def set_unpaid_list(self, rex):
        self.unpaid_list_ctrl.SetObjects(rex)

    def get_unpaid_list_selection(self):
        return self.unpaid_list_ctrl.GetSelectedObject()

    def set_total(self, value):
        self.total_ctrl.SetValue(uil.to_money(value))

    def set_deposits_list(self, rex):
        self.deposits_list_ctrl.SetObjects(rex)

    def get_deposits_list(self):
        return self.deposits_list_ctrl.GetObjects()

    def refresh_invoices(self):
        self.unpaid_list_ctrl.SetObjects(gbl.dataset.get_ledger_data())
