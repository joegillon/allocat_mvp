import wx
import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil


class BillingPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.pnlBg))
        layout = wx.BoxSizer(wx.HORIZONTAL)

        billing_panel = self.build_billing_panel(self)
        # detail_panel = self.build_detail_panel(self)
        #
        layout.Add(billing_panel, 0, wx.EXPAND | wx.ALL, 5)
        # layout.Add(detail_panel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)

    def build_billing_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, size=(680, 500)
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_toolbar_panel(panel)
        # list_panel = self.build_list_panel(panel)

        layout.Add(tb_panel, 0, wx.EXPAND | wx.ALL, 5)
        # layout.Add(list_panel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)
        return panel

    def build_toolbar_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        lbl = uil.get_toolbar_label(panel, 'Billing Records')
        lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(lbl, 0, wx.ALL, 5)

        self.import_btn = uil.toolbar_button(panel, 'Import')
        layout.Add(self.import_btn, 0, wx.ALL, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def build_list_panel(self, parent):
        pass