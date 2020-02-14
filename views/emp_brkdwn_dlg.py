import wx
import globals as gbl
import lib.ui_lib as uil


class EmployeeBreakdownDlg(wx.Dialog):

    def __init__(self, parent, winId, items):
        self.ht = (len(items) + 1) * 25
        wx.Dialog.__init__(self, parent, winId, size=(600, self.ht + 100))
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_toolbar_panel(panel)
        lst_panel = self.build_list_panel(panel,items)

        layout.Add(tb_panel, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(lst_panel, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizerAndFit(layout)

    def build_toolbar_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.name_lbl = uil.get_toolbar_label(panel, '')
        self.name_lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(self.name_lbl, 0, wx.ALL, 5)

        self.total_lbl = uil.get_toolbar_label(panel, '')
        self.total_lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(self.total_lbl, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def build_list_panel(self, parent, items):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.the_list = wx.ListCtrl(panel, wx.ID_ANY,
                                    size=(550, self.ht),
                                    style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.the_list.InsertColumn(0, 'Project', width=200)
        self.the_list.InsertColumn(1, 'From', wx.LIST_FORMAT_RIGHT)
        self.the_list.InsertColumn(2, 'Thru', wx.LIST_FORMAT_RIGHT)
        self.the_list.InsertColumn(3, '% Effort', wx.LIST_FORMAT_RIGHT)

        self.set_the_list(items)

        layout.Add(self.the_list, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def set_name_lbl(self, value):
        self.name_lbl.SetLabelText(value)

    def set_total_lbl(self, value):
        self.total_lbl.SetLabelText(value)

    def set_the_list(self, items):
        for item in items:
            self.the_list.Append(item)
