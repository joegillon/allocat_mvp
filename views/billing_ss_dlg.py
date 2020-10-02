import wx
import globals as gbl
import lib.ui_lib as uil


class BillingSSDlg(wx.Dialog):

    def __init__(self, parent, winId, items):
        wx.Dialog.__init__(self, parent, winId, size=(600, 300))
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        self.items = items
        self.result = ''

        tb_panel = self.build_toolbar_panel(panel)
        lst_panel = self.build_list_panel(panel)

        layout.Add(tb_panel, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(lst_panel, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizerAndFit(layout)

    def build_toolbar_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        title_lbl = uil.get_toolbar_label(panel, 'Worksheets: Select Stopping Point')
        title_lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(title_lbl, 0, wx.ALL, 5)

        self.ok_btn = uil.toolbar_button(panel, 'OK')
        layout.Add(self.ok_btn, 0, wx.ALL, 5)

        self.ok_btn.Bind(wx.EVT_BUTTON, self.on_ok_click)

        panel.SetSizer(layout)

        return panel

    def build_list_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.the_list = wx.ListBox(panel, wx.ID_ANY,
                                   choices=self.items,
                                    size=(550, 300),
                                    style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        layout.Add(self.the_list, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def on_ok_click(self, evt):
        choice = self.the_list.GetSelection()
        self.result = self.items[choice]
        self.Hide()
