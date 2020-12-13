import wx
import globals as gbl
import lib.ui_lib as uil


class MonthBreakdownDialog(wx.Dialog):

    def __init__(self, parent, winId, employee, month, items):
        self.ht = (len(items) + 1) * 25
        wx.Dialog.__init__(self, parent, winId, size=(400, self.ht + 100))
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_toolbar_panel(panel, employee, month)
        lst_panel = self.build_list_panel(panel, items)

        layout.Add(tb_panel, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(lst_panel, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizerAndFit(layout)

    def build_toolbar_panel(self, parent, employee, month):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        s = '%s @ %s' % (employee, month)
        self.lbl = uil.get_toolbar_label(panel, s)
        self.lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(self.lbl, 0, wx.ALL, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def build_list_panel(self, parent, items):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.the_list = wx.ListCtrl(panel, wx.ID_ANY,
                                    size=(450, self.ht),
                                    style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        self.the_list.InsertColumn(0, 'Project', width=200)
        self.the_list.InsertColumn(1, '% Effort', wx.LIST_FORMAT_RIGHT)

        self.set_the_list(items)

        layout.Add(self.the_list, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def set_the_list(self, items):
        for item in items:
            self.the_list.Append(item)
