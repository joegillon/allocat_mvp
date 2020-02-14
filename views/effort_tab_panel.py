import wx
import wx.grid
import globals as gbl
import lib.month_lib as ml
import lib.ui_lib as uil


class EffTab(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_toolbar_panel(self)
        grid_panel = self.build_grid_panel(self)

        layout.Add(tb_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(grid_panel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)

    def build_toolbar_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        frum_lbl = uil.get_toolbar_label(panel, 'From:')
        frum_lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(frum_lbl, 0, wx.ALL, 5)

        self.frum_ctrl = uil.get_month_ctrl(panel, '')
        layout.Add(self.frum_ctrl, 0, wx.ALL, 5)

        thru_lbl = uil.get_toolbar_label(panel, 'Thru:')
        thru_lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(thru_lbl, 0, wx.ALL, 5)

        self.thru_ctrl = uil.get_month_ctrl(panel, '')
        layout.Add(self.thru_ctrl, 0, wx.ALL, 5)

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
        self.grid_ctrl.CreateGrid(0, 3)
        self.grid_ctrl.SetRowLabelSize(0)
        self.grid_ctrl.HideCol(0)
        self.grid_ctrl.SetColSize(1, 200)

        self.grid_ctrl.SetColLabelValue(0, 'EmpID')
        self.grid_ctrl.SetColLabelValue(1, 'Employee')
        self.grid_ctrl.SetColLabelValue(2, 'FTE')

        layout.Add(self.grid_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        # These 2 lines are required to get scroll bars on subsequent grids
        panel.SetSizer(layout)
        self.Layout()

        return panel

    def set_frum(self, value):
        self.frum_ctrl.SetValue(ml.prettify(value))

    def get_frum(self):
        return ml.uglify(self.frum_ctrl.GetValue())

    def set_thru(self, value):
        self.thru_ctrl.SetValue(ml.prettify(value))

    def get_thru(self):
        return ml.uglify(self.thru_ctrl.GetValue())

    def load_grid(self, months, rows):
        # Clear current grid
        ncols = self.grid_ctrl.GetNumberCols()
        nrows = self.grid_ctrl.GetNumberRows()
        if nrows:
            self.grid_ctrl.DeleteCols(3, ncols - 3)
            self.grid_ctrl.DeleteRows(0, nrows)

        # Resize new grid
        self.grid_ctrl.AppendCols(numCols=len(months) - 1)
        self.grid_ctrl.AppendRows(numRows=len(rows))

        self.set_grid_alignment(ncols, nrows)

        # New column labels
        colnum = 3
        for month in months:
            self.grid_ctrl.SetColLabelValue(colnum, ml.prettify(month))
            colnum += 1

        # New data
        for rownum in range(0, len(rows)):
            employee = rows[rownum].employee
            self.grid_ctrl.SetCellValue(rownum, 0, str(employee.id))
            self.grid_ctrl.SetCellValue(rownum, 1, employee.name)
            self.grid_ctrl.SetCellValue(rownum, 2, str(employee.fte))
            for colnum in range(3, len(months) + 2):
                value = rows[rownum].cells[colnum - 3].total
                self.grid_ctrl.SetCellValue(rownum, colnum, str(value))
                if value < employee.fte:
                    self.grid_ctrl.SetCellTextColour(rownum, colnum, 'red')

    def set_grid_alignment(self, ncols, nrows):
        for i in range(nrows):
            for j in range(2, ncols):
                self.grid_ctrl.SetCellAlignment(i, j, wx.ALIGN_RIGHT, wx.ALIGN_CENTER)

    def get_emp_id(self, row):
        return int(self.grid_ctrl.GetCellValue(row, 0))

    def get_emp_name(self, row):
        return self.grid_ctrl.GetCellValue(row, 1)

    def get_selected_month(self, col):
        return ml.uglify(self.grid_ctrl.GetColLabelValue(col))
