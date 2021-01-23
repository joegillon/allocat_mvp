import wx
import globals as gbl
import lib.ui_lib as uil


class DepositsDlg(wx.Dialog):

    def __init__(self, parent, winId, deposits):
        wx.Dialog.__init__(self, parent, winId)
        layout = wx.BoxSizer(wx.VERTICAL)

        panel = self.build_deposits_panel(self)
        layout.Add(panel, 0, wx.ALL | wx.EXPAND, 5)

        self.set_deposits_list(deposits)

        panel.SetSizerAndFit(layout)

    def build_deposits_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, size=(900, 900)
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.pnlBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_deposits_toolbar_panel(panel)
        list_panel = self.build_deposits_list_panel(panel)

        layout.Add(tb_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(list_panel, 0, wx.EXPAND | wx.ALL, 5)

        panel.SetSize(list_panel.GetSize())
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

        self.update_btn = uil.toolbar_button(panel, 'Update')
        layout.Add(self.update_btn, 0, wx.ALL, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def build_deposits_list_panel(self, parent):
        import ObjectListView as olv

        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.deposits_list_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                            # size=wx.Size(680, 775),
                                            style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        self.deposits_list_ctrl.SetColumns([
            olv.ColumnDefn('Invoice', 'left', 100, 'invoice_num'),
            olv.ColumnDefn('Deposit', 'left', 100, 'deposit_num'),
            olv.ColumnDefn('Date', 'right', 70, 'date'),
            olv.ColumnDefn('Amount', 'right', 100, 'amount',
                           stringConverter=uil.to_money),
            olv.ColumnDefn('FY', 'left', 70, 'fy'),
            olv.ColumnDefn('Qtr', 'left', 70, 'qtr'),
        ])
        # self.deposits_list_ctrl.AutoSizeColumns()

        layout.Add(self.deposits_list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        # These 2 lines are required to get scroll bars on subsequent grids
        panel.SetSizerAndFit(layout)
        self.Layout()

        return panel

    def set_deposits_list(self, deposits):
        self.deposits_list_ctrl.SetObjects(deposits)

    def get_deposits_list(self):
        return self.deposits_list_ctrl.GetObjects()

