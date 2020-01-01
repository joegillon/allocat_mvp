import unittest
import wx
import globals as gbl
from unittest.mock import MagicMock
from dal.dao import Dao
from models.project import Project
from models.employee import Employee
from models.assignment import Assignment
import globals as gbl
from models.dataset import AllocatDataSet
from views.project_panel import ProjectPanel
from event_handlers.project_event_handler import ProjectEventHandler
from presenters.project_presenter import ProjectPresenter


class TestProjectPresenter(unittest.TestCase):

    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None)
        self.view = ProjectPanel(self.frame)

        gbl.theDataSet = AllocatDataSet(db_path='c:/bench/allocat/tests/allocat.db')

        # dao = Dao(db_path='c:/bench/allocat/tests/allocat.db', stateful=True)
        # prj_rex = Project.get_all(dao)
        # emp_rex = Employee.get_all(dao)
        # asn_rex = Assignment.get_all(dao)
        # dao.close()
        #
        # for prj in prj_rex:
        #     prj.asns = [asn for asn in asn_rex if asn.project_id==prj.id]
        #
        # for emp in emp_rex:
        #     emp.asns = [asn for asn in asn_rex if asn.employee_id==emp.id]

        self.interactor = ProjectEventHandler()
        self.presenter = ProjectPresenter(self.view, self.interactor)
        self.presenter.initView()

    def tearDown(self):
        self.frame.Destroy()
        self.app.Destroy()

    def testViewLoadedPIAndPM(self):
        idx = 0
        # Check the project list
        list_items = self.view.listCtrl.GetObjects()
        assert len(list_items) == 31
        item = list_items[idx]
        assert item.id == 303
        assert item.name == 'Biosimilar Merit_Waljee'
        assert item.full_name == 'Effectiveness, Safety, and Patient Preferences of Infliximab Biosimilar Medications for Inflammatory Bowel Disease'
        assert item.investigator == 'WALJEE,AKBAR, MD'
        assert item.manager == 'ARASIM,MARIA E'
        assert self.view.listCtrl.GetItemText(idx, 1) == '01/20'
        assert self.view.listCtrl.GetItemText(idx, 2) == '12/25'
        assert item.frum == '2001'
        assert item.thru == '2512'
        assert self.presenter.model[idx].frum == '2001'
        assert self.presenter.model[idx].thru == '2512'

        # Check the details form
        assert self.view.getName() == 'Biosimilar Merit_Waljee'
        assert self.view.getFullName() == 'Effectiveness, Safety, and Patient Preferences of Infliximab Biosimilar Medications for Inflammatory Bowel Disease'
        assert self.view.frumCtrl.GetValue() == '01/20'
        assert self.view.thruCtrl.GetValue() == '12/25'
        assert self.view.getFrum() == '2001'
        assert self.view.getThru() == '2512'
        assert self.view.piCtrl.GetCount() == 27
        assert self.view.pmCtrl.GetCount() == 130
        assert self.view.getPI().name == 'WALJEE,AKBAR, MD'
        assert self.view.piCtrl.getSelectionId() == 67
        assert self.view.getPM().name == 'ARASIM,MARIA E'
        assert self.view.pmCtrl.getSelectionId() == 80
        assert self.view.getButtonLabel() == 'Update Project'

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 5
        ass_items = self.view.asnListCtrl.GetObjects()
        assert len(ass_items) == 5
        assert ass_items[idx].employee == 'ARASIM,MARIA E'
        assert ass_items[idx].employee_id == 80
        assert self.presenter.model[idx].asns[0].frum == '2001'
        assert self.presenter.model[idx].asns[0].thru == '2009'
        assert self.view.asnListCtrl.GetItemText(0, 1) == '01/20'
        assert self.view.asnListCtrl.GetItemText(0, 2) == '09/20'

    def testPrjListSelectPIAndPM(self):
        idx = 1
        self.presenter.setSelection(idx)
        item = self.view.getSelection()
        assert item.id == 313
        assert item.name == 'CFIR V2 LIP'
        assert item.full_name == 'Updating the Consolidated Framework for Implementation Research (CFIR V2)'
        assert item.investigator == 'DAMSCHRODER,LAURA J'
        assert item.manager == 'REARDON,CAITLIN M'
        assert self.view.listCtrl.GetItemText(idx, 1) == '10/19'
        assert self.view.listCtrl.GetItemText(idx, 2) == '09/20'
        assert item.frum == '1910'
        assert item.thru == '2009'
        assert self.presenter.model[idx].frum == '1910'
        assert self.presenter.model[idx].thru == '2009'
        assert self.view.getButtonLabel() == 'Update Project'

        # Check the details form
        assert self.view.getName() == 'CFIR V2 LIP'
        assert self.view.getFullName() == 'Updating the Consolidated Framework for Implementation Research (CFIR V2)'
        assert self.view.frumCtrl.GetValue() == '10/19'
        assert self.view.thruCtrl.GetValue() == '09/20'
        assert self.view.getFrum() == '1910'
        assert self.view.getThru() == '2009'
        assert self.view.piCtrl.GetCount() == 27
        assert self.view.pmCtrl.GetCount() == 130
        assert self.view.getPI().name == 'DAMSCHRODER,LAURA J'
        assert self.view.piCtrl.getSelectionId() == 57
        assert self.view.getPM().name == 'REARDON,CAITLIN M'
        assert self.view.pmCtrl.getSelectionId() == 31

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 1
        ass_items = self.view.asnListCtrl.GetObjects()
        assert len(ass_items) == 1
        assert ass_items[0].employee == 'OPRA,MARILLA'
        assert ass_items[0].employee_id == 302
        assert self.presenter.model[idx].asns[0].frum == '1911'
        assert self.presenter.model[idx].asns[0].thru == '2009'
        assert self.view.asnListCtrl.GetItemText(0, 1) == '11/19'
        assert self.view.asnListCtrl.GetItemText(0, 2) == '09/20'

    def testPrjListSelectNoPI(self):
        idx = 4
        self.presenter.setSelection(idx)
        item = self.view.getSelection()
        assert item.id == 293
        assert item.name == 'IIR 17-269 Morphomics (Su)'
        assert item.full_name == 'Morphomics (Su)'
        assert item.investigator == None
        assert item.manager == 'YOULES,BRADLEY W'
        assert self.view.listCtrl.GetItemText(idx, 1) == '05/19'
        assert self.view.listCtrl.GetItemText(idx, 2) == '09/30'
        assert item.frum == '1905'
        assert item.thru == '3009'
        assert self.presenter.model[idx].frum == '1905'
        assert self.presenter.model[idx].thru == '3009'
        assert self.view.getButtonLabel() == 'Update Project'

        # Check the details form
        assert self.view.getName() == 'IIR 17-269 Morphomics (Su)'
        assert self.view.getFullName() == 'Morphomics (Su)'
        assert self.view.frumCtrl.GetValue() == '05/19'
        assert self.view.thruCtrl.GetValue() == '09/30'
        assert self.view.getFrum() == '1905'
        assert self.view.getThru() == '3009'
        assert self.view.piCtrl.GetCount() == 27
        assert self.view.pmCtrl.GetCount() == 130
        assert self.view.getPI() == None
        assert self.view.piCtrl.getSelectionId() == None
        assert self.view.getPM().name == 'YOULES,BRADLEY W'
        assert self.view.pmCtrl.getSelectionId() == 86

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 6
        ass_items = self.view.asnListCtrl.GetObjects()
        assert len(ass_items) == 6
        assert ass_items[0].employee == 'MYERS,AIMEE'
        assert ass_items[0].employee_id == 212
        assert self.presenter.model[idx].asns[0].frum == '1905'
        assert self.presenter.model[idx].asns[0].thru == '2009'
        assert self.view.asnListCtrl.GetItemText(0, 1) == '05/19'
        assert self.view.asnListCtrl.GetItemText(0, 2) == '09/20'

    def testPrjListSelectNoPM(self):
        idx = 10
        self.presenter.setSelection(idx)
        item = self.view.getSelection()
        assert item.id == 308
        assert item.name == 'LIP 20-120 (Sears)'
        assert item.full_name == 'Assessing Utilization and Access in Surgical Episodes Across Differing Healthcare Delivery Settings (Sears)'
        assert item.investigator == 'SEARS,ERICA, MD.'
        assert item.manager == None
        assert self.view.listCtrl.GetItemText(idx, 1) == '10/19'
        assert self.view.listCtrl.GetItemText(idx, 2) == '09/20'
        assert item.frum == '1910'
        assert item.thru == '2009'
        assert self.presenter.model[idx].frum == '1910'
        assert self.presenter.model[idx].thru == '2009'
        assert self.view.getButtonLabel() == 'Update Project'

        # Check the details form
        assert self.view.getName() == 'LIP 20-120 (Sears)'
        assert self.view.getFullName() == 'Assessing Utilization and Access in Surgical Episodes Across Differing Healthcare Delivery Settings (Sears)'
        assert self.view.frumCtrl.GetValue() == '10/19'
        assert self.view.thruCtrl.GetValue() == '09/20'
        assert self.view.getFrum() == '1910'
        assert self.view.getThru() == '2009'
        assert self.view.piCtrl.GetCount() == 27
        assert self.view.pmCtrl.GetCount() == 130
        assert self.view.getPI().name == 'SEARS,ERICA, MD.'
        assert self.view.piCtrl.getSelectionId() == 279
        assert self.view.getPM() == None
        assert self.view.pmCtrl.getSelectionId() == None

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 1
        ass_items = self.view.asnListCtrl.GetObjects()
        assert len(ass_items) == 1
        assert ass_items[0].employee == 'EVANS,RICHARD'
        assert ass_items[0].employee_id == 256
        assert self.presenter.model[idx].asns[0].frum == '1910'
        assert self.presenter.model[idx].asns[0].thru == '2009'
        assert self.view.asnListCtrl.GetItemText(0, 1) == '10/19'
        assert self.view.asnListCtrl.GetItemText(0, 2) == '09/20'

    def testPrjListSelectNoAsns(self):
        idx = 25
        self.presenter.setSelection(idx)
        item = self.view.getSelection()
        assert item.id == 282
        assert item.name == 'UM MTOP (Saini)'
        assert item.full_name == 'UM Michigan Treatment Optimization Program_Evaluation (Saini)'
        assert item.investigator == 'SAINI,SAMEER, MD'
        assert item.manager == 'SAFFAR,DARCY A'
        assert self.view.listCtrl.GetItemText(idx, 1) == '01/19'
        assert self.view.listCtrl.GetItemText(idx, 2) == '09/19'
        assert item.frum == '1901'
        assert item.thru == '1909'
        assert self.presenter.model[idx].frum == '1901'
        assert self.presenter.model[idx].thru == '1909'
        assert self.view.getButtonLabel() == 'Update Project'

        # Check the details form
        assert self.view.getName() == 'UM MTOP (Saini)'
        assert self.view.getFullName() == 'UM Michigan Treatment Optimization Program_Evaluation (Saini)'
        assert self.view.frumCtrl.GetValue() == '01/19'
        assert self.view.thruCtrl.GetValue() == '09/19'
        assert self.view.getFrum() == '1901'
        assert self.view.getThru() == '1909'
        assert self.view.piCtrl.GetCount() == 27
        assert self.view.pmCtrl.GetCount() == 130
        assert self.view.getPI().name == 'SAINI,SAMEER, MD'
        assert self.view.piCtrl.getSelectionId() == 63
        assert self.view.getPM().name == 'SAFFAR,DARCY A'
        assert self.view.pmCtrl.getSelectionId() == 22

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 0
        ass_items = self.view.asnListCtrl.GetObjects()
        assert len(ass_items) == 0

    def testPrjNameFilter(self):
        self.presenter.applyFilter('nameFltrCtrl', 'x', '')
        assert self.view.listCtrl.GetItemCount() == 1
        obj = self.view.listCtrl.GetFilteredObjects()[0]
        assert obj.id == 312
        idx = self.view.getSelectedIdx()
        assert idx == 0

        item = self.view.getSelection()
        assert item.id == 312
        assert item.name == 'UM ICU Expansion OPTION 2 (SAINT)'
        assert item.full_name == 'UM Expanding the Comprehensive Unit-based Safety Program (CUSP) to Reduce Central Line-Associated Blood Stream Infections (CLABSI) and Catheter-Associated Urinary Tract Infections (CAUTI) in Intensive Care Units (ICU) with Persistently Elevated Infection Rates - OPTION 1'
        assert item.investigator == None
        assert item.manager == 'FOWLER,KAREN E'
        assert self.view.listCtrl.GetItemText(idx, 1) == '09/19'
        assert self.view.listCtrl.GetItemText(idx, 2) == '09/21'
        assert item.frum == '1909'
        assert item.thru == '2109'
        assert self.view.getButtonLabel() == 'Update Project'

        # Check the details form
        assert self.view.getName() == 'UM ICU Expansion OPTION 2 (SAINT)'
        assert self.view.getFullName() == 'UM Expanding the Comprehensive Unit-based Safety Program (CUSP) to Reduce Central Line-Associated Blood Stream Infections (CLABSI) and Catheter-Associated Urinary Tract Infections (CAUTI) in Intensive Care Units (ICU) with Persistently Elevated Infection Rates - OPTION 1'
        assert self.view.frumCtrl.GetValue() == '09/19'
        assert self.view.thruCtrl.GetValue() == '09/21'
        assert self.view.getFrum() == '1909'
        assert self.view.getThru() == '2109'
        assert self.view.piCtrl.GetCount() == 27
        assert self.view.pmCtrl.GetCount() == 130
        assert self.view.getPI() == None
        assert self.view.piCtrl.getSelectionId() == None
        assert self.view.getPM().name == 'FOWLER,KAREN E'
        assert self.view.pmCtrl.getSelectionId() == 15

        # Check the assignments list
        ass_items = self.view.asnListCtrl.GetObjects()
        assert len(ass_items) == 1
        assert ass_items[0].employee == 'FOWLER,KAREN E'
        assert ass_items[0].employee_id == 15
        assert self.view.asnListCtrl.GetItemText(0, 1) == '10/19'
        assert self.view.asnListCtrl.GetItemText(0, 2) == '09/20'

    def testCancelPrjNameFilter(self):
        evt = wx.CommandEvent(wx.EVT_SEARCHCTRL_CANCEL_BTN.typeId)
        obj = self.view.nameFltrCtrl
        evt.SetEventObject(obj)
        evt.SetId(obj.GetId())
        obj.GetEventHandler().ProcessEvent(evt)

        idx = self.view.getSelectedIdx()
        list_items = self.view.listCtrl.GetObjects()
        assert len(list_items) == 31
        item = list_items[idx]
        assert item.id == 303
        assert item.name == 'Biosimilar Merit_Waljee'
        assert item.full_name == 'Effectiveness, Safety, and Patient Preferences of Infliximab Biosimilar Medications for Inflammatory Bowel Disease'
        assert item.investigator == 'WALJEE,AKBAR, MD'
        assert item.manager == 'ARASIM,MARIA E'
        assert self.view.listCtrl.GetItemText(idx, 1) == '01/20'
        assert self.view.listCtrl.GetItemText(idx, 2) == '12/25'
        assert item.frum == '2001'
        assert item.thru == '2512'
        assert self.presenter.model[idx].frum == '2001'
        assert self.presenter.model[idx].thru == '2512'
        assert self.view.getButtonLabel() == 'Update Project'

        # Check the details form
        assert self.view.getName() == 'Biosimilar Merit_Waljee'
        assert self.view.getFullName() == 'Effectiveness, Safety, and Patient Preferences of Infliximab Biosimilar Medications for Inflammatory Bowel Disease'
        assert self.view.frumCtrl.GetValue() == '01/20'
        assert self.view.thruCtrl.GetValue() == '12/25'
        assert self.view.getFrum() == '2001'
        assert self.view.getThru() == '2512'
        assert self.view.piCtrl.GetCount() == 27
        assert self.view.pmCtrl.GetCount() == 130
        assert self.view.getPI().name == 'WALJEE,AKBAR, MD'
        assert self.view.piCtrl.getSelectionId() == 67
        assert self.view.getPM().name == 'ARASIM,MARIA E'
        assert self.view.pmCtrl.getSelectionId() == 80

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 5
        ass_items = self.view.asnListCtrl.GetObjects()
        assert len(ass_items) == 5
        assert ass_items[idx].employee == 'ARASIM,MARIA E'
        assert ass_items[idx].employee_id == 80
        assert self.presenter.model[idx].asns[0].frum == '2001'
        assert self.presenter.model[idx].asns[0].thru == '2009'
        assert self.view.asnListCtrl.GetItemText(0, 1) == '01/20'
        assert self.view.asnListCtrl.GetItemText(0, 2) == '09/20'


    def testPrjNotesFilter(self):
        self.presenter.applyFilter('notesFltrCtrl', 'l', 'pau')
        assert self.view.listCtrl.GetItemCount() == 1
        obj = self.view.listCtrl.GetFilteredObjects()[0]
        assert obj.id == 285
        idx = self.view.getSelectedIdx()
        assert idx == 0

        item = self.view.getSelection()
        assert item.id == 285
        assert item.name == 'UM SPIRIT (Pfeiffer)'
        assert item.full_name == 'UM Integrated Versus Referral Care for Complex Psychiatric Disorders'
        assert item.investigator == 'PFEIFFER,PAUL, MD'
        assert item.manager == None
        assert self.view.listCtrl.GetItemText(idx, 1) == '01/19'
        assert self.view.listCtrl.GetItemText(idx, 2) == '12/20'
        assert item.frum == '1901'
        assert item.thru == '2012'
        assert self.view.getButtonLabel() == 'Update Project'

        # Check the details form
        assert self.view.getName() == 'UM SPIRIT (Pfeiffer)'
        assert self.view.getFullName() == 'UM Integrated Versus Referral Care for Complex Psychiatric Disorders'
        assert self.view.frumCtrl.GetValue() == '01/19'
        assert self.view.thruCtrl.GetValue() == '12/20'
        assert self.view.getFrum() == '1901'
        assert self.view.getThru() == '2012'
        assert self.view.piCtrl.GetCount() == 27
        assert self.view.pmCtrl.GetCount() == 130
        assert self.view.getPI().name == 'PFEIFFER,PAUL, MD'
        assert self.view.piCtrl.getSelectionId() == 75
        assert self.view.getPM() == None
        assert self.view.pmCtrl.getSelectionId() == None

        # Check the assignments list
        ass_items = self.view.asnListCtrl.GetObjects()
        assert len(ass_items) == 1
        assert ass_items[0].employee == 'TAKAMINE,LINDA'
        assert ass_items[0].employee_id == 248
        assert self.view.asnListCtrl.GetItemText(0, 1) == '01/19'
        assert self.view.asnListCtrl.GetItemText(0, 2) == '12/20'

    def testCancelNotesFilter(self):
        evt = wx.CommandEvent(wx.EVT_SEARCHCTRL_CANCEL_BTN.typeId)
        obj = self.view.notesFltrCtrl
        evt.SetEventObject(obj)
        evt.SetId(obj.GetId())
        obj.GetEventHandler().ProcessEvent(evt)

        idx = self.view.getSelectedIdx()
        list_items = self.view.listCtrl.GetObjects()
        assert len(list_items) == 31
        item = list_items[idx]
        assert item.id == 303
        assert item.name == 'Biosimilar Merit_Waljee'
        assert item.full_name == 'Effectiveness, Safety, and Patient Preferences of Infliximab Biosimilar Medications for Inflammatory Bowel Disease'
        assert item.investigator == 'WALJEE,AKBAR, MD'
        assert item.manager == 'ARASIM,MARIA E'
        assert self.view.listCtrl.GetItemText(idx, 1) == '01/20'
        assert self.view.listCtrl.GetItemText(idx, 2) == '12/25'
        assert item.frum == '2001'
        assert item.thru == '2512'
        assert self.presenter.model[idx].frum == '2001'
        assert self.presenter.model[idx].thru == '2512'
        assert self.view.getButtonLabel() == 'Update Project'

        # Check the details form
        assert self.view.getName() == 'Biosimilar Merit_Waljee'
        assert self.view.getFullName() == 'Effectiveness, Safety, and Patient Preferences of Infliximab Biosimilar Medications for Inflammatory Bowel Disease'
        assert self.view.frumCtrl.GetValue() == '01/20'
        assert self.view.thruCtrl.GetValue() == '12/25'
        assert self.view.getFrum() == '2001'
        assert self.view.getThru() == '2512'
        assert self.view.piCtrl.GetCount() == 27
        assert self.view.pmCtrl.GetCount() == 130
        assert self.view.getPI().name == 'WALJEE,AKBAR, MD'
        assert self.view.piCtrl.getSelectionId() == 67
        assert self.view.getPM().name == 'ARASIM,MARIA E'
        assert self.view.pmCtrl.getSelectionId() == 80

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 5
        ass_items = self.view.asnListCtrl.GetObjects()
        assert len(ass_items) == 5
        assert ass_items[idx].employee == 'ARASIM,MARIA E'
        assert ass_items[idx].employee_id == 80
        assert self.presenter.model[idx].asns[0].frum == '2001'
        assert self.presenter.model[idx].asns[0].thru == '2009'
        assert self.view.asnListCtrl.GetItemText(0, 1) == '01/20'
        assert self.view.asnListCtrl.GetItemText(0, 2) == '09/20'

    def testClearForm(self):
        evt = wx.CommandEvent(wx.EVT_BUTTON.typeId)
        obj = self.view.clearBtn
        evt.SetEventObject(obj)
        evt.SetId(obj.GetId())
        obj.GetEventHandler().ProcessEvent(evt)

        assert self.view.getSelectedIdx() == -1
        assert self.view.getName() == ''
        assert self.view.getFullName() == ''
        assert self.view.getFrum() == ''
        assert self.view.getThru() == ''
        assert self.view.getPI() == None
        assert self.view.piCtrl.CurrentSelection == 0
        assert self.view.getPM() == None
        assert self.view.pmCtrl.CurrentSelection == 0
        assert self.view.getNotes() == ''
        ass_items = self.view.asnListCtrl.GetObjects()
        assert len(ass_items) == 0
        assert self.view.getButtonLabel() == 'Add Project'

    def testButtonLabelChange(self):
        assert self.view.getButtonLabel() == 'Update Project'
        self.presenter.clear()
        assert self.view.getButtonLabel() == 'Add Project'
        self.presenter.setSelection(1)
        assert self.view.getButtonLabel() == 'Update Project'

    def testValidateProjectFormOnAdd(self):
        self.presenter.clear()

        # No project name entered
        errMsg = self.presenter.validate()
        assert errMsg == 'Project name required!'

        # Duplicate project name
        self.view.setName('CFIR V2 LIP')
        errMsg = self.presenter.validate()
        assert errMsg == 'Project name not unique!'

        self.view.setName('Test Prj 1')

        # No full name entered
        errMsg = self.presenter.validate()
        assert errMsg == 'Project full name required!'

        # Duplicate full name
        self.view.setFullName('Morphomics (Su)')
        errMsg = self.presenter.validate()
        assert errMsg == 'Project full name not unique!'

        self.view.setFullName('Test Project One')

        # No frum date
        errMsg = self.presenter.validate()
        assert errMsg == 'From date invalid!'

        # Bogus from dates (UI always gets 4 digits)
        self.view.setFrum('0000')       # month 00
        errMsg = self.presenter.validate()
        assert errMsg == 'From date invalid!'

        self.view.setFrum('0013')       # month 13
        errMsg = self.presenter.validate()
        assert errMsg == 'From date invalid!'

        self.view.setFrum('2001')

        # Bogus thru dates (UI always gets 4 digits)
        self.view.setThru('0000')       # month 00
        errMsg = self.presenter.validate()
        assert errMsg == 'Thru date invalid!'

        self.view.setThru('0013')       # month 13
        errMsg = self.presenter.validate()
        assert errMsg == 'Thru date invalid!'

        # Frum date later than thru date
        self.view.setThru('1912')
        errMsg = self.presenter.validate()
        assert errMsg == 'From date must precede thru date!'

        self.view.setThru('2001')   # 1 month project
        errMsg = self.presenter.validate()
        assert errMsg == None

    def testValidateProjectFormOnUpdate(self):
        self.presenter.setSelection(1)
        assert self.view.getName() == 'CFIR V2 LIP'

        # No project name entered
        self.view.setName('')
        errMsg = self.presenter.validate()
        assert errMsg == 'Project name required!'

        # Can't steal name from another project
        self.view.setName('LIP 20-121 (Saint)')
        errMsg = self.presenter.validate()
        assert errMsg == 'Project name not unique!'

        # Duplicate project name OK since it's the same project
        self.view.setName('CFIR V2 LIP')
        errMsg = self.presenter.validate()
        assert errMsg == None

        # Can rename the project with a unique name
        self.view.setName('Test Prj 1')
        errMsg = self.presenter.validate()
        assert errMsg == None

        # No project full name entered
        self.view.setFullName('')
        errMsg = self.presenter.validate()
        assert errMsg == 'Project full name required!'

        # Can't steal full name from another project
        self.view.setFullName('Morphomics (Su)')
        errMsg = self.presenter.validate()
        assert errMsg == 'Project full name not unique!'

        # Duplicate project frull name OK since it's the same project
        self.view.setFullName('Updating the Consolidated Framework for Implementation Research (CFIR V2)')
        errMsg = self.presenter.validate()
        assert errMsg == None

        # Can rename the project with a unique name
        self.view.setFullName('Test Project One')
        errMsg = self.presenter.validate()
        assert errMsg == None

        # No frum date
        self.view.setFrum('0000')
        errMsg = self.presenter.validate()
        assert errMsg == 'From date invalid!'

        self.view.setFrum('0013')       # month 13
        errMsg = self.presenter.validate()
        assert errMsg == 'From date invalid!'

        self.view.setFrum('2001')

        # Bogus thru dates (UI always gets 4 digits)
        self.view.setThru('0000')       # month 00
        errMsg = self.presenter.validate()
        assert errMsg == 'Thru date invalid!'

        self.view.setThru('0013')       # month 13
        errMsg = self.presenter.validate()
        assert errMsg == 'Thru date invalid!'

        # Frum date later than thru date
        self.view.setThru('1912')
        errMsg = self.presenter.validate()
        assert errMsg == 'From date must precede thru date!'

        self.view.setThru('2001')   # 1 month project
        errMsg = self.presenter.validate()
        assert errMsg == None

    # This test has all valid data. See above invalid tests
    def testAddUpdatesModelAndView(self):
        self.presenter.clear()
        self.view.setName('Test Prj 5')
        self.view.setFullName('Test Project Five')
        self.view.setFrum('1911')
        self.view.setThru('2004')
        self.view.setPI('KERR,EVE,MD')
        self.view.setPM('GILLON,LEAH R')
        self.view.setNotes('This is a comment.')

        self.presenter.save()

        list_items = self.view.listCtrl.GetObjects()
        assert len(list_items) == 32
        idx = self.view.getSelectedIdx()
        item = list_items[idx]
        # assert item.id == 303
        assert item.name == 'Test Prj 5'
        assert item.full_name == 'Test Project Five'
        assert item.investigator == 'KERR,EVE,MD'
        assert item.manager == 'GILLON,LEAH R'
        assert self.view.listCtrl.GetItemText(idx, 1) == '11/19'
        assert self.view.listCtrl.GetItemText(idx, 2) == '04/20'
        assert item.frum == '1911'
        assert item.thru == '2004'

        prj_model = self.presenter.model[idx]
        # assert prj_model.id == 300
        assert prj_model.name == 'Test Prj 5'
        assert prj_model.full_name == 'Test Project Five'
        assert prj_model.frum == '1911'
        assert prj_model.thru == '2004'
        assert prj_model.investigator == 'KERR,EVE,MD'
        assert prj_model.investigator_id == 7
        assert prj_model.manager == 'GILLON,LEAH R'
        assert prj_model.manager_id == 52
        assert prj_model.notes == 'This is a comment.'
        assert prj_model.active == 1
        assert prj_model.asns == []

        ass_items = self.view.asnListCtrl.GetObjects()
        assert len(ass_items) == 0

    # This test has all valid data. See above invalid tests
    def testUpdateUpdatesModelAndView(self):
        idx = 6
        self.presenter.setSelection(idx)
        item = self.view.getSelection()
        assert item.id == 279
        assert item.name == 'LIP 19-111 (Prescott)'
        assert item.full_name == 'LIP 19-111 Prescott'
        assert item.investigator == None
        assert item.manager == 'LUGINBILL,KAITLYN A'
        assert self.view.listCtrl.GetItemText(idx, 1) == '04/19'
        assert self.view.listCtrl.GetItemText(idx, 2) == '09/19'
        assert item.frum == '1904'
        assert item.thru == '1909'
        assert self.presenter.model[idx].frum == '1904'
        assert self.presenter.model[idx].thru == '1909'
        assert self.view.getButtonLabel() == 'Update Project'

        # Check the details form
        assert self.view.getName() == 'LIP 19-111 (Prescott)'
        assert self.view.getFullName() == 'LIP 19-111 Prescott'
        assert self.view.frumCtrl.GetValue() == '04/19'
        assert self.view.thruCtrl.GetValue() == '09/19'
        assert self.view.getFrum() == '1904'
        assert self.view.getThru() == '1909'
        assert self.view.piCtrl.GetCount() == 27
        assert self.view.pmCtrl.GetCount() == 130
        assert self.view.getPI() == None
        assert self.view.piCtrl.getSelectionId() == None
        assert self.view.getPM().name == 'LUGINBILL,KAITLYN A'
        assert self.view.pmCtrl.getSelectionId() == 120

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 1
        ass_items = self.view.asnListCtrl.GetObjects()
        assert len(ass_items) == 1
        assert ass_items[0].employee == 'SEEYLE,SARAH'
        assert ass_items[0].employee_id == 278
        assert self.presenter.model[idx].asns[0].frum == '1904'
        assert self.presenter.model[idx].asns[0].thru == '1909'
        assert self.view.asnListCtrl.GetItemText(0, 1) == '04/19'
        assert self.view.asnListCtrl.GetItemText(0, 2) == '09/19'

        self.view.setName('Test Prj 5')
        self.view.setFullName('Test Project Five')
        self.view.setFrum('1905')
        self.view.setThru('1908')
        self.view.setPI('KERR,EVE,MD')
        self.view.setPM('GILLON,LEAH R')
        self.view.setNotes('This is a comment.')

        self.presenter.save()

        list_items = self.view.listCtrl.GetObjects()
        assert len(list_items) == 31
        idx = self.view.getSelectedIdx()
        assert idx == 6
        item = list_items[idx]
        assert item.id == 279
        assert item.name == 'Test Prj 5'
        assert item.full_name == 'Test Project Five'
        assert item.investigator == 'KERR,EVE,MD'
        assert item.manager == 'GILLON,LEAH R'
        assert self.view.listCtrl.GetItemText(idx, 1) == '05/19'
        assert self.view.listCtrl.GetItemText(idx, 2) == '08/19'
        assert item.frum == '1905'
        assert item.thru == '1908'

        prj_model = self.presenter.model[idx]
        assert prj_model.id == 279
        assert prj_model.name == 'Test Prj 5'
        assert prj_model.full_name == 'Test Project Five'
        assert prj_model.frum == '1905'
        assert prj_model.thru == '1908'
        assert prj_model.investigator == 'KERR,EVE,MD'
        assert prj_model.investigator_id == 7
        assert prj_model.manager == 'GILLON,LEAH R'
        assert prj_model.manager_id == 52
        assert prj_model.notes == 'This is a comment.'
        assert prj_model.active == 1

        assert len(self.presenter.model[idx].asns) == 1
        ass_items = self.view.asnListCtrl.GetObjects()
        assert len(ass_items) == 1
        assert ass_items[0].employee == 'SEEYLE,SARAH'
        assert ass_items[0].employee_id == 278
        assert self.presenter.model[idx].asns[0].frum == '1904'
        assert self.presenter.model[idx].asns[0].thru == '1909'
        assert self.view.asnListCtrl.GetItemText(0, 1) == '04/19'
        assert self.view.asnListCtrl.GetItemText(0, 2) == '09/19'

    def testDropUpdatesModelAndView(self):
        idx = 6
        self.presenter.setSelection(idx)
        item = self.view.getSelection()
        assert item.id == 279
        assert item.name == 'LIP 19-111 (Prescott)'
        assert item.full_name == 'LIP 19-111 Prescott'
        assert item.investigator == None
        assert item.manager == 'LUGINBILL,KAITLYN A'
        assert self.view.listCtrl.GetItemText(idx, 1) == '04/19'
        assert self.view.listCtrl.GetItemText(idx, 2) == '09/19'
        assert item.frum == '1904'
        assert item.thru == '1909'
        assert self.presenter.model[idx].frum == '1904'
        assert self.presenter.model[idx].thru == '1909'
        assert self.view.getButtonLabel() == 'Update Project'

        # Check the details form
        assert self.view.getName() == 'LIP 19-111 (Prescott)'
        assert self.view.getFullName() == 'LIP 19-111 Prescott'
        assert self.view.frumCtrl.GetValue() == '04/19'
        assert self.view.thruCtrl.GetValue() == '09/19'
        assert self.view.getFrum() == '1904'
        assert self.view.getThru() == '1909'
        assert self.view.piCtrl.GetCount() == 27
        assert self.view.pmCtrl.GetCount() == 130
        assert self.view.getPI() == None
        assert self.view.piCtrl.getSelectionId() == None
        assert self.view.getPM().name == 'LUGINBILL,KAITLYN A'
        assert self.view.pmCtrl.getSelectionId() == 120

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 1
        ass_items = self.view.asnListCtrl.GetObjects()
        assert len(ass_items) == 1
        assert ass_items[0].employee == 'SEEYLE,SARAH'
        assert ass_items[0].employee_id == 278
        assert self.presenter.model[idx].asns[0].frum == '1904'
        assert self.presenter.model[idx].asns[0].thru == '1909'
        assert self.view.asnListCtrl.GetItemText(0, 1) == '04/19'
        assert self.view.asnListCtrl.GetItemText(0, 2) == '09/19'

        self.presenter.drop()

        idx = self.view.getSelectedIdx()
        item = self.view.getSelection()
        assert item.id == 280
        assert item.name == 'LIP 19-112 (Kullgren-DeWitt) Visceral MDM'
        assert item.full_name == 'LIP 19-112 Understanding the Influence of Patient and Provider Visceral Factors on Clinical Decision-Making (Kullgren-DeWitt)'
        assert item.investigator == None
        assert item.manager == 'DEWITT,JEFFREY,POSTDOC'
        assert self.view.listCtrl.GetItemText(idx, 1) == '03/19'
        assert self.view.listCtrl.GetItemText(idx, 2) == '09/20'
        assert item.frum == '1903'
        assert item.thru == '2009'
        assert self.presenter.model[idx].frum == '1903'
        assert self.presenter.model[idx].thru == '2009'
        assert self.view.getButtonLabel() == 'Update Project'

        # Check the details form
        assert self.view.getName() == 'LIP 19-112 (Kullgren-DeWitt) Visceral MDM'
        assert self.view.getFullName() == 'LIP 19-112 Understanding the Influence of Patient and Provider Visceral Factors on Clinical Decision-Making (Kullgren-DeWitt)'
        assert self.view.frumCtrl.GetValue() == '03/19'
        assert self.view.thruCtrl.GetValue() == '09/20'
        assert self.view.getFrum() == '1903'
        assert self.view.getThru() == '2009'
        assert self.view.piCtrl.GetCount() == 27
        assert self.view.pmCtrl.GetCount() == 130
        assert self.view.getPI() == None
        assert self.view.piCtrl.getSelectionId() == None
        assert self.view.getPM().name == 'DEWITT,JEFFREY,POSTDOC'
        assert self.view.pmCtrl.getSelectionId() == 284

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 5
        ass_items = self.view.asnListCtrl.GetObjects()
        assert len(ass_items) == 5
        assert ass_items[0].employee == 'DEWITT,JEFFREY,POSTDOC'
        assert ass_items[0].employee_id == 284
        assert self.presenter.model[idx].asns[0].frum == '1903'
        assert self.presenter.model[idx].asns[0].thru == '1909'
        assert self.view.asnListCtrl.GetItemText(0, 1) == '03/19'
        assert self.view.asnListCtrl.GetItemText(0, 2) == '09/19'

    def testDropLastRecUpdatesModelAndView(self):
        idx = 30
        self.presenter.setSelection(idx)
        item = self.view.getSelection()
        assert item.id == 300
        assert item.name == 'VERAM CHRT (Adams)'
        assert item.full_name == 'VERAM Assessing the Capacity of Community-based Providers to Care for Older Veterans (Adams)'
        assert item.investigator == None
        assert item.manager == 'SAFFAR,DARCY A'
        assert self.view.listCtrl.GetItemText(idx, 1) == '04/19'
        assert self.view.listCtrl.GetItemText(idx, 2) == '09/19'
        assert item.frum == '1904'
        assert item.thru == '1909'
        assert self.presenter.model[idx].frum == '1904'
        assert self.presenter.model[idx].thru == '1909'
        assert self.view.getButtonLabel() == 'Update Project'

        # Check the details form
        assert self.view.getName() == 'VERAM CHRT (Adams)'
        assert self.view.getFullName() == 'VERAM Assessing the Capacity of Community-based Providers to Care for Older Veterans (Adams)'
        assert self.view.frumCtrl.GetValue() == '04/19'
        assert self.view.thruCtrl.GetValue() == '09/19'
        assert self.view.getFrum() == '1904'
        assert self.view.getThru() == '1909'
        assert self.view.piCtrl.GetCount() == 27
        assert self.view.pmCtrl.GetCount() == 130
        assert self.view.getPI() == None
        assert self.view.piCtrl.getSelectionId() == None
        assert self.view.getPM().name == 'SAFFAR,DARCY A'
        assert self.view.pmCtrl.getSelectionId() == 22

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 5
        ass_items = self.view.asnListCtrl.GetObjects()
        assert len(ass_items) == 5
        assert ass_items[0].employee == 'SAFFAR,DARCY A'
        assert ass_items[0].employee_id == 22
        assert self.presenter.model[idx].asns[0].frum == '1904'
        assert self.presenter.model[idx].asns[0].thru == '1904'
        assert self.view.asnListCtrl.GetItemText(0, 1) == '04/19'
        assert self.view.asnListCtrl.GetItemText(0, 2) == '04/19'

        self.presenter.drop()

        idx = self.view.getSelectedIdx()
        item = self.view.getSelection()
        assert item.id == 310
        assert item.name == 'UM_RO1 (Ilgen & LIn)'
        assert item.full_name == 'Enhancing the impact of behavioral pain management on MAT outcomes (Ilgen & Lin)'
        assert item.investigator == 'ILGEN,MARK PHD'
        assert item.manager == 'LEWIS (STINCHOMB),MANDY'
        assert self.view.listCtrl.GetItemText(idx, 1) == '09/19'
        assert self.view.listCtrl.GetItemText(idx, 2) == '08/23'
        assert item.frum == '1909'
        assert item.thru == '2308'
        assert self.presenter.model[idx].frum == '1909'
        assert self.presenter.model[idx].thru == '2308'
        assert self.view.getButtonLabel() == 'Update Project'

        # Check the details form
        assert self.view.getName() == 'UM_RO1 (Ilgen & LIn)'
        assert self.view.getFullName() == 'Enhancing the impact of behavioral pain management on MAT outcomes (Ilgen & Lin)'
        assert self.view.frumCtrl.GetValue() == '09/19'
        assert self.view.thruCtrl.GetValue() == '08/23'
        assert self.view.getFrum() == '1909'
        assert self.view.getThru() == '2308'
        assert self.view.piCtrl.GetCount() == 27
        assert self.view.pmCtrl.GetCount() == 130
        assert self.view.getPI().name == 'ILGEN,MARK PHD'
        assert self.view.piCtrl.getSelectionId() == 73
        assert self.view.getPM().name == 'LEWIS (STINCHOMB),MANDY'
        assert self.view.pmCtrl.getSelectionId() == 250

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 1
        ass_items = self.view.asnListCtrl.GetObjects()
        assert len(ass_items) == 1
        assert ass_items[0].employee == 'LEWIS (STINCHOMB),MANDY'
        assert ass_items[0].employee_id == 250
        assert self.presenter.model[idx].asns[0].frum == '1910'
        assert self.presenter.model[idx].asns[0].thru == '2009'
        assert self.view.asnListCtrl.GetItemText(0, 1) == '10/19'
        assert self.view.asnListCtrl.GetItemText(0, 2) == '09/20'
