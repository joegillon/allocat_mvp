import datetime
import wx
import globals as gbl
import lib.ui_lib as uil
from presenters.ledger_presenter import LedgerPresenter


class MainLedgerWindow(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self, None, title='allocat ledger', size=(1300, 800))
        self.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_toolbar_panel(self)
        grid_panel = self.build_grid_panel(self)

        layout.Add(tb_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(grid_panel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)

        presenter = LedgerPresenter(self)
        presenter.init_view()

    def build_toolbar_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        yr_lbl = uil.get_toolbar_label(panel, 'Year:')
        yr_lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        self.yr_ctrl = wx.TextCtrl(panel, wx.ID_ANY, '')
        layout.Add(yr_lbl, 0, wx.ALL, 5)
        layout.Add(self.yr_ctrl, 0, wx.ALL, 5)

        qtr_lbl = uil.get_toolbar_label(panel, 'Qtr:')
        qtr_lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        self.qtr_ctrl = wx.RadioBox(panel, wx.ID_ANY,
                                     label='',
                                     choices=['1', '2', '3', '4'],
                                     majorDimension=1,
                                     style=wx.RA_SPECIFY_ROWS)
        layout.Add(qtr_lbl, 0, wx.ALL, 5)
        layout.Add(self.qtr_ctrl, 0, wx.ALL, 5)

        self.run_btn = uil.toolbar_button(panel, 'Run Query')
        layout.Add(self.run_btn, 0, wx.ALL, 5)

        self.help_btn = uil.get_help_btn(panel)
        layout.Add(self.help_btn, 0, wx.ALL, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def build_grid_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.grid_ctrl = wx.grid.Grid(panel, wx.ID_ANY)
        self.grid_ctrl.EnableEditing(False)
        self.grid_ctrl.CreateGrid(35, 19)
        self.grid_ctrl.SetRowLabelSize(0)

        self.grid_ctrl.SetColLabelValue(0, 'Department')
        self.grid_ctrl.SetColLabelValue(1, u'Admin \u2713')
        self.grid_ctrl.SetColLabelValue(2, u'VA \u2713')
        self.grid_ctrl.SetColLabelValue(3, 'Invoice #')
        self.grid_ctrl.SetColLabelValue(4, 'Project')
        self.grid_ctrl.SetColLabelValue(5, 'Staff')
        self.grid_ctrl.SetColLabelValue(6, '%')
        self.grid_ctrl.SetColLabelValue(7, 'Salary')
        self.grid_ctrl.SetColLabelValue(8, 'Fringe')
        self.grid_ctrl.SetColLabelValue(9, 'Total/Day')
        self.grid_ctrl.SetColLabelValue(10, 'Days')
        self.grid_ctrl.SetColLabelValue(11, 'Amount')
        self.grid_ctrl.SetColLabelValue(12, 'From')
        self.grid_ctrl.SetColLabelValue(13, 'Thru')
        self.grid_ctrl.SetColLabelValue(14, 'Paid')
        self.grid_ctrl.SetColLabelValue(15, 'Balance')
        self.grid_ctrl.SetColLabelValue(16, 'Short Code')
        self.grid_ctrl.SetColLabelValue(17, 'Grant Admin')
        self.grid_ctrl.SetColLabelValue(18, 'GA Email')

        layout.Add(self.grid_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        # These 2 lines are required to get scroll bars on subsequent grids
        panel.SetSizer(layout)
        self.Layout()

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
        return self.qtr_ctrl.GetSelection()

    def load_grid(self, rows):
        nrows = self.grid_ctrl.GetNumberRows()
        if nrows:
            self.grid_ctrl.DeleteRows(0, nrows)

        self.grid_ctrl.AppendRows(numRows=len(rows))

        for rownum in range(0, len(rows)):
            values = list(rows[rownum].values())[2:]
            for colnum in range(0, self.grid_ctrl.GetNumberCols()):
                value = values[colnum]
                if not value:
                    value = ''
                elif value == 1:
                    value = 'Y'
                elif value == 0:
                    value = 'N'
                elif isinstance(value, datetime.date):
                    value = value.strftime('%#m/%#d/%y')
                self.grid_ctrl.SetCellValue(rownum, colnum, str(value))

        self.grid_ctrl.AutoSizeColumns()

    def get_row(self, rownum):
        ncols = self.grid_ctrl.GetNumberCols()
        return [self.grid_ctrl.GetCellValue(rownum, colnum) for colnum in range(0, ncols)]

    def set_row(self, rownum, values):
        self.grid_ctrl.SetCellValue(rownum, 0, values['dept'])
        self.grid_ctrl.SetCellValue(rownum, 7, values['salary'])
        self.grid_ctrl.SetCellValue(rownum, 8, values['fringe'])
