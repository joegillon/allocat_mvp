import wx
import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil

class ImportPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.pnlBg))

        layout = wx.BoxSizer(wx.HORIZONTAL)

        rex_panel = self.build_rex_panel(self)
        match_panel = self.build_match_panel(self)

        layout.Add(rex_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(match_panel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)

    def build_rex_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, size=(500, 500)
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_rex_toolbar_panel(panel)
        list_panel = self.build_rex_list_panel(panel)

        layout.Add(tb_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(list_panel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)
        return panel

    def build_rex_toolbar_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.import_btn = uil.toolbar_button(panel, 'Import Salary Data')
        layout.Add(self.import_btn, 0, wx.ALL, 5)

        self.update_allocat_btn = uil.toolbar_button(panel, 'Update allocat')
        layout.Add(self.update_allocat_btn, 0, wx.ALL, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def build_rex_list_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.list_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                            size=wx.Size(480, 640),
                                            style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        match_img = wx.Bitmap('images/Apply.bmp', wx.BITMAP_TYPE_BMP)
        mismatch_img = wx.Bitmap('images/Alert.bmp', wx.BITMAP_TYPE_BMP)
        self.list_ctrl.AddNamedImages('match', match_img)
        self.list_ctrl.AddNamedImages('mismatch', mismatch_img)

        self.list_ctrl.SetColumns([
            olv.ColumnDefn('Employee', 'left', wx.LIST_AUTOSIZE, 'name'),
            olv.ColumnDefn('Salary', 'right', 100, 'salary'),
            olv.ColumnDefn('Fringe', 'right', 100, 'fringe'),
            olv.ColumnDefn('Match', 'right', 30, '', imageGetter=self.match_image_getter)
        ])
        self.list_ctrl.AutoSizeColumns()

        layout.Add(self.list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        # These 2 lines are required to get scroll bars on subsequent grids
        panel.SetSizerAndFit(layout)
        self.Layout()

        return panel

    def match_image_getter(self, obj):
        if obj.matched:
            return 'match'
        return 'mismatch'

    def build_match_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, size=(500, 500)
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_match_toolbar_panel(panel)
        form_panel = self.build_match_form_panel(panel)

        layout.Add(tb_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(form_panel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)
        return panel

    def build_match_toolbar_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.match_btn = uil.toolbar_button(panel, 'Match!')
        layout.Add(self.match_btn, 0, wx.ALL, 5)

        self.no_match_btn = uil.toolbar_button(panel, 'No Match!')
        layout.Add(self.no_match_btn, 0, wx.ALL, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def build_match_form_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_BOLD)
        matches_lbl = wx.StaticText(panel, wx.ID_ANY, "Possible Matches")
        matches_lbl.SetFont(font)
        matches_lbl.SetForegroundColour(gbl.COLOR_SCHEME.tbBg)

        layout.Add(matches_lbl, 0, wx.ALL, 5)

        self.matches_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                            size=wx.Size(480, 600),
                                            style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        self.matches_ctrl.SetColumns([
            olv.ColumnDefn('Name', 'left', wx.LIST_AUTOSIZE, 'name'),
            olv.ColumnDefn('Score', 'right', 100, 'score'),
        ])
        self.matches_ctrl.AutoSizeColumns()

        layout.Add(self.matches_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        # These 2 lines are required to get scroll bars on subsequent grids
        panel.SetSizerAndFit(layout)
        self.Layout()

        return panel

    def display(self, ss_rex):
        ss_rex.sort(key=lambda x: x.name)
        self.list_ctrl.SetObjects(ss_rex)
        self.list_ctrl.Refresh()

    def get_list_selection(self):
        return self.list_ctrl.GetSelectedObject()

    def get_list(self):
        return self.list_ctrl.GetObjects()

    def load_mismatch_list(self, items):
        self.matches_ctrl.SetObjects(items)

    def get_match_selection(self):
        obj = self.matches_ctrl.GetSelectedObject()
        idx = self.matches_ctrl.GetIndexOf(obj)
        return obj, idx

    def set_match_selection(self, obj):
        self.matches_ctrl.SelectObject(obj, ensureVisible=True)

    def get_rex(self):
        return self.list_ctrl.GetObjects()
