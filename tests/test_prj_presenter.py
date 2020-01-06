import unittest
import wx
import globals as gbl
from models.dataset import AllocatDataSet
from presenters.project_presenter import ProjectPresenter


class TestProjectPresenter(unittest.TestCase):

    def setUp(self):
        gbl.dataset = AllocatDataSet(db_path='c:/bench/allocat/tests/allocat.db')
        self.app = wx.App()
        self.frame = wx.Frame(None)

        self.presenter = ProjectPresenter(self.frame)
        self.presenter.init_view()

    def tearDown(self):
        self.frame.Destroy()
        self.app.Destroy()

    def testViewLoadedPIAndPM(self):
        idx = 0
        # Check the project list
        list_items = self.presenter.view.list_ctrl.GetObjects()
        assert len(list_items) == 31
        item = list_items[idx]
        assert item.id == 303
        assert item.name == 'Biosimilar Merit_Waljee'
        assert item.full_name == 'Effectiveness, Safety, and Patient Preferences of Infliximab Biosimilar Medications for Inflammatory Bowel Disease'
        assert item.investigator == 'WALJEE,AKBAR, MD'
        assert item.manager == 'ARASIM,MARIA E'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 1) == '01/20'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 2) == '12/25'
        assert item.frum == '2001'
        assert item.thru == '2512'
        assert self.presenter.model[idx].frum == '2001'
        assert self.presenter.model[idx].thru == '2512'

        # Check the details form
        assert self.presenter.view.get_name() == 'Biosimilar Merit_Waljee'
        assert self.presenter.view.get_full_name() == 'Effectiveness, Safety, and Patient Preferences of Infliximab Biosimilar Medications for Inflammatory Bowel Disease'
        assert self.presenter.view.frum_ctrl.GetValue() == '01/20'
        assert self.presenter.view.thru_ctrl.GetValue() == '12/25'
        assert self.presenter.view.get_frum() == '2001'
        assert self.presenter.view.get_thru() == '2512'
        assert self.presenter.view.pi_ctrl.GetCount() == 27
        assert self.presenter.view.pm_ctrl.GetCount() == 130
        assert self.presenter.view.get_pi().name == 'WALJEE,AKBAR, MD'
        assert self.presenter.view.pi_ctrl.get_selection_id() == 67
        assert self.presenter.view.get_pm().name == 'ARASIM,MARIA E'
        assert self.presenter.view.pm_ctrl.get_selection_id() == 80
        assert self.presenter.view.get_button_label() == 'Update Project'

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 5
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 5
        assert ass_items[idx].employee == 'ARASIM,MARIA E'
        assert ass_items[idx].employee_id == 80
        assert self.presenter.model[idx].asns[0].frum == '2001'
        assert self.presenter.model[idx].asns[0].thru == '2009'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 1) == '01/20'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 2) == '09/20'

    def testPrjListSelectPIAndPM(self):
        idx = 1
        self.presenter.set_selection(idx)
        item = self.presenter.view.get_selection()
        assert item.id == 313
        assert item.name == 'CFIR V2 LIP'
        assert item.full_name == 'Updating the Consolidated Framework for Implementation Research (CFIR V2)'
        assert item.investigator == 'DAMSCHRODER,LAURA J'
        assert item.manager == 'REARDON,CAITLIN M'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 1) == '10/19'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 2) == '09/20'
        assert item.frum == '1910'
        assert item.thru == '2009'
        assert self.presenter.model[idx].frum == '1910'
        assert self.presenter.model[idx].thru == '2009'
        assert self.presenter.view.get_button_label() == 'Update Project'

        # Check the details form
        assert self.presenter.view.get_name() == 'CFIR V2 LIP'
        assert self.presenter.view.get_full_name() == 'Updating the Consolidated Framework for Implementation Research (CFIR V2)'
        assert self.presenter.view.frum_ctrl.GetValue() == '10/19'
        assert self.presenter.view.thru_ctrl.GetValue() == '09/20'
        assert self.presenter.view.get_frum() == '1910'
        assert self.presenter.view.get_thru() == '2009'
        assert self.presenter.view.pi_ctrl.GetCount() == 27
        assert self.presenter.view.pm_ctrl.GetCount() == 130
        assert self.presenter.view.get_pi().name == 'DAMSCHRODER,LAURA J'
        assert self.presenter.view.pi_ctrl.get_selection_id() == 57
        assert self.presenter.view.get_pm().name == 'REARDON,CAITLIN M'
        assert self.presenter.view.pm_ctrl.get_selection_id() == 31

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 1
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 1
        assert ass_items[0].employee == 'OPRA,MARILLA'
        assert ass_items[0].employee_id == 302
        assert self.presenter.model[idx].asns[0].frum == '1911'
        assert self.presenter.model[idx].asns[0].thru == '2009'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 1) == '11/19'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 2) == '09/20'

    def testPrjListSelectNoPI(self):
        idx = 4
        self.presenter.set_selection(idx)
        item = self.presenter.view.get_selection()
        assert item.id == 293
        assert item.name == 'IIR 17-269 Morphomics (Su)'
        assert item.full_name == 'Morphomics (Su)'
        assert item.investigator == None
        assert item.manager == 'YOULES,BRADLEY W'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 1) == '05/19'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 2) == '09/30'
        assert item.frum == '1905'
        assert item.thru == '3009'
        assert self.presenter.model[idx].frum == '1905'
        assert self.presenter.model[idx].thru == '3009'
        assert self.presenter.view.get_button_label() == 'Update Project'

        # Check the details form
        assert self.presenter.view.get_name() == 'IIR 17-269 Morphomics (Su)'
        assert self.presenter.view.get_full_name() == 'Morphomics (Su)'
        assert self.presenter.view.frum_ctrl.GetValue() == '05/19'
        assert self.presenter.view.thru_ctrl.GetValue() == '09/30'
        assert self.presenter.view.get_frum() == '1905'
        assert self.presenter.view.get_thru() == '3009'
        assert self.presenter.view.pi_ctrl.GetCount() == 27
        assert self.presenter.view.pm_ctrl.GetCount() == 130
        assert self.presenter.view.get_pi() == None
        assert self.presenter.view.pi_ctrl.get_selection_id() == None
        assert self.presenter.view.get_pm().name == 'YOULES,BRADLEY W'
        assert self.presenter.view.pm_ctrl.get_selection_id() == 86

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 6
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 6
        assert ass_items[0].employee == 'MYERS,AIMEE'
        assert ass_items[0].employee_id == 212
        assert self.presenter.model[idx].asns[0].frum == '1905'
        assert self.presenter.model[idx].asns[0].thru == '2009'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 1) == '05/19'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 2) == '09/20'

    def testPrjListSelectNoPM(self):
        idx = 10
        self.presenter.set_selection(idx)
        item = self.presenter.view.get_selection()
        assert item.id == 308
        assert item.name == 'LIP 20-120 (Sears)'
        assert item.full_name == 'Assessing Utilization and Access in Surgical Episodes Across Differing Healthcare Delivery Settings (Sears)'
        assert item.investigator == 'SEARS,ERICA, MD.'
        assert item.manager == None
        assert self.presenter.view.list_ctrl.GetItemText(idx, 1) == '10/19'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 2) == '09/20'
        assert item.frum == '1910'
        assert item.thru == '2009'
        assert self.presenter.model[idx].frum == '1910'
        assert self.presenter.model[idx].thru == '2009'
        assert self.presenter.view.get_button_label() == 'Update Project'

        # Check the details form
        assert self.presenter.view.get_name() == 'LIP 20-120 (Sears)'
        assert self.presenter.view.get_full_name() == 'Assessing Utilization and Access in Surgical Episodes Across Differing Healthcare Delivery Settings (Sears)'
        assert self.presenter.view.frum_ctrl.GetValue() == '10/19'
        assert self.presenter.view.thru_ctrl.GetValue() == '09/20'
        assert self.presenter.view.get_frum() == '1910'
        assert self.presenter.view.get_thru() == '2009'
        assert self.presenter.view.pi_ctrl.GetCount() == 27
        assert self.presenter.view.pm_ctrl.GetCount() == 130
        assert self.presenter.view.get_pi().name == 'SEARS,ERICA, MD.'
        assert self.presenter.view.pi_ctrl.get_selection_id() == 279
        assert self.presenter.view.get_pm() == None
        assert self.presenter.view.pm_ctrl.get_selection_id() == None

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 1
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 1
        assert ass_items[0].employee == 'EVANS,RICHARD'
        assert ass_items[0].employee_id == 256
        assert self.presenter.model[idx].asns[0].frum == '1910'
        assert self.presenter.model[idx].asns[0].thru == '2009'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 1) == '10/19'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 2) == '09/20'

    def testPrjListSelectNoAsns(self):
        idx = 25
        self.presenter.set_selection(idx)
        item = self.presenter.view.get_selection()
        assert item.id == 282
        assert item.name == 'UM MTOP (Saini)'
        assert item.full_name == 'UM Michigan Treatment Optimization Program_Evaluation (Saini)'
        assert item.investigator == 'SAINI,SAMEER, MD'
        assert item.manager == 'SAFFAR,DARCY A'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 1) == '01/19'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 2) == '09/19'
        assert item.frum == '1901'
        assert item.thru == '1909'
        assert self.presenter.model[idx].frum == '1901'
        assert self.presenter.model[idx].thru == '1909'
        assert self.presenter.view.get_button_label() == 'Update Project'

        # Check the details form
        assert self.presenter.view.get_name() == 'UM MTOP (Saini)'
        assert self.presenter.view.get_full_name() == 'UM Michigan Treatment Optimization Program_Evaluation (Saini)'
        assert self.presenter.view.frum_ctrl.GetValue() == '01/19'
        assert self.presenter.view.thru_ctrl.GetValue() == '09/19'
        assert self.presenter.view.get_frum() == '1901'
        assert self.presenter.view.get_thru() == '1909'
        assert self.presenter.view.pi_ctrl.GetCount() == 27
        assert self.presenter.view.pm_ctrl.GetCount() == 130
        assert self.presenter.view.get_pi().name == 'SAINI,SAMEER, MD'
        assert self.presenter.view.pi_ctrl.get_selection_id() == 63
        assert self.presenter.view.get_pm().name == 'SAFFAR,DARCY A'
        assert self.presenter.view.pm_ctrl.get_selection_id() == 22

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 0
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 0

    def testPrjNameFilter(self):
        self.presenter.apply_filter('name_fltr_ctrl', 'x', '')
        assert self.presenter.view.list_ctrl.GetItemCount() == 1
        obj = self.presenter.view.list_ctrl.GetFilteredObjects()[0]
        assert obj.id == 312
        idx = self.presenter.view.get_selected_idx()
        assert idx == 0

        item = self.presenter.view.get_selection()
        assert item.id == 312
        assert item.name == 'UM ICU Expansion OPTION 2 (SAINT)'
        assert item.full_name == 'UM Expanding the Comprehensive Unit-based Safety Program (CUSP) to Reduce Central Line-Associated Blood Stream Infections (CLABSI) and Catheter-Associated Urinary Tract Infections (CAUTI) in Intensive Care Units (ICU) with Persistently Elevated Infection Rates - OPTION 1'
        assert item.investigator == None
        assert item.manager == 'FOWLER,KAREN E'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 1) == '09/19'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 2) == '09/21'
        assert item.frum == '1909'
        assert item.thru == '2109'
        assert self.presenter.view.get_button_label() == 'Update Project'

        # Check the details form
        assert self.presenter.view.get_name() == 'UM ICU Expansion OPTION 2 (SAINT)'
        assert self.presenter.view.get_full_name() == 'UM Expanding the Comprehensive Unit-based Safety Program (CUSP) to Reduce Central Line-Associated Blood Stream Infections (CLABSI) and Catheter-Associated Urinary Tract Infections (CAUTI) in Intensive Care Units (ICU) with Persistently Elevated Infection Rates - OPTION 1'
        assert self.presenter.view.frum_ctrl.GetValue() == '09/19'
        assert self.presenter.view.thru_ctrl.GetValue() == '09/21'
        assert self.presenter.view.get_frum() == '1909'
        assert self.presenter.view.get_thru() == '2109'
        assert self.presenter.view.pi_ctrl.GetCount() == 27
        assert self.presenter.view.pm_ctrl.GetCount() == 130
        assert self.presenter.view.get_pi() == None
        assert self.presenter.view.pi_ctrl.get_selection_id() == None
        assert self.presenter.view.get_pm().name == 'FOWLER,KAREN E'
        assert self.presenter.view.pm_ctrl.get_selection_id() == 15

        # Check the assignments list
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 1
        assert ass_items[0].employee == 'FOWLER,KAREN E'
        assert ass_items[0].employee_id == 15
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 1) == '10/19'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 2) == '09/20'

    def testCancelPrjNameFilter(self):
        evt = wx.CommandEvent(wx.EVT_SEARCHCTRL_CANCEL_BTN.typeId)
        obj = self.presenter.view.name_fltr_ctrl
        evt.SetEventObject(obj)
        evt.SetId(obj.GetId())
        obj.GetEventHandler().ProcessEvent(evt)

        idx = self.presenter.view.get_selected_idx()
        list_items = self.presenter.view.list_ctrl.GetObjects()
        assert len(list_items) == 31
        item = list_items[idx]
        assert item.id == 303
        assert item.name == 'Biosimilar Merit_Waljee'
        assert item.full_name == 'Effectiveness, Safety, and Patient Preferences of Infliximab Biosimilar Medications for Inflammatory Bowel Disease'
        assert item.investigator == 'WALJEE,AKBAR, MD'
        assert item.manager == 'ARASIM,MARIA E'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 1) == '01/20'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 2) == '12/25'
        assert item.frum == '2001'
        assert item.thru == '2512'
        assert self.presenter.model[idx].frum == '2001'
        assert self.presenter.model[idx].thru == '2512'
        assert self.presenter.view.get_button_label() == 'Update Project'

        # Check the details form
        assert self.presenter.view.get_name() == 'Biosimilar Merit_Waljee'
        assert self.presenter.view.get_full_name() == 'Effectiveness, Safety, and Patient Preferences of Infliximab Biosimilar Medications for Inflammatory Bowel Disease'
        assert self.presenter.view.frum_ctrl.GetValue() == '01/20'
        assert self.presenter.view.thru_ctrl.GetValue() == '12/25'
        assert self.presenter.view.get_frum() == '2001'
        assert self.presenter.view.get_thru() == '2512'
        assert self.presenter.view.pi_ctrl.GetCount() == 27
        assert self.presenter.view.pm_ctrl.GetCount() == 130
        assert self.presenter.view.get_pi().name == 'WALJEE,AKBAR, MD'
        assert self.presenter.view.pi_ctrl.get_selection_id() == 67
        assert self.presenter.view.get_pm().name == 'ARASIM,MARIA E'
        assert self.presenter.view.pm_ctrl.get_selection_id() == 80

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 5
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 5
        assert ass_items[idx].employee == 'ARASIM,MARIA E'
        assert ass_items[idx].employee_id == 80
        assert self.presenter.model[idx].asns[0].frum == '2001'
        assert self.presenter.model[idx].asns[0].thru == '2009'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 1) == '01/20'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 2) == '09/20'

    def testPrjNotesFilter(self):
        self.presenter.apply_filter('notes_fltr_ctrl', 'l', 'pau')
        assert self.presenter.view.list_ctrl.GetItemCount() == 1
        obj = self.presenter.view.list_ctrl.GetFilteredObjects()[0]
        assert obj.id == 285
        idx = self.presenter.view.get_selected_idx()
        assert idx == 0

        item = self.presenter.view.get_selection()
        assert item.id == 285
        assert item.name == 'UM SPIRIT (Pfeiffer)'
        assert item.full_name == 'UM Integrated Versus Referral Care for Complex Psychiatric Disorders'
        assert item.investigator == 'PFEIFFER,PAUL, MD'
        assert item.manager == None
        assert self.presenter.view.list_ctrl.GetItemText(idx, 1) == '01/19'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 2) == '12/20'
        assert item.frum == '1901'
        assert item.thru == '2012'
        assert self.presenter.view.get_button_label() == 'Update Project'

        # Check the details form
        assert self.presenter.view.get_name() == 'UM SPIRIT (Pfeiffer)'
        assert self.presenter.view.get_full_name() == 'UM Integrated Versus Referral Care for Complex Psychiatric Disorders'
        assert self.presenter.view.frum_ctrl.GetValue() == '01/19'
        assert self.presenter.view.thru_ctrl.GetValue() == '12/20'
        assert self.presenter.view.get_frum() == '1901'
        assert self.presenter.view.get_thru() == '2012'
        assert self.presenter.view.pi_ctrl.GetCount() == 27
        assert self.presenter.view.pm_ctrl.GetCount() == 130
        assert self.presenter.view.get_pi().name == 'PFEIFFER,PAUL, MD'
        assert self.presenter.view.pi_ctrl.get_selection_id() == 75
        assert self.presenter.view.get_pm() == None
        assert self.presenter.view.pm_ctrl.get_selection_id() == None

        # Check the assignments list
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 1
        assert ass_items[0].employee == 'TAKAMINE,LINDA'
        assert ass_items[0].employee_id == 248
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 1) == '01/19'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 2) == '12/20'

    def testCancelNotesFilter(self):
        evt = wx.CommandEvent(wx.EVT_SEARCHCTRL_CANCEL_BTN.typeId)
        obj = self.presenter.view.notes_fltr_ctrl
        evt.SetEventObject(obj)
        evt.SetId(obj.GetId())
        obj.GetEventHandler().ProcessEvent(evt)

        idx = self.presenter.view.get_selected_idx()
        list_items = self.presenter.view.list_ctrl.GetObjects()
        assert len(list_items) == 31
        item = list_items[idx]
        assert item.id == 303
        assert item.name == 'Biosimilar Merit_Waljee'
        assert item.full_name == 'Effectiveness, Safety, and Patient Preferences of Infliximab Biosimilar Medications for Inflammatory Bowel Disease'
        assert item.investigator == 'WALJEE,AKBAR, MD'
        assert item.manager == 'ARASIM,MARIA E'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 1) == '01/20'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 2) == '12/25'
        assert item.frum == '2001'
        assert item.thru == '2512'
        assert self.presenter.model[idx].frum == '2001'
        assert self.presenter.model[idx].thru == '2512'
        assert self.presenter.view.get_button_label() == 'Update Project'

        # Check the details form
        assert self.presenter.view.get_name() == 'Biosimilar Merit_Waljee'
        assert self.presenter.view.get_full_name() == 'Effectiveness, Safety, and Patient Preferences of Infliximab Biosimilar Medications for Inflammatory Bowel Disease'
        assert self.presenter.view.frum_ctrl.GetValue() == '01/20'
        assert self.presenter.view.thru_ctrl.GetValue() == '12/25'
        assert self.presenter.view.get_frum() == '2001'
        assert self.presenter.view.get_thru() == '2512'
        assert self.presenter.view.pi_ctrl.GetCount() == 27
        assert self.presenter.view.pm_ctrl.GetCount() == 130
        assert self.presenter.view.get_pi().name == 'WALJEE,AKBAR, MD'
        assert self.presenter.view.pi_ctrl.get_selection_id() == 67
        assert self.presenter.view.get_pm().name == 'ARASIM,MARIA E'
        assert self.presenter.view.pm_ctrl.get_selection_id() == 80

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 5
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 5
        assert ass_items[idx].employee == 'ARASIM,MARIA E'
        assert ass_items[idx].employee_id == 80
        assert self.presenter.model[idx].asns[0].frum == '2001'
        assert self.presenter.model[idx].asns[0].thru == '2009'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 1) == '01/20'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 2) == '09/20'

    def testClearForm(self):
        evt = wx.CommandEvent(wx.EVT_BUTTON.typeId)
        obj = self.presenter.view.clear_btn
        evt.SetEventObject(obj)
        evt.SetId(obj.GetId())
        obj.GetEventHandler().ProcessEvent(evt)

        assert self.presenter.view.get_selected_idx() == -1
        assert self.presenter.view.get_name() == ''
        assert self.presenter.view.get_full_name() == ''
        assert self.presenter.view.get_frum() == ''
        assert self.presenter.view.get_thru() == ''
        assert self.presenter.view.get_pi() == None
        assert self.presenter.view.pi_ctrl.CurrentSelection == 0
        assert self.presenter.view.get_pm() == None
        assert self.presenter.view.pm_ctrl.CurrentSelection == 0
        assert self.presenter.view.get_notes() == ''
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 0
        assert self.presenter.view.get_button_label() == 'Add Project'

    def testButtonLabelChange(self):
        assert self.presenter.view.get_button_label() == 'Update Project'
        self.presenter.clear()
        assert self.presenter.view.get_button_label() == 'Add Project'
        self.presenter.set_selection(1)
        assert self.presenter.view.get_button_label() == 'Update Project'

    def testValidateProjectFormOnAdd(self):
        self.presenter.clear()

        # No project name entered
        err_msg = self.presenter.validate()
        assert err_msg == 'Project name required!'

        # Duplicate project name
        self.presenter.view.set_name('CFIR V2 LIP')
        err_msg = self.presenter.validate()
        assert err_msg == 'Project name not unique!'

        self.presenter.view.set_name('Test Prj 1')

        # No full name entered
        err_msg = self.presenter.validate()
        assert err_msg == 'Project full name required!'

        # Duplicate full name
        self.presenter.view.set_full_name('Morphomics (Su)')
        err_msg = self.presenter.validate()
        assert err_msg == 'Project full name not unique!'

        self.presenter.view.set_full_name('Test Project One')

        # No frum date
        err_msg = self.presenter.validate()
        assert err_msg == 'From date invalid!'

        # Bogus from dates (UI always gets 4 digits)
        self.presenter.view.set_frum('0000')       # month 00
        err_msg = self.presenter.validate()
        assert err_msg == 'From date invalid!'

        self.presenter.view.set_frum('0013')       # month 13
        err_msg = self.presenter.validate()
        assert err_msg == 'From date invalid!'

        self.presenter.view.set_frum('2001')

        # Bogus thru dates (UI always gets 4 digits)
        self.presenter.view.set_thru('0000')       # month 00
        err_msg = self.presenter.validate()
        assert err_msg == 'Thru date invalid!'

        self.presenter.view.set_thru('0013')       # month 13
        err_msg = self.presenter.validate()
        assert err_msg == 'Thru date invalid!'

        # Frum date later than thru date
        self.presenter.view.set_thru('1912')
        err_msg = self.presenter.validate()
        assert err_msg == 'From date must precede thru date!'

        self.presenter.view.set_thru('2001')   # 1 month project
        err_msg = self.presenter.validate()
        assert err_msg == None

    def testValidateProjectFormOnUpdate(self):
        self.presenter.set_selection(1)
        assert self.presenter.view.get_name() == 'CFIR V2 LIP'

        # No project name entered
        self.presenter.view.set_name('')
        err_msg = self.presenter.validate()
        assert err_msg == 'Project name required!'

        # Can't steal name from another project
        self.presenter.view.set_name('LIP 20-121 (Saint)')
        err_msg = self.presenter.validate()
        assert err_msg == 'Project name not unique!'

        # Duplicate project name OK since it's the same project
        self.presenter.view.set_name('CFIR V2 LIP')
        err_msg = self.presenter.validate()
        assert err_msg == None

        # Can rename the project with a unique name
        self.presenter.view.set_name('Test Prj 1')
        err_msg = self.presenter.validate()
        assert err_msg == None

        # No project full name entered
        self.presenter.view.set_full_name('')
        err_msg = self.presenter.validate()
        assert err_msg == 'Project full name required!'

        # Can't steal full name from another project
        self.presenter.view.set_full_name('Morphomics (Su)')
        err_msg = self.presenter.validate()
        assert err_msg == 'Project full name not unique!'

        # Duplicate project frull name OK since it's the same project
        self.presenter.view.set_full_name('Updating the Consolidated Framework for Implementation Research (CFIR V2)')
        err_msg = self.presenter.validate()
        assert err_msg == None

        # Can rename the project with a unique name
        self.presenter.view.set_full_name('Test Project One')
        err_msg = self.presenter.validate()
        assert err_msg == None

        # No frum date
        self.presenter.view.set_frum('0000')
        err_msg = self.presenter.validate()
        assert err_msg == 'From date invalid!'

        self.presenter.view.set_frum('0013')       # month 13
        err_msg = self.presenter.validate()
        assert err_msg == 'From date invalid!'

        self.presenter.view.set_frum('2001')

        # Bogus thru dates (UI always gets 4 digits)
        self.presenter.view.set_thru('0000')       # month 00
        err_msg = self.presenter.validate()
        assert err_msg == 'Thru date invalid!'

        self.presenter.view.set_thru('0013')       # month 13
        err_msg = self.presenter.validate()
        assert err_msg == 'Thru date invalid!'

        # Frum date later than thru date
        self.presenter.view.set_thru('1912')
        err_msg = self.presenter.validate()
        assert err_msg == 'From date must precede thru date!'

        self.presenter.view.set_thru('2001')   # 1 month project
        err_msg = self.presenter.validate()
        assert err_msg == None

    # This test has all valid data. See above invalid tests
    def testAddUpdatesModelAndView(self):
        self.presenter.clear()
        self.presenter.view.set_name('Test Prj 5')
        self.presenter.view.set_full_name('Test Project Five')
        self.presenter.view.set_frum('1911')
        self.presenter.view.set_thru('2004')
        self.presenter.view.set_pi('KERR,EVE,MD')
        self.presenter.view.set_pm('GILLON,LEAH R')
        self.presenter.view.set_notes('This is a comment.')

        self.presenter.save()

        list_items = self.presenter.view.list_ctrl.GetObjects()
        assert len(list_items) == 32
        idx = self.presenter.view.get_selected_idx()
        item = list_items[idx]
        # assert item.id == 303
        assert item.name == 'Test Prj 5'
        assert item.full_name == 'Test Project Five'
        assert item.investigator == 'KERR,EVE,MD'
        assert item.manager == 'GILLON,LEAH R'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 1) == '11/19'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 2) == '04/20'
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

        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 0

    # This test has all valid data. See above invalid tests
    def testUpdateUpdatesModelAndView(self):
        idx = 6
        self.presenter.set_selection(idx)
        item = self.presenter.view.get_selection()
        assert item.id == 279
        assert item.name == 'LIP 19-111 (Prescott)'
        assert item.full_name == 'LIP 19-111 Prescott'
        assert item.investigator == None
        assert item.manager == 'LUGINBILL,KAITLYN A'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 1) == '04/19'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 2) == '09/19'
        assert item.frum == '1904'
        assert item.thru == '1909'
        assert self.presenter.model[idx].frum == '1904'
        assert self.presenter.model[idx].thru == '1909'
        assert self.presenter.view.get_button_label() == 'Update Project'

        # Check the details form
        assert self.presenter.view.get_name() == 'LIP 19-111 (Prescott)'
        assert self.presenter.view.get_full_name() == 'LIP 19-111 Prescott'
        assert self.presenter.view.frum_ctrl.GetValue() == '04/19'
        assert self.presenter.view.thru_ctrl.GetValue() == '09/19'
        assert self.presenter.view.get_frum() == '1904'
        assert self.presenter.view.get_thru() == '1909'
        assert self.presenter.view.pi_ctrl.GetCount() == 27
        assert self.presenter.view.pm_ctrl.GetCount() == 130
        assert self.presenter.view.get_pi() == None
        assert self.presenter.view.pi_ctrl.get_selection_id() == None
        assert self.presenter.view.get_pm().name == 'LUGINBILL,KAITLYN A'
        assert self.presenter.view.pm_ctrl.get_selection_id() == 120

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 1
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 1
        assert ass_items[0].employee == 'SEEYLE,SARAH'
        assert ass_items[0].employee_id == 278
        assert self.presenter.model[idx].asns[0].frum == '1904'
        assert self.presenter.model[idx].asns[0].thru == '1909'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 1) == '04/19'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 2) == '09/19'

        self.presenter.view.set_name('Test Prj 5')
        self.presenter.view.set_full_name('Test Project Five')
        self.presenter.view.set_frum('1905')
        self.presenter.view.set_thru('1908')
        self.presenter.view.set_pi('KERR,EVE,MD')
        self.presenter.view.set_pm('GILLON,LEAH R')
        self.presenter.view.set_notes('This is a comment.')

        self.presenter.save()

        list_items = self.presenter.view.list_ctrl.GetObjects()
        assert len(list_items) == 31
        idx = self.presenter.view.get_selected_idx()
        assert idx == 6
        item = list_items[idx]
        assert item.id == 279
        assert item.name == 'Test Prj 5'
        assert item.full_name == 'Test Project Five'
        assert item.investigator == 'KERR,EVE,MD'
        assert item.manager == 'GILLON,LEAH R'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 1) == '05/19'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 2) == '08/19'
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
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 1
        assert ass_items[0].employee == 'SEEYLE,SARAH'
        assert ass_items[0].employee_id == 278
        assert self.presenter.model[idx].asns[0].frum == '1904'
        assert self.presenter.model[idx].asns[0].thru == '1909'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 1) == '04/19'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 2) == '09/19'

    def testDropUpdatesModelAndView(self):
        idx = 6
        self.presenter.set_selection(idx)
        item = self.presenter.view.get_selection()
        assert item.id == 279
        assert item.name == 'LIP 19-111 (Prescott)'
        assert item.full_name == 'LIP 19-111 Prescott'
        assert item.investigator == None
        assert item.manager == 'LUGINBILL,KAITLYN A'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 1) == '04/19'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 2) == '09/19'
        assert item.frum == '1904'
        assert item.thru == '1909'
        assert self.presenter.model[idx].frum == '1904'
        assert self.presenter.model[idx].thru == '1909'
        assert self.presenter.view.get_button_label() == 'Update Project'

        # Check the details form
        assert self.presenter.view.get_name() == 'LIP 19-111 (Prescott)'
        assert self.presenter.view.get_full_name() == 'LIP 19-111 Prescott'
        assert self.presenter.view.frum_ctrl.GetValue() == '04/19'
        assert self.presenter.view.thru_ctrl.GetValue() == '09/19'
        assert self.presenter.view.get_frum() == '1904'
        assert self.presenter.view.get_thru() == '1909'
        assert self.presenter.view.pi_ctrl.GetCount() == 27
        assert self.presenter.view.pm_ctrl.GetCount() == 130
        assert self.presenter.view.get_pi() == None
        assert self.presenter.view.pi_ctrl.get_selection_id() == None
        assert self.presenter.view.get_pm().name == 'LUGINBILL,KAITLYN A'
        assert self.presenter.view.pm_ctrl.get_selection_id() == 120

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 1
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 1
        assert ass_items[0].employee == 'SEEYLE,SARAH'
        assert ass_items[0].employee_id == 278
        assert self.presenter.model[idx].asns[0].frum == '1904'
        assert self.presenter.model[idx].asns[0].thru == '1909'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 1) == '04/19'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 2) == '09/19'

        self.presenter.drop()

        idx = self.presenter.view.get_selected_idx()
        item = self.presenter.view.get_selection()
        assert item.id == 280
        assert item.name == 'LIP 19-112 (Kullgren-DeWitt) Visceral MDM'
        assert item.full_name == 'LIP 19-112 Understanding the Influence of Patient and Provider Visceral Factors on Clinical Decision-Making (Kullgren-DeWitt)'
        assert item.investigator == None
        assert item.manager == 'DEWITT,JEFFREY,POSTDOC'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 1) == '03/19'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 2) == '09/20'
        assert item.frum == '1903'
        assert item.thru == '2009'
        assert self.presenter.model[idx].frum == '1903'
        assert self.presenter.model[idx].thru == '2009'
        assert self.presenter.view.get_button_label() == 'Update Project'

        # Check the details form
        assert self.presenter.view.get_name() == 'LIP 19-112 (Kullgren-DeWitt) Visceral MDM'
        assert self.presenter.view.get_full_name() == 'LIP 19-112 Understanding the Influence of Patient and Provider Visceral Factors on Clinical Decision-Making (Kullgren-DeWitt)'
        assert self.presenter.view.frum_ctrl.GetValue() == '03/19'
        assert self.presenter.view.thru_ctrl.GetValue() == '09/20'
        assert self.presenter.view.get_frum() == '1903'
        assert self.presenter.view.get_thru() == '2009'
        assert self.presenter.view.pi_ctrl.GetCount() == 27
        assert self.presenter.view.pm_ctrl.GetCount() == 130
        assert self.presenter.view.get_pi() == None
        assert self.presenter.view.pi_ctrl.get_selection_id() == None
        assert self.presenter.view.get_pm().name == 'DEWITT,JEFFREY,POSTDOC'
        assert self.presenter.view.pm_ctrl.get_selection_id() == 284

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 5
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 5
        assert ass_items[0].employee == 'DEWITT,JEFFREY,POSTDOC'
        assert ass_items[0].employee_id == 284
        assert self.presenter.model[idx].asns[0].frum == '1903'
        assert self.presenter.model[idx].asns[0].thru == '1909'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 1) == '03/19'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 2) == '09/19'

    def testDropLastRecUpdatesModelAndView(self):
        idx = 30
        self.presenter.set_selection(idx)
        item = self.presenter.view.get_selection()
        assert item.id == 300
        assert item.name == 'VERAM CHRT (Adams)'
        assert item.full_name == 'VERAM Assessing the Capacity of Community-based Providers to Care for Older Veterans (Adams)'
        assert item.investigator == None
        assert item.manager == 'SAFFAR,DARCY A'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 1) == '04/19'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 2) == '09/19'
        assert item.frum == '1904'
        assert item.thru == '1909'
        assert self.presenter.model[idx].frum == '1904'
        assert self.presenter.model[idx].thru == '1909'
        assert self.presenter.view.get_button_label() == 'Update Project'

        # Check the details form
        assert self.presenter.view.get_name() == 'VERAM CHRT (Adams)'
        assert self.presenter.view.get_full_name() == 'VERAM Assessing the Capacity of Community-based Providers to Care for Older Veterans (Adams)'
        assert self.presenter.view.frum_ctrl.GetValue() == '04/19'
        assert self.presenter.view.thru_ctrl.GetValue() == '09/19'
        assert self.presenter.view.get_frum() == '1904'
        assert self.presenter.view.get_thru() == '1909'
        assert self.presenter.view.pi_ctrl.GetCount() == 27
        assert self.presenter.view.pm_ctrl.GetCount() == 130
        assert self.presenter.view.get_pi() == None
        assert self.presenter.view.pi_ctrl.get_selection_id() == None
        assert self.presenter.view.get_pm().name == 'SAFFAR,DARCY A'
        assert self.presenter.view.pm_ctrl.get_selection_id() == 22

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 5
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 5
        assert ass_items[0].employee == 'SAFFAR,DARCY A'
        assert ass_items[0].employee_id == 22
        assert self.presenter.model[idx].asns[0].frum == '1904'
        assert self.presenter.model[idx].asns[0].thru == '1904'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 1) == '04/19'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 2) == '04/19'

        self.presenter.drop()

        idx = self.presenter.view.get_selected_idx()
        item = self.presenter.view.get_selection()
        assert item.id == 310
        assert item.name == 'UM_RO1 (Ilgen & LIn)'
        assert item.full_name == 'Enhancing the impact of behavioral pain management on MAT outcomes (Ilgen & Lin)'
        assert item.investigator == 'ILGEN,MARK PHD'
        assert item.manager == 'LEWIS (STINCHOMB),MANDY'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 1) == '09/19'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 2) == '08/23'
        assert item.frum == '1909'
        assert item.thru == '2308'
        assert self.presenter.model[idx].frum == '1909'
        assert self.presenter.model[idx].thru == '2308'
        assert self.presenter.view.get_button_label() == 'Update Project'

        # Check the details form
        assert self.presenter.view.get_name() == 'UM_RO1 (Ilgen & LIn)'
        assert self.presenter.view.get_full_name() == 'Enhancing the impact of behavioral pain management on MAT outcomes (Ilgen & Lin)'
        assert self.presenter.view.frum_ctrl.GetValue() == '09/19'
        assert self.presenter.view.thru_ctrl.GetValue() == '08/23'
        assert self.presenter.view.get_frum() == '1909'
        assert self.presenter.view.get_thru() == '2308'
        assert self.presenter.view.pi_ctrl.GetCount() == 27
        assert self.presenter.view.pm_ctrl.GetCount() == 130
        assert self.presenter.view.get_pi().name == 'ILGEN,MARK PHD'
        assert self.presenter.view.pi_ctrl.get_selection_id() == 73
        assert self.presenter.view.get_pm().name == 'LEWIS (STINCHOMB),MANDY'
        assert self.presenter.view.pm_ctrl.get_selection_id() == 250

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 1
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 1
        assert ass_items[0].employee == 'LEWIS (STINCHOMB),MANDY'
        assert ass_items[0].employee_id == 250
        assert self.presenter.model[idx].asns[0].frum == '1910'
        assert self.presenter.model[idx].asns[0].thru == '2009'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 1) == '10/19'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 2) == '09/20'
