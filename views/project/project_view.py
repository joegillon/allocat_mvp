import wx
import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil
import lib.month_lib as ml


class ProjectPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.pnlBg))
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.clearBtn = None
        self.saveBtn = None
        self.dropBtn = None
        self.helpBtn = None
        self.nameFltrCtrl = None
        self.notesFltrCtrl = None

        self.listCtrl = None
        self.nameCtrl = None
        self.nicknameCtrl = None
        self.frumCtrl = None
        self.thruCtrl = None
        self.piCtrl = None
        self.pmCtrl = None
        self.notesCtrl = None
        self.asnListCtrl = None

        listPanel = self.buildListPanel(self)
        detailPanel = self.buildDetailPanel(self)

        layout.Add(listPanel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(detailPanel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(layout)

    def buildListPanel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        tbPanel = self.buildListToolbarPanel(panel)
        lstPanel = self.buildListListPanel(panel)

        layout.Add(tbPanel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(lstPanel, 0, wx.EXPAND | wx.ALL, 5)

        panel.SetSizerAndFit(layout)
        return panel

    def buildListToolbarPanel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.HORIZONTAL)

        nameFltrLbl = uil.getToolbarLabel(panel, 'nickname:')
        nameFltrLbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(nameFltrLbl, 0, wx.ALL, 5)
        self.nameFltrCtrl = wx.SearchCtrl(panel, wx.ID_ANY, '',
                                 style=wx.TE_PROCESS_ENTER, name='nameFltrCtrl')
        self.nameFltrCtrl.ShowCancelButton(True)
        layout.Add(self.nameFltrCtrl, 0, wx.ALL, 5)

        notesFltrLbl = uil.getToolbarLabel(panel, 'Notes')
        notesFltrLbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
        layout.Add(notesFltrLbl, 0, wx.ALL, 5)

        self.notesFltrCtrl = wx.SearchCtrl(panel, wx.ID_ANY,
                                  style=wx.TE_PROCESS_ENTER, name='notesFltrCtrl')
        self.notesFltrCtrl.ShowCancelButton(True)
        layout.Add(self.notesFltrCtrl, 0, wx.ALL, 5)

        self.helpBtn = uil.getHelpBtn(panel)
        layout.Add(self.helpBtn, 0, wx.ALL, 5)

        panel.SetSizerAndFit(layout)

        return panel

    def buildListListPanel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        flags = wx.LC_REPORT | wx.SUNKEN_BORDER | wx.LC_SINGLE_SEL
        self.listCtrl = olv.ObjectListView(panel, wx.ID_ANY,
                                           size=wx.Size(-1, 600),
                                           style=flags)
        self.listCtrl.SetColumns([
            olv.ColumnDefn('Nickname', 'left', 200, 'nickname'),
            olv.ColumnDefn('From', 'left', 105, 'frum',
                           stringConverter=ml.prettify),
            olv.ColumnDefn('Thru', 'left', 100, 'thru',
                           stringConverter=ml.prettify),
            olv.ColumnDefn('PI', 'left', 150, 'investigator'),
            olv.ColumnDefn('PM', 'left', 150, 'manager'),
            olv.ColumnDefn('Name', 'left', 0, 'name'),
            olv.ColumnDefn('Notes', 'left', 0, 'notes')
        ])

        self.listCtrl.SetBackgroundColour(gbl.COLOR_SCHEME.lstHdr)

        layout.Add(self.listCtrl, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def buildDetailPanel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        tbPanel = self.buildDetailToolbarPanel(panel)
        fmPanel = self.buildDetailFormPanel(panel)
        asnPanel = self.buildAsnPanel(panel)

        layout.Add(tbPanel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(fmPanel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(asnPanel, 0, wx.EXPAND | wx.ALL, 5)

        panel.SetSizerAndFit(layout)
        return panel

    def buildDetailToolbarPanel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.clearBtn = uil.toolbar_button(panel, 'Clear Form')
        self.saveBtn = uil.toolbar_button(panel, 'Save Project')
        self.dropBtn = uil.toolbar_button(panel, 'Drop Project')

        layout.Add(self.clearBtn, 0, wx.ALL, 5)
        layout.Add(self.dropBtn, 0, wx.ALL, 5)
        layout.Add(self.saveBtn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def buildDetailFormPanel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, size=(-1, 300)
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.frmBg))
        panel.SetForegroundColour('black')

        layout = wx.BoxSizer(wx.VERTICAL)

        nameLayout = wx.BoxSizer(wx.HORIZONTAL)
        nameLbl = wx.StaticText(panel, wx.ID_ANY, 'Project Name: *')
        self.nameCtrl = wx.TextCtrl(panel, wx.ID_ANY, size=(500, -1))
        nameLayout.Add(nameLbl, 0, wx.ALL, 5)
        nameLayout.Add(self.nameCtrl, 0, wx.ALL | wx.EXPAND, 5)

        layout.Add(nameLayout, 0, wx.ALL | wx.EXPAND, 5)

        nicknameLayout = wx.BoxSizer(wx.HORIZONTAL)
        nicknameLbl = wx.StaticText(panel, wx.ID_ANY, 'Nickname: *')
        self.nicknameCtrl = wx.TextCtrl(panel, wx.ID_ANY, size=(400, -1))
        nicknameLayout.Add(nicknameLbl, 0, wx.ALL, 5)
        nicknameLayout.Add(self.nicknameCtrl, 0, wx.ALL, 5)

        layout.Add(nicknameLayout, 0, wx.ALL | wx.EXPAND, 5)

        intervalLayout = wx.BoxSizer(wx.HORIZONTAL)
        frumLbl = wx.StaticText(panel, wx.ID_ANY, 'From: *')
        self.frumCtrl = uil.getMonthCtrl(panel, '')
        intervalLayout.Add(frumLbl, 0, wx.ALL, 5)
        intervalLayout.Add(self.frumCtrl, 0, wx.ALL, 5)

        thruLbl = wx.StaticText(panel, wx.ID_ANY, 'Last Month: *')
        self.thruCtrl = uil.getMonthCtrl(panel, '')
        intervalLayout.Add(thruLbl, 0, wx.ALL, 5)
        intervalLayout.Add(self.thruCtrl, 0, wx.ALL, 5)

        layout.Add(intervalLayout, 0, wx.ALL, 5)

        personsLayout = wx.BoxSizer(wx.HORIZONTAL)

        piLbl = wx.StaticText(panel, wx.ID_ANY, 'PI:')
        self.piCtrl = uil.ObjComboBox(panel,
                                      [],
                                     'name',
                                     'Employee',
                                      style=wx.CB_READONLY)
        personsLayout.Add(piLbl, 0, wx.ALL, 5)
        personsLayout.Add(self.piCtrl, 0, wx.ALL, 5)

        pmLbl = wx.StaticText(panel, wx.ID_ANY, 'PM:')
        self.pmCtrl = uil.ObjComboBox(panel,
                                      [],
                                     'name',
                                     'Employee',
                                      style=wx.CB_READONLY)
        personsLayout.Add(pmLbl, 0, wx.ALL, 5)
        personsLayout.Add(self.pmCtrl, 0, wx.ALL, 5)

        layout.Add(personsLayout, 0, wx.ALL, 5)

        notesLayout = wx.BoxSizer(wx.VERTICAL)
        notesLbl = wx.StaticText(panel, wx.ID_ANY, 'Notes:')
        self.notesCtrl = wx.TextCtrl(panel, wx.ID_ANY,
                                     style=wx.TE_MULTILINE, size=(500, 100))
        notesLayout.Add(notesLbl, 0, wx.ALL, 5)
        notesLayout.Add(self.notesCtrl, 0, wx.ALL, 5)

        layout.Add(notesLayout, 0, wx.ALL, 5)

        panel.SetSizer(layout)
        return panel

    def buildAsnPanel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(wx.Colour(gbl.COLOR_SCHEME.tbBg))
        layout = wx.BoxSizer(wx.VERTICAL)

        tbPanel = self.buildAsnListToolbarPanel(panel)
        lstPanel = self.buildAsnListListPanel(panel)

        layout.Add(tbPanel, 0, wx.EXPAND | wx.ALL, 5)
        layout.Add(lstPanel, 0, wx.EXPAND | wx.ALL, 5)

        panel.SetSizerAndFit(layout)
        return panel

    def buildAsnListToolbarPanel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.addAsnBtn = uil.toolbar_button(panel, 'Add Assignment')
        layout.Add(self.addAsnBtn, 0, wx.ALL, 5)

        dropAsnBtn = uil.toolbar_button(panel, 'Drop Assignments')
        layout.Add(dropAsnBtn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def buildAsnListListPanel(self, parent):
        panel = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.lstBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.asnListCtrl = olv.ObjectListView(panel, wx.ID_ANY,
                                              size=wx.Size(-1, 375),
                                              style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        self.asnListCtrl.SetColumns([
            olv.ColumnDefn('Employee', 'left', 200, 'employee'),
            olv.ColumnDefn('From', 'left', 105, 'frum',
                           stringConverter=ml.prettify,
                           ),
            olv.ColumnDefn('Thru', 'left', 100, 'thru',
                           stringConverter=ml.prettify
                           ),
            olv.ColumnDefn('Effort', 'left', 100, 'effort'),
        ])

        layout.Add(self.asnListCtrl, 1, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(layout)

        return panel

    def setList(self, model):
        self.Freeze()
        sorted_data = sorted(model, key=lambda i: i.nickname.lower())
        self.listCtrl.SetObjects(sorted_data)
        self.Thaw()

    def setName(self, value):
        self.nameCtrl.SetValue(value)

    def getNameFilter(self):
        return self.nameFltrCtrl.GetValue()

    def getName(self):
        return self.nameCtrl.GetValue()

    def setNickname(self, value):
        self.nicknameCtrl.SetValue(value)

    def getNickname(self):
        return self.nicknameCtrl.GetValue()

    def setFrum(self, value):
        self.frumCtrl.SetValue(value)

    def getFrum(self):
        return self.frumCtrl.GetValue()

    def setThru(self, value):
        self.thruCtrl.SetValue(value)

    def getThru(self):
        return self.thruCtrl.GetValue()

    def loadPI(self, investigators):
        self.piCtrl.setChoices(investigators)

    def setPI(self, value):
        x = value if value else ''
        self.piCtrl.SetValue(x)

    def loadPM(self, managers):
        self.pmCtrl.setChoices(managers)

    def getPI(self):
        return self.piCtrl.GetValue

    def setPM(self, value):
        x = value if value else ''
        self.pmCtrl.SetValue(x)

    def getPM(self):
        return self.pmCtrl.GetValue()

    def setNotes(self, value):
        self.notesCtrl.SetValue(value)

    def getNotes(self):
        return self.notesCtrl.GetValue()

    def setSelectedIdx(self, idx):
        self.listCtrl.Select(idx)

    def getSelectedIdx(self):
        return self.listCtrl.GetNextSelected(-1)

    def setSelection(self, idx):
        self.listCtrl.Select(idx, on=1)

    def getSelection(self):
        return self.listCtrl.GetSelectedObject()

    def setAsnList(self, asns):
        self.Freeze()
        self.asnListCtrl.SetObjects(asns)
        self.Thaw()

