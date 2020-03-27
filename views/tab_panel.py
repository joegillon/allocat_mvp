import wx
import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil
import lib.month_lib as ml


class TabPanel(wx.Panel):

    def __init__(self, parent, model_name):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.pnlBg))
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.model_name = model_name

        list_panel = self.build_list_panel(self)
        detail_panel = self.build_detail_panel(self)

        layout.Add(list_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(detail_panel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)

    def build_list_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_list_toolbar_panel(panel)
        lst_panel = self.build_list_list_panel(panel)

        layout.Add(tb_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(lst_panel, 0, wx.EXPAND | wx.ALL, 5)

        panel.SetSizerAndFit(layout)
        return panel

    def build_list_toolbar_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.HORIZONTAL)

        name_fltr_lbl = uil.get_toolbar_label(panel, 'Name:')
        name_fltr_lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(name_fltr_lbl, 0, wx.ALL, 5)
        self.name_fltr_ctrl = wx.SearchCtrl(panel, wx.ID_ANY, '',
                                            style=wx.TE_PROCESS_ENTER, name='nameFltrCtrl')
        self.name_fltr_ctrl.ShowCancelButton(True)
        layout.Add(self.name_fltr_ctrl, 0, wx.ALL, 5)

        notes_fltr_lbl = uil.get_toolbar_label(panel, 'Notes')
        notes_fltr_lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(notes_fltr_lbl, 0, wx.ALL, 5)

        self.notes_fltr_ctrl = wx.SearchCtrl(panel, wx.ID_ANY,
                                             style=wx.TE_PROCESS_ENTER, name='notesFltrCtrl')
        self.notes_fltr_ctrl.ShowCancelButton(True)
        layout.Add(self.notes_fltr_ctrl, 0, wx.ALL, 5)

        self.active_btn = uil.toolbar_button(panel, 'ALL')
        self.active_btn.set_size(wx.Size(70, -1))
        layout.Add(self.active_btn, 0, wx.ALL, 0)

        self.help_btn = uil.get_help_btn(panel)
        layout.Add(self.help_btn, 0, wx.ALL, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def build_list_list_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        flags = wx.LC_REPORT | wx.SUNKEN_BORDER | wx.LC_SINGLE_SEL
        self.list_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                            size=wx.Size(-1, 600),
                                            style=flags)
        self.set_columns(self.list_ctrl)
        self.list_ctrl.SetBackgroundColour(gbl.COLOR_SCHEME.lstHdr)

        layout.Add(self.list_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def set_columns(self, listCtrl):
        raise NotImplementedError("Please Implement this method")

    def build_detail_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_detail_toolbar_panel(panel)
        self.fm_panel = self.build_detail_form_panel(panel)
        self.asn_panel = self.build_asn_panel(panel)

        layout.Add(tb_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(self.fm_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(self.asn_panel, 0, wx.EXPAND | wx.ALL, 5)

        panel.SetSizerAndFit(layout)
        return panel

    def build_detail_toolbar_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.clear_btn = uil.toolbar_button(panel, 'Clear Form')
        self.save_btn = uil.toolbar_button(panel, 'Update ' + self.model_name)

        self.drop_btn = uil.toolbar_button(panel, 'Drop ' + self.model_name)
        self.drop_btn.set_size((150, -1))

        layout.Add(self.clear_btn, 0, wx.ALL, 5)
        layout.Add(self.drop_btn, 0, wx.ALL, 5)
        layout.Add(self.save_btn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def build_detail_form_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, size=(-1, 300)
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.frmBg))
        panel.SetForegroundColour('black')

        layout = wx.BoxSizer(wx.VERTICAL)

        name_layout = wx.BoxSizer(wx.HORIZONTAL)
        name_lbl = wx.StaticText(panel, wx.ID_ANY, self.model_name + ' Name: *')
        self.name_ctrl = wx.TextCtrl(panel, wx.ID_ANY, size=(400, -1))
        name_layout.Add(name_lbl, 0, wx.ALL, 5)
        name_layout.Add(self.name_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        layout.Add(name_layout, 0, wx.ALL | wx.EXPAND, 5)

        self.add_model_layout(panel, layout)

        notes_layout = wx.BoxSizer(wx.VERTICAL)
        notes_lbl = wx.StaticText(panel, wx.ID_ANY, 'Notes:')
        self.notes_ctrl = wx.TextCtrl(panel, wx.ID_ANY,
                                      style=wx.TE_MULTILINE, size=(500, 100))
        notes_layout.Add(notes_lbl, 0, wx.ALL, 5)
        notes_layout.Add(self.notes_ctrl, 0, wx.ALL, 5)

        layout.Add(notes_layout, 0, wx.ALL, 5)

        panel.SetSizer(layout)
        return panel

    def add_model_layout(self, panel, layout):
        raise NotImplementedError("Please Implement this method")

    def build_asn_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        tb_panel = self.build_asn_list_toolbar_panel(panel)
        asn_list_panel = self.build_asn_list_list_panel(panel)

        layout.Add(tb_panel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(asn_list_panel, 0, wx.EXPAND | wx.ALL, 5)

        panel.SetSizerAndFit(layout)
        return panel

    def build_asn_list_toolbar_panel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.add_asn_btn = uil.toolbar_button(panel, 'Add Assignment')
        layout.Add(self.add_asn_btn, 0, wx.ALL, 5)

        self.drop_asn_btn = uil.toolbar_button(panel, 'Drop Assignments')
        # self.drop_asn_btn.set_size((150, -1))
        layout.Add(self.drop_asn_btn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def build_asn_list_list_panel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.asn_list_ctrl = olv.ObjectListView(panel, wx.ID_ANY,
                                                size=wx.Size(-1, 375),
                                                style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        self.asn_list_ctrl.SetColumns([
            self.get_owner_column(),
            olv.ColumnDefn('From', 'left', 105, 'frum',
                           stringConverter=ml.prettify,
                           ),
            olv.ColumnDefn('Thru', 'left', 100, 'thru',
                           stringConverter=ml.prettify
                           ),
            olv.ColumnDefn('Effort', 'left', 100, 'effort'),
        ])

        layout.Add(self.asn_list_ctrl, 1, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def get_owner_column(self):
        raise NotImplementedError("Please Implement this method")

    def set_list(self, model):
        self.Freeze()
        self.list_ctrl.SetObjects(model)
        self.Thaw()

    def set_name(self, value):
        self.name_ctrl.SetValue(value)

    def get_name(self):
        return self.name_ctrl.GetValue()

    def set_notes(self, value):
        if not value:
            value = ''
        self.notes_ctrl.SetValue(value)

    def get_notes(self):
        return self.notes_ctrl.GetValue()

    def set_selected_idx(self, idx):
        self.selected_idx = idx

    def get_selected_idx(self):
        return self.list_ctrl.GetNextSelected(-1)
        # return self.selectedIdx

    def set_selection(self, idx):
        self.list_ctrl.Select(idx, on=1)

    def get_selection(self):
        return self.list_ctrl.GetSelectedObject()

    def clear_selection(self):
        self.list_ctrl.Select(self.get_selected_idx(), on=False)

    def set_save_button_label(self, value):
        self.save_btn.set_label(value)

    def get_save_button_label(self):
        return self.save_btn.get_label()

    def set_active_button_label(self, value):
        self.active_btn.set_label(value)

    def get_active_button_label(self):
        return self.active_btn.label

    def get_asn_selections(self):
        return self.asn_list_ctrl.GetSelectedObjects()

    def set_asn_list(self, asns):
        self.Freeze()
        self.asn_list_ctrl.SetObjects(asns)
        self.Thaw()

    def get_selected_asns(self):
        return self.asn_list_ctrl.GetSelectedObjects()

    # def set_drop_asn_btn_lbl(self, txt):
    #     self.drop_asn_btn.set_label(txt)

    def set_details_active(self, active, model):
        if active:
            self.drop_btn.set_label('Drop %s'% model)
            # self.set_drop_asn_btn_lbl('Drop Assignments')
            self.fm_panel.Enable()
            self.asn_panel.Enable()
            self.asn_list_ctrl.SetTextColour('black')
            self.clear_btn.Enable()
            self.save_btn.Enable()
        else:
            self.drop_btn.set_label('Undrop %s'% model)
            # self.set_drop_asn_btn_lbl('Undrop Assignments')
            self.fm_panel.Disable()
            self.asn_panel.Disable()
            self.asn_list_ctrl.SetTextColour('gray')
            self.clear_btn.Disable()
            self.save_btn.Disable()
