import wx
import globals as gbl
import lib.ui_lib as uil
import lib.month_lib as ml


class AssignmentPanel(wx.Panel):
    def __init__(self, parent, owner, assignee):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        self.owner = owner
        self.assignee = assignee

        tbPanel = self.buildToolbarPanel(self)
        frmPanel = self.buildFormPanel(self)

        layout.Add(tbPanel, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(frmPanel, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(layout)

    def buildToolbarPanel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.tbBg)
        layout = wx.BoxSizer(wx.HORIZONTAL)

        self.saveBtn = uil.toolbar_button(panel, 'Save Assignment')
        self.cancelBtn = uil.toolbar_button(panel, 'Cancel')

        layout.Add(self.saveBtn, 0, wx.ALL, 5)
        layout.Add(self.cancelBtn, 0, wx.ALL, 5)

        panel.SetSizer(layout)

        return panel

    def buildFormPanel(self, parent):
        panel = wx.Panel(
            parent, wx.ID_ANY, wx.DefaultPosition, size=(-1, 375)
        )
        panel.SetBackgroundColour(gbl.COLOR_SCHEME.frmBg)
        layout = wx.BoxSizer(wx.VERTICAL)

        ownerLayout = wx.BoxSizer(wx.HORIZONTAL)
        ownerLbl = wx.StaticText(panel, wx.ID_ANY, self.owner)
        ownerLayout.Add(ownerLbl, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(ownerLayout, 0, wx.ALL | wx.EXPAND, 5)

        assigneeLayout = wx.BoxSizer(wx.HORIZONTAL)
        assigneeLbl = wx.StaticText(panel, wx.ID_ANY, 'Employee: ')
        assigneeLayout.Add(assigneeLbl, 0, wx.ALL, 5)
        if isinstance(self.assignee, str):
            assigneeLbl.SetLabelText(self.assignee)
        else:
            self.assignee.Reparent(panel)
            assigneeLayout.Add(self.assignee, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(assigneeLayout, 0, wx.ALL | wx.EXPAND, 5)

        intervalLayout = wx.BoxSizer(wx.HORIZONTAL)

        frumLbl = wx.StaticText(panel, wx.ID_ANY, 'From: *')
        intervalLayout.Add(frumLbl, 0, wx.ALL, 5)
        self.frumCtrl = uil.get_month_ctrl(panel, '')
        intervalLayout.Add(self.frumCtrl, 0, wx.ALL, 5)

        thruLbl = wx.StaticText(panel, wx.ID_ANY, 'Thru: *')
        intervalLayout.Add(thruLbl, 0, wx.ALL, 5)
        self.thruCtrl = uil.get_month_ctrl(panel, '')
        intervalLayout.Add(self.thruCtrl, 0, wx.ALL, 5)

        layout.Add(intervalLayout)

        effLayout = wx.BoxSizer(wx.HORIZONTAL)
        effortLbl = wx.StaticText(panel, wx.ID_ANY, '% Effort: *')
        effLayout.Add(effortLbl, 0, wx.ALL, 5)
        self.effortCtrl = wx.TextCtrl(panel, wx.ID_ANY, '', size=(50, -1))
        effLayout.Add(self.effortCtrl, 0, wx.ALL, 5)
        layout.Add(effLayout)

        notesLayout = wx.BoxSizer(wx.VERTICAL)
        notesLbl = wx.StaticText(panel, wx.ID_ANY, 'Notes:')
        notesLayout.Add(notesLbl, 0, wx.ALL, 5)
        self.notesCtrl = wx.TextCtrl(panel, wx.ID_ANY, '',
                                     style=wx.TE_MULTILINE, size=(500, 200))
        notesLayout.Add(self.notesCtrl, 0, wx.ALL, 5)
        layout.Add(notesLayout)

        panel.SetSizer(layout)

        return panel

    def setFrum(self, value):
        self.frumCtrl.SetValue(value)

    def getFrum(self):
        return ml.uglify(self.frumCtrl.GetValue())

    def setThru(self, value):
        self.thruCtrl.SetValue(value)

    def getThru(self):
        return ml.uglify(self.thruCtrl.GetValue())

    def setEffort(self, value):
        value = str(value) if value else ''
        self.effortCtrl.SetValue(value)

    def getEffort(self):
        return self.effortCtrl.GetValue()

    def setNotes(self, value):
        self.notesCtrl.SetValue(value)

    def getNotes(self):
        return self.notesCtrl.GetValue()

    # def getComboBox(self, panel):
    #     raise NotImplementedError("Please Implement this method")
    #
    # def onSaveClick(self, event):
    #     self.getFormData()
    #
    #     if not self.validate():
    #         return
    #
    #     self.processAsn()
    #
    #     self.Parent.Close()
    #
    # def getFormData(self):
    #     self.formData['owner'] = self.cboOwner.GetValue()
    #     self.formData['first_month'] = ml.uglify(self.frumCtrl.GetValue())
    #     self.formData['last_month'] = ml.uglify(self.thruCtrl.GetValue())
    #     self.formData['effort'] = self.effortCtrl.GetValue()
    #     self.formData['notes'] = self.notesCtrl.GetValue()
    #
    # def validate(self):
    #     import lib.validator_lib as vl
    #
    #     if self.cboOwner:
    #         if not self.formData['owner']:
    #             errMsg = '%s is required!' % self.cboOwner.Name
    #             vl.showErrMsg(self.cboOwner, errMsg)
    #             return False
    #
    #     errMsg = vl.validateTimeframe(
    #         self.formData['first_month'],
    #         self.formData['last_month'])
    #     if errMsg:
    #         vl.showErrMsg(self.frumCtrl, errMsg)
    #         return False
    #
    #     errMsg = vl.validateEffort(self.formData['effort'])
    #     if errMsg:
    #         vl.showErrMsg(self.effortCtrl, errMsg)
    #         return False
    #
    #     errMsg = vl.validateAsnTimeframe(
    #         self.formData['first_month'],
    #         self.formData['last_month'],
    #         self.ownerRec
    #     )
    #     if errMsg:
    #         vl.showErrMsg(self.frumCtrl, errMsg)
    #         return False
    #
    #     # Check for existing appointment in same timeframe
    #
    #     return True
    #
    # def setOwnerIds(self, d):
    #     raise NotImplementedError("Please Implement this method")
    #
    # def processAsn(self):
    #
    #     d = self.formData.copy()
    #     del d['owner']
    #     if self.asn is None:
    #         self.addAsn(d)
    #     else:
    #         self.updateAsn(d)
    #
    # def addAsn(self, d):
    #     self.setOwnerIds(d)
    #     try:
    #         result = asn_dal.add(Dao(), d)
    #     except Exception as ex:
    #         wx.MessageBox('Error adding %s: %s' % (self.ownerName, str(ex)))
    #         return False
    #
    #     self.asn = d.copy()
    #     self.asn['id'] = result
    #     prj_rec = gbl.prjRex[self.asn['project_id']]
    #     emp_rec = gbl.empRex[self.asn['employee_id']]
    #     self.asn['project'] = prj_rec['nickname']
    #     self.asn['employee'] = emp_rec['name']
    #     self.asn['active'] = 1
    #
    #     prj_rec['asns'].append(self.asn)
    #     emp_rec['asns'].append(self.asn)
    #
    #     self.GrandParent.theList.SetObjects(self.ownerRec['asns'])
    #     self.GrandParent.theList.RefreshItems()
    #
    # def updateAsn(self, d):
    #     self.setOwnerIds(d)
    #     try:
    #         result = asn_dal.update(Dao(), self.asn['id'], d)
    #     except Exception as ex:
    #         wx.MessageBox('Error updating %s: %s' % (self.ownerName, str(ex)))
    #         return False
    #
    #     # self.asn = d.copy()
    #     # self.asn['id'] = result
    #     # self.asn['active'] = 1
    #     # gbl.prjRex[d['project_id']] ['asns'].append(self.asn)
    #     # gbl.empRex[d['employee_id']]['asns'].append(self.asn)
    #     # self.GrandParent.theList.SetObjects(self.ownerRec['asns'])
    #
    # def onCancelClick(self, event):
    #     self.Parent.Close()
