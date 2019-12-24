import wx
from views.asn_form_panel import AsnFormPanel
import globals as gbl
import lib.ui_lib as uil


class PrjAsnFormPanel(AsnFormPanel):
    def setProps(self, prjId):
        self.ownerRec = gbl.prjRex[prjId] if prjId else None
        self.ownerName = 'Project'
        self.ownerNameFld = 'nickname'
        self.assigneeName = 'Employee'
        self.assigneeNameFld = 'employee'

    def getComboBox(self, panel):
        return uil.ObjComboBox(panel,
                               list(gbl.empRex.values()),
                               'name',
                               'Employee',
                               style=wx.CB_READONLY)

    def setOwnerIds(self, d):
        d['employee_id'] = self.cboOwner.getSelectionId()
        d['project_id'] = self.ownerRec['id']
