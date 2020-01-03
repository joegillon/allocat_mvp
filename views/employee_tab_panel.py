import wx
import ObjectListView as olv
from views.tab_panel import TabPanel
import lib.ui_lib as uil


class EmployeeTabPanel(TabPanel):

    def set_columns(self, listCtrl):
        listCtrl.SetColumns([
            olv.ColumnDefn('Name', 'left', 200, 'name'),
            olv.ColumnDefn('FTE', 'right', wx.LIST_AUTOSIZE_USEHEADER, 'fte'),
            olv.ColumnDefn('Investigator', 'right', wx.LIST_AUTOSIZE_USEHEADER, 'investigator',
                           stringConverter=uil.toYN),
            olv.ColumnDefn('Notes', 'left', 400, 'notes'),
        ])

    def add_model_layout(self, panel, layout):
        import wx.lib.masked as masked

        formLayout = wx.BoxSizer(wx.HORIZONTAL)
        fteLbl = wx.StaticText(panel, wx.ID_ANY, 'FTE: ')
        self.fteCtrl = masked.TextCtrl(panel, wx.ID_ANY,
                                       mask='###',
                                       size=(50, -1))
        formLayout.Add(fteLbl, 0, wx.ALL, 5)
        formLayout.Add(self.fteCtrl, 0, wx.ALL, 5)

        investigatorLbl = wx.StaticText(panel, wx.ID_ANY, 'Investigator:')
        self.investigatorCtrl = wx.CheckBox(panel, wx.ID_ANY)
        formLayout.Add(investigatorLbl, 0, wx.ALL, 5)
        formLayout.Add(self.investigatorCtrl, 0, wx.ALL, 5)

        layout.Add(formLayout, 0, wx.ALL, 5)

    def get_owner_column(self):
        return olv.ColumnDefn('Project', 'left', 200, 'project')
