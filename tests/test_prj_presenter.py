import unittest
from unittest.mock import patch
from tests.helpers import *
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

    def get_vars(self):
        return self.presenter.view, self.presenter.model, self.presenter.view.list_ctrl, self.presenter.view.asn_list_ctrl

    def testViewLoadedPIAndPM(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        model_idx = 0

        # No list click made

        # Check the project list
        list_items = list_ctrl.GetObjects()
        assert len(list_items) == 31
        item = list_items[model_idx]
        assert item.id == 303
        assert item.name == 'Biosimilar Merit_Waljee'
        assert item.full_name == 'Effectiveness, Safety, and Patient Preferences of Infliximab Biosimilar Medications for Inflammatory Bowel Disease'
        assert item.investigator == 'WALJEE,AKBAR, MD'
        assert item.manager == 'ARASIM,MARIA E'
        assert list_ctrl.GetItemText(model_idx, 1) == '01/20'
        assert list_ctrl.GetItemText(model_idx, 2) == '12/25'
        assert item.frum == '2001'
        assert item.thru == '2512'
        assert model[model_idx].frum == '2001'
        assert model[model_idx].thru == '2512'

        # Check the details form
        assert view.get_name() == 'Biosimilar Merit_Waljee'
        assert view.get_full_name() == 'Effectiveness, Safety, and Patient Preferences of Infliximab Biosimilar Medications for Inflammatory Bowel Disease'
        assert view.frum_ctrl.GetValue() == '01/20'
        assert view.thru_ctrl.GetValue() == '12/25'
        assert view.get_frum() == '2001'
        assert view.get_thru() == '2512'
        assert view.pi_ctrl.GetCount() == 29
        assert view.pm_ctrl.GetCount() == 128
        assert view.get_pi().name == 'WALJEE,AKBAR, MD'
        assert view.pi_ctrl.get_selection_id() == 67
        assert view.get_pm().name == 'ARASIM,MARIA E'
        assert view.pm_ctrl.get_selection_id() == 80
        assert view.get_button_label() == 'Update Project'

        # Check the assignments list
        assert len(model[model_idx].asns) == 5
        asn_idx = 0
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 5
        asn_ids = [2320, 2321, 2322, 2323, 2324]
        assert [asn.id for asn in asn_items] == asn_ids
        assert [asn.id for asn in model[model_idx].asns] == asn_ids
        assert asn_items[asn_idx].employee == 'ARASIM,MARIA E'
        assert asn_items[asn_idx].employee_id == 80
        assert model[model_idx].asns[asn_idx].frum == '2001'
        assert model[model_idx].asns[asn_idx].thru == '2009'
        assert asn_list_ctrl.GetItemText(0, 1) == '01/20'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/20'

    def testPrjListSelectPIAndPM(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        model_idx = 1
        click_list_ctrl(list_ctrl, model_idx)
        item = view.get_selection()
        assert item.id == 313
        assert item.name == 'CFIR V2 LIP'
        assert item.full_name == 'Updating the Consolidated Framework for Implementation Research (CFIR V2)'
        assert item.investigator == 'DAMSCHRODER,LAURA J'
        assert item.manager == 'REARDON,CAITLIN M'
        assert list_ctrl.GetItemText(model_idx, 1) == '10/19'
        assert list_ctrl.GetItemText(model_idx, 2) == '09/20'
        assert item.frum == '1910'
        assert item.thru == '2009'
        assert model[model_idx].frum == '1910'
        assert model[model_idx].thru == '2009'
        assert view.get_button_label() == 'Update Project'

        # Check the details form
        assert view.get_name() == 'CFIR V2 LIP'
        assert view.get_full_name() == 'Updating the Consolidated Framework for Implementation Research (CFIR V2)'
        assert view.frum_ctrl.GetValue() == '10/19'
        assert view.thru_ctrl.GetValue() == '09/20'
        assert view.get_frum() == '1910'
        assert view.get_thru() == '2009'
        assert view.pi_ctrl.GetCount() == 29
        assert view.pm_ctrl.GetCount() == 128
        assert view.get_pi().name == 'DAMSCHRODER,LAURA J'
        assert view.pi_ctrl.get_selection_id() == 57
        assert view.get_pm().name == 'REARDON,CAITLIN M'
        assert view.pm_ctrl.get_selection_id() == 31

        # Check the assignments list
        assert len(model[model_idx].asns) == 1
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 1
        assert asn_items[0].employee == 'OPRA,MARILLA'
        assert asn_items[0].employee_id == 302
        assert model[model_idx].asns[0].frum == '1911'
        assert model[model_idx].asns[0].thru == '2009'
        assert asn_list_ctrl.GetItemText(0, 1) == '11/19'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/20'

    def testPrjListSelectNoPI(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        model_idx = 4
        click_list_ctrl(list_ctrl, model_idx)
        item = view.get_selection()
        assert item.id == 293
        assert item.name == 'IIR 17-269 Morphomics (Su)'
        assert item.full_name == 'Morphomics (Su)'
        assert item.investigator == None
        assert item.manager == 'YOULES,BRADLEY W'
        assert list_ctrl.GetItemText(model_idx, 1) == '05/19'
        assert list_ctrl.GetItemText(model_idx, 2) == '09/30'
        assert item.frum == '1905'
        assert item.thru == '3009'
        assert model[model_idx].frum == '1905'
        assert model[model_idx].thru == '3009'
        assert view.get_button_label() == 'Update Project'

        # Check the details form
        assert view.get_name() == 'IIR 17-269 Morphomics (Su)'
        assert view.get_full_name() == 'Morphomics (Su)'
        assert view.frum_ctrl.GetValue() == '05/19'
        assert view.thru_ctrl.GetValue() == '09/30'
        assert view.get_frum() == '1905'
        assert view.get_thru() == '3009'
        assert view.pi_ctrl.GetCount() == 29
        assert view.pm_ctrl.GetCount() == 128
        assert view.get_pi() == None
        assert view.pi_ctrl.get_selection_id() == None
        assert view.get_pm().name == 'YOULES,BRADLEY W'
        assert view.pm_ctrl.get_selection_id() == 86

        # Check the assignments list
        assert len(model[model_idx].asns) == 6
        asn_idx = 0
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 6
        asn_ids = [2196, 2197, 2240, 2296, 2305, 2306]
        assert [asn.id for asn in asn_items] == asn_ids
        assert [asn.id for asn in model[model_idx].asns] == asn_ids
        assert asn_items[asn_idx].employee == 'MYERS,AIMEE'
        assert asn_items[asn_idx].employee_id == 212
        assert model[model_idx].asns[asn_idx].frum == '1905'
        assert model[model_idx].asns[asn_idx].thru == '2009'
        assert asn_list_ctrl.GetItemText(0, 1) == '05/19'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/20'


    def testPrjListSelectNoPM(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        model_idx = 10
        click_list_ctrl(list_ctrl, model_idx)
        item = view.get_selection()
        assert item.id == 308
        assert item.name == 'LIP 20-120 (Sears)'
        assert item.full_name == 'Assessing Utilization and Access in Surgical Episodes Across Differing Healthcare Delivery Settings (Sears)'
        assert item.investigator == 'SEARS,ERICA, MD.'
        assert item.manager == None
        assert list_ctrl.GetItemText(model_idx, 1) == '10/19'
        assert list_ctrl.GetItemText(model_idx, 2) == '09/20'
        assert item.frum == '1910'
        assert item.thru == '2009'
        assert model[model_idx].frum == '1910'
        assert model[model_idx].thru == '2009'
        assert view.get_button_label() == 'Update Project'

        # Check the details form
        assert view.get_name() == 'LIP 20-120 (Sears)'
        assert view.get_full_name() == 'Assessing Utilization and Access in Surgical Episodes Across Differing Healthcare Delivery Settings (Sears)'
        assert view.frum_ctrl.GetValue() == '10/19'
        assert view.thru_ctrl.GetValue() == '09/20'
        assert view.get_frum() == '1910'
        assert view.get_thru() == '2009'
        assert view.pi_ctrl.GetCount() == 29
        assert view.pm_ctrl.GetCount() == 128
        assert view.get_pi().name == 'SEARS,ERICA, MD.'
        assert view.pi_ctrl.get_selection_id() == 279
        assert view.get_pm() == None
        assert view.pm_ctrl.get_selection_id() == None

        # Check the assignments list
        assert len(model[model_idx].asns) == 1
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 1
        assert asn_items[0].employee == 'EVANS,RICHARD'
        assert asn_items[0].employee_id == 256
        assert model[model_idx].asns[0].frum == '1910'
        assert model[model_idx].asns[0].thru == '2009'
        assert asn_list_ctrl.GetItemText(0, 1) == '10/19'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/20'

    def testPrjListSelectNoAsns(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        model_idx = 25
        click_list_ctrl(list_ctrl, model_idx)
        item = view.get_selection()
        assert item.id == 282
        assert item.name == 'UM MTOP (Saini)'
        assert item.full_name == 'UM Michigan Treatment Optimization Program_Evaluation (Saini)'
        assert item.investigator == 'SAINI,SAMEER, MD'
        assert item.manager == 'SAFFAR,DARCY A'
        assert list_ctrl.GetItemText(model_idx, 1) == '01/19'
        assert list_ctrl.GetItemText(model_idx, 2) == '09/19'
        assert item.frum == '1901'
        assert item.thru == '1909'
        assert model[model_idx].frum == '1901'
        assert model[model_idx].thru == '1909'
        assert view.get_button_label() == 'Update Project'

        # Check the details form
        assert view.get_name() == 'UM MTOP (Saini)'
        assert view.get_full_name() == 'UM Michigan Treatment Optimization Program_Evaluation (Saini)'
        assert view.frum_ctrl.GetValue() == '01/19'
        assert view.thru_ctrl.GetValue() == '09/19'
        assert view.get_frum() == '1901'
        assert view.get_thru() == '1909'
        assert view.pi_ctrl.GetCount() == 29
        assert view.pm_ctrl.GetCount() == 128
        assert view.get_pi().name == 'SAINI,SAMEER, MD'
        assert view.pi_ctrl.get_selection_id() == 63
        assert view.get_pm().name == 'SAFFAR,DARCY A'
        assert view.pm_ctrl.get_selection_id() == 22

        # Check the assignments list
        assert len(model[model_idx].asns) == 0
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 0

    def testPrjNameFilter(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        self.presenter.apply_filter('name_fltr_ctrl', 'x', '')
        assert list_ctrl.GetItemCount() == 1
        obj = list_ctrl.GetFilteredObjects()[0]
        assert obj.id == 312
        model_idx = view.get_selected_idx()
        assert model_idx == 0

        item = view.get_selection()
        assert item.id == 312
        assert item.name == 'UM ICU Expansion OPTION 2 (SAINT)'
        assert item.full_name == 'UM Expanding the Comprehensive Unit-based Safety Program (CUSP) to Reduce Central Line-Associated Blood Stream Infections (CLABSI) and Catheter-Associated Urinary Tract Infections (CAUTI) in Intensive Care Units (ICU) with Persistently Elevated Infection Rates - OPTION 1'
        assert item.investigator == None
        assert item.manager == 'FOWLER,KAREN E'
        assert list_ctrl.GetItemText(model_idx, 1) == '09/19'
        assert list_ctrl.GetItemText(model_idx, 2) == '09/21'
        assert item.frum == '1909'
        assert item.thru == '2109'
        assert view.get_button_label() == 'Update Project'

        # Check the details form
        assert view.get_name() == 'UM ICU Expansion OPTION 2 (SAINT)'
        assert view.get_full_name() == 'UM Expanding the Comprehensive Unit-based Safety Program (CUSP) to Reduce Central Line-Associated Blood Stream Infections (CLABSI) and Catheter-Associated Urinary Tract Infections (CAUTI) in Intensive Care Units (ICU) with Persistently Elevated Infection Rates - OPTION 1'
        assert view.frum_ctrl.GetValue() == '09/19'
        assert view.thru_ctrl.GetValue() == '09/21'
        assert view.get_frum() == '1909'
        assert view.get_thru() == '2109'
        assert view.pi_ctrl.GetCount() == 29
        assert view.pm_ctrl.GetCount() == 128
        assert view.get_pi() == None
        assert view.pi_ctrl.get_selection_id() == None
        assert view.get_pm().name == 'FOWLER,KAREN E'
        assert view.pm_ctrl.get_selection_id() == 15

        # Check the assignments list
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 1
        assert asn_items[0].employee == 'FOWLER,KAREN E'
        assert asn_items[0].employee_id == 15
        assert asn_list_ctrl.GetItemText(0, 1) == '10/19'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/20'

    def testCancelPrjNameFilter(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        click_search_ctrl(view.name_fltr_ctrl)

        model_idx = view.get_selected_idx()
        list_items = list_ctrl.GetObjects()
        assert len(list_items) == 31
        item = list_items[model_idx]
        assert item.id == 303
        assert item.name == 'Biosimilar Merit_Waljee'
        assert item.full_name == 'Effectiveness, Safety, and Patient Preferences of Infliximab Biosimilar Medications for Inflammatory Bowel Disease'
        assert item.investigator == 'WALJEE,AKBAR, MD'
        assert item.manager == 'ARASIM,MARIA E'
        assert list_ctrl.GetItemText(model_idx, 1) == '01/20'
        assert list_ctrl.GetItemText(model_idx, 2) == '12/25'
        assert item.frum == '2001'
        assert item.thru == '2512'
        assert model[model_idx].frum == '2001'
        assert model[model_idx].thru == '2512'
        assert view.get_button_label() == 'Update Project'

        # Check the details form
        assert view.get_name() == 'Biosimilar Merit_Waljee'
        assert view.get_full_name() == 'Effectiveness, Safety, and Patient Preferences of Infliximab Biosimilar Medications for Inflammatory Bowel Disease'
        assert view.frum_ctrl.GetValue() == '01/20'
        assert view.thru_ctrl.GetValue() == '12/25'
        assert view.get_frum() == '2001'
        assert view.get_thru() == '2512'
        assert view.pi_ctrl.GetCount() == 29
        assert view.pm_ctrl.GetCount() == 128
        assert view.get_pi().name == 'WALJEE,AKBAR, MD'
        assert view.pi_ctrl.get_selection_id() == 67
        assert view.get_pm().name == 'ARASIM,MARIA E'
        assert view.pm_ctrl.get_selection_id() == 80

        # Check the assignments list
        assert len(model[model_idx].asns) == 5
        asn_idx = 0
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 5
        asn_ids = [2320, 2321, 2322, 2323, 2324]
        assert [asn.id for asn in asn_items] == asn_ids
        assert [asn.id for asn in model[model_idx].asns] == asn_ids
        assert asn_items[asn_idx].employee == 'ARASIM,MARIA E'
        assert asn_items[asn_idx].employee_id == 80
        assert model[model_idx].asns[asn_idx].frum == '2001'
        assert model[model_idx].asns[asn_idx].thru == '2009'
        assert asn_list_ctrl.GetItemText(0, 1) == '01/20'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/20'

    def testPrjNotesFilter(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        self.presenter.apply_filter('notes_fltr_ctrl', 'l', 'pau')
        assert list_ctrl.GetItemCount() == 1
        obj = list_ctrl.GetFilteredObjects()[0]
        assert obj.id == 285
        model_idx = view.get_selected_idx()
        assert model_idx == 0

        item = view.get_selection()
        assert item.id == 285
        assert item.name == 'UM SPIRIT (Pfeiffer)'
        assert item.full_name == 'UM Integrated Versus Referral Care for Complex Psychiatric Disorders'
        assert item.investigator == 'PFEIFFER,PAUL, MD'
        assert item.manager == None
        assert list_ctrl.GetItemText(model_idx, 1) == '01/19'
        assert list_ctrl.GetItemText(model_idx, 2) == '12/20'
        assert item.frum == '1901'
        assert item.thru == '2012'
        assert view.get_button_label() == 'Update Project'

        # Check the details form
        assert view.get_name() == 'UM SPIRIT (Pfeiffer)'
        assert view.get_full_name() == 'UM Integrated Versus Referral Care for Complex Psychiatric Disorders'
        assert view.frum_ctrl.GetValue() == '01/19'
        assert view.thru_ctrl.GetValue() == '12/20'
        assert view.get_frum() == '1901'
        assert view.get_thru() == '2012'
        assert view.pi_ctrl.GetCount() == 29
        assert view.pm_ctrl.GetCount() == 128
        assert view.get_pi().name == 'PFEIFFER,PAUL, MD'
        assert view.pi_ctrl.get_selection_id() == 75
        assert view.get_pm() == None
        assert view.pm_ctrl.get_selection_id() == None

        # Check the assignments list
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 1
        assert asn_items[0].employee == 'TAKAMINE,LINDA'
        assert asn_items[0].employee_id == 248
        assert asn_list_ctrl.GetItemText(0, 1) == '01/19'
        assert asn_list_ctrl.GetItemText(0, 2) == '12/20'

    def testCancelNotesFilter(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        click_search_ctrl(view.notes_fltr_ctrl)

        model_idx = view.get_selected_idx()
        list_items = list_ctrl.GetObjects()
        assert len(list_items) == 31
        item = list_items[model_idx]
        assert item.id == 303
        assert item.name == 'Biosimilar Merit_Waljee'
        assert item.full_name == 'Effectiveness, Safety, and Patient Preferences of Infliximab Biosimilar Medications for Inflammatory Bowel Disease'
        assert item.investigator == 'WALJEE,AKBAR, MD'
        assert item.manager == 'ARASIM,MARIA E'
        assert list_ctrl.GetItemText(model_idx, 1) == '01/20'
        assert list_ctrl.GetItemText(model_idx, 2) == '12/25'
        assert item.frum == '2001'
        assert item.thru == '2512'
        assert model[model_idx].frum == '2001'
        assert model[model_idx].thru == '2512'
        assert view.get_button_label() == 'Update Project'

        # Check the details form
        assert view.get_name() == 'Biosimilar Merit_Waljee'
        assert view.get_full_name() == 'Effectiveness, Safety, and Patient Preferences of Infliximab Biosimilar Medications for Inflammatory Bowel Disease'
        assert view.frum_ctrl.GetValue() == '01/20'
        assert view.thru_ctrl.GetValue() == '12/25'
        assert view.get_frum() == '2001'
        assert view.get_thru() == '2512'
        assert view.pi_ctrl.GetCount() == 29
        assert view.pm_ctrl.GetCount() == 128
        assert view.get_pi().name == 'WALJEE,AKBAR, MD'
        assert view.pi_ctrl.get_selection_id() == 67
        assert view.get_pm().name == 'ARASIM,MARIA E'
        assert view.pm_ctrl.get_selection_id() == 80

        # Check the assignments list
        assert len(model[model_idx].asns) == 5
        asn_idx = 0
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 5
        asn_ids = [2320, 2321, 2322, 2323, 2324]
        assert [asn.id for asn in asn_items] == asn_ids
        assert [asn.id for asn in model[model_idx].asns] == asn_ids
        assert asn_items[asn_idx].employee == 'ARASIM,MARIA E'
        assert asn_items[asn_idx].employee_id == 80
        assert model[model_idx].asns[asn_idx].frum == '2001'
        assert model[model_idx].asns[asn_idx].thru == '2009'
        assert asn_list_ctrl.GetItemText(0, 1) == '01/20'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/20'

    def testClearForm(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        click_button(view.clear_btn)

        assert view.get_selected_idx() == -1
        assert view.get_name() == ''
        assert view.get_full_name() == ''
        assert view.get_frum() == ''
        assert view.get_thru() == ''
        assert view.get_pi() == None
        assert view.pi_ctrl.CurrentSelection == 0
        assert view.get_pm() == None
        assert view.pm_ctrl.CurrentSelection == 0
        assert view.get_notes() == ''
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 0
        assert view.get_button_label() == 'Add Project'

    def testButtonLabelChange(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        assert view.get_button_label() == 'Update Project'
        click_button(view.clear_btn)
        assert view.get_button_label() == 'Add Project'
        click_list_ctrl(list_ctrl, 1)
        assert view.get_button_label() == 'Update Project'

    def testValidateProjectFormOnAdd(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        click_button(view.clear_btn)

        # No project name entered
        err_msg = self.presenter.validate()
        assert err_msg == 'Project name required!'

        # Duplicate project name
        view.set_name('CFIR V2 LIP')
        err_msg = self.presenter.validate()
        assert err_msg == 'Project name not unique!'

        view.set_name('Test Prj 1')

        # No full name entered
        err_msg = self.presenter.validate()
        assert err_msg == 'Project full name required!'

        # Duplicate full name
        view.set_full_name('Morphomics (Su)')
        err_msg = self.presenter.validate()
        assert err_msg == 'Project full name not unique!'

        view.set_full_name('Test Project One')

        # No frum date
        err_msg = self.presenter.validate()
        assert err_msg == 'From date invalid!'

        # Bogus from dates (UI always gets 4 digits)
        view.set_frum('0000')       # month 00
        err_msg = self.presenter.validate()
        assert err_msg == 'From date invalid!'

        view.set_frum('0013')       # month 13
        err_msg = self.presenter.validate()
        assert err_msg == 'From date invalid!'

        view.set_frum('2001')

        # Bogus thru dates (UI always gets 4 digits)
        view.set_thru('0000')       # month 00
        err_msg = self.presenter.validate()
        assert err_msg == 'Thru date invalid!'

        view.set_thru('0013')       # month 13
        err_msg = self.presenter.validate()
        assert err_msg == 'Thru date invalid!'

        # Frum date later than thru date
        view.set_thru('1912')
        err_msg = self.presenter.validate()
        assert err_msg == 'From date must precede thru date!'

        view.set_thru('2001')   # 1 month project
        err_msg = self.presenter.validate()
        assert err_msg == None

    def testValidateProjectFormOnUpdate(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        click_list_ctrl(list_ctrl, 1)
        assert view.get_name() == 'CFIR V2 LIP'

        # No project name entered
        view.set_name('')
        err_msg = self.presenter.validate()
        assert err_msg == 'Project name required!'

        # Can't steal name from another project
        view.set_name('LIP 20-121 (Saint)')
        err_msg = self.presenter.validate()
        assert err_msg == 'Project name not unique!'

        # Duplicate project name OK since it's the same project
        view.set_name('CFIR V2 LIP')
        err_msg = self.presenter.validate()
        assert err_msg == None

        # Can rename the project with a unique name
        view.set_name('Test Prj 1')
        err_msg = self.presenter.validate()
        assert err_msg == None

        # No project full name entered
        view.set_full_name('')
        err_msg = self.presenter.validate()
        assert err_msg == 'Project full name required!'

        # Can't steal full name from another project
        view.set_full_name('Morphomics (Su)')
        err_msg = self.presenter.validate()
        assert err_msg == 'Project full name not unique!'

        # Duplicate project frull name OK since it's the same project
        view.set_full_name('Updating the Consolidated Framework for Implementation Research (CFIR V2)')
        err_msg = self.presenter.validate()
        assert err_msg == None

        # Can rename the project with a unique name
        view.set_full_name('Test Project One')
        err_msg = self.presenter.validate()
        assert err_msg == None

        # No frum date
        view.set_frum('0000')
        err_msg = self.presenter.validate()
        assert err_msg == 'From date invalid!'

        view.set_frum('0013')       # month 13
        err_msg = self.presenter.validate()
        assert err_msg == 'From date invalid!'

        view.set_frum('2001')

        # Bogus thru dates (UI always gets 4 digits)
        view.set_thru('0000')       # month 00
        err_msg = self.presenter.validate()
        assert err_msg == 'Thru date invalid!'

        view.set_thru('0013')       # month 13
        err_msg = self.presenter.validate()
        assert err_msg == 'Thru date invalid!'

        # Frum date later than thru date
        view.set_thru('1912')
        err_msg = self.presenter.validate()
        assert err_msg == 'From date must precede thru date!'

        view.set_thru('2001')   # 1 month project
        err_msg = self.presenter.validate()
        assert err_msg == None

    # This test has all valid data. See above invalid tests
    @patch('presenters.presenter.Dao._Dao__write', return_value=317)
    def testAddUpdatesModelAndView(self, write_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        click_button(view.clear_btn)

        view.set_name('Test Prj 5')
        view.set_full_name('Test Project Five')
        view.set_frum('1911')
        view.set_thru('2004')
        view.set_pi('KERR,EVE,MD')
        view.set_pm('GILLON,LEAH R')
        view.set_notes('This is a comment.')

        click_button(view.save_btn)

        assert write_mock.call_count == 1
        args, kwargs = write_mock.call_args
        assert len(args) == 2
        assert len(kwargs) == 0
        assert args[0] == 'INSERT INTO projects (name,full_name,frum,thru,investigator_id,manager_id,notes,active) VALUES (?,?,?,?,?,?,?,?)'
        assert args[1] == ['Test Prj 5', 'Test Project Five', '1911', '2004', 7, 52, 'This is a comment.', 1]

        list_items = list_ctrl.GetObjects()
        assert len(list_items) == 32
        model_idx = view.get_selected_idx()
        item = list_items[model_idx]
        assert item.id == 317
        assert item.name == 'Test Prj 5'
        assert item.full_name == 'Test Project Five'
        assert item.investigator == 'KERR,EVE,MD'
        assert item.manager == 'GILLON,LEAH R'
        assert list_ctrl.GetItemText(model_idx, 1) == '11/19'
        assert list_ctrl.GetItemText(model_idx, 2) == '04/20'
        assert item.frum == '1911'
        assert item.thru == '2004'

        prj_model = self.presenter.model[model_idx]
        assert prj_model.id == 317
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

        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 0

    # This test has all valid data. See above invalid tests
    @patch('presenters.presenter.Dao._Dao__write', return_value=1)
    def testUpdateUpdatesModelAndView(self, write_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        model_idx = 6
        click_list_ctrl(list_ctrl, model_idx)
        item = view.get_selection()
        assert item.id == 279
        assert item.name == 'LIP 19-111 (Prescott)'
        assert item.full_name == 'LIP 19-111 Prescott'
        assert item.investigator == None
        assert item.manager == 'LUGINBILL,KAITLYN A'
        assert list_ctrl.GetItemText(model_idx, 1) == '04/19'
        assert list_ctrl.GetItemText(model_idx, 2) == '09/19'
        assert item.frum == '1904'
        assert item.thru == '1909'
        assert model[model_idx].frum == '1904'
        assert model[model_idx].thru == '1909'
        assert view.get_button_label() == 'Update Project'

        # Check the details form
        assert view.get_name() == 'LIP 19-111 (Prescott)'
        assert view.get_full_name() == 'LIP 19-111 Prescott'
        assert view.frum_ctrl.GetValue() == '04/19'
        assert view.thru_ctrl.GetValue() == '09/19'
        assert view.get_frum() == '1904'
        assert view.get_thru() == '1909'
        assert view.pi_ctrl.GetCount() == 29
        assert view.pm_ctrl.GetCount() == 128
        assert view.get_pi() == None
        assert view.pi_ctrl.get_selection_id() == None
        assert view.get_pm().name == 'LUGINBILL,KAITLYN A'
        assert view.pm_ctrl.get_selection_id() == 120

        # Check the assignments list
        assert len(model[model_idx].asns) == 1
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 1
        assert asn_items[0].employee == 'SEEYLE,SARAH'
        assert asn_items[0].employee_id == 278
        assert model[model_idx].asns[0].frum == '1904'
        assert model[model_idx].asns[0].thru == '1909'
        assert asn_list_ctrl.GetItemText(0, 1) == '04/19'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/19'

        view.set_name('Test Prj 5')
        view.set_full_name('Test Project Five')
        view.set_frum('1905')
        view.set_thru('1908')
        view.set_pi('KERR,EVE,MD')
        view.set_pm('GILLON,LEAH R')
        view.set_notes('This is a comment.')

        click_button(view.save_btn)

        assert write_mock.call_count == 1
        args, kwargs = write_mock.call_args
        assert len(args) == 2
        assert len(kwargs) ==0
        assert args[0] == 'UPDATE projects SET name=?,full_name=?,frum=?,thru=?,notes=?,investigator_id=?,manager_id=? WHERE id=?;'
        assert args[1] == ['Test Prj 5', 'Test Project Five', '1905', '1908', 'This is a comment.', 7, 52, 279]

        list_items = list_ctrl.GetObjects()
        assert len(list_items) == 31
        model_idx = view.get_selected_idx()
        assert model_idx == 6
        item = list_items[model_idx]
        assert item.id == 279
        assert item.name == 'Test Prj 5'
        assert item.full_name == 'Test Project Five'
        assert item.investigator == 'KERR,EVE,MD'
        assert item.manager == 'GILLON,LEAH R'
        assert list_ctrl.GetItemText(model_idx, 1) == '05/19'
        assert list_ctrl.GetItemText(model_idx, 2) == '08/19'
        assert item.frum == '1905'
        assert item.thru == '1908'

        prj_model = self.presenter.model[model_idx]
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

        assert len(model[model_idx].asns) == 1
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 1
        assert asn_items[0].employee == 'SEEYLE,SARAH'
        assert asn_items[0].employee_id == 278
        assert model[model_idx].asns[0].frum == '1904'
        assert model[model_idx].asns[0].thru == '1909'
        assert asn_list_ctrl.GetItemText(0, 1) == '04/19'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/19'

    # This time update with no name, full name change and no PI or PM
    @patch('presenters.presenter.Dao._Dao__write', return_value=1)
    def testUpdateUpdatesModelAndView2(self, write_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        model_idx = 6
        click_list_ctrl(list_ctrl, model_idx)
        item = view.get_selection()
        assert item.id == 279
        assert item.name == 'LIP 19-111 (Prescott)'
        assert item.full_name == 'LIP 19-111 Prescott'
        assert item.investigator == None
        assert item.manager == 'LUGINBILL,KAITLYN A'
        assert list_ctrl.GetItemText(model_idx, 1) == '04/19'
        assert list_ctrl.GetItemText(model_idx, 2) == '09/19'
        assert item.frum == '1904'
        assert item.thru == '1909'
        assert model[model_idx].frum == '1904'
        assert model[model_idx].thru == '1909'
        assert view.get_button_label() == 'Update Project'

        # Check the details form
        assert view.get_name() == 'LIP 19-111 (Prescott)'
        assert view.get_full_name() == 'LIP 19-111 Prescott'
        assert view.frum_ctrl.GetValue() == '04/19'
        assert view.thru_ctrl.GetValue() == '09/19'
        assert view.get_frum() == '1904'
        assert view.get_thru() == '1909'
        assert view.pi_ctrl.GetCount() == 29
        assert view.pm_ctrl.GetCount() == 128
        assert view.get_pi() == None
        assert view.pi_ctrl.get_selection_id() == None
        assert view.get_pm().name == 'LUGINBILL,KAITLYN A'
        assert view.pm_ctrl.get_selection_id() == 120

        # Check the assignments list
        assert len(model[model_idx].asns) == 1
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 1
        assert asn_items[0].employee == 'SEEYLE,SARAH'
        assert asn_items[0].employee_id == 278
        assert model[model_idx].asns[0].frum == '1904'
        assert model[model_idx].asns[0].thru == '1909'
        assert asn_list_ctrl.GetItemText(0, 1) == '04/19'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/19'

        view.set_frum('1905')
        view.set_thru('1908')
        view.set_pi(None)
        view.set_pm(None)
        view.set_notes('This is a comment.')

        click_button(view.save_btn)

        assert write_mock.call_count == 1
        args, kwargs = write_mock.call_args
        assert len(args) == 2
        assert len(kwargs) ==0
        assert args[0] == 'UPDATE projects SET frum=?,thru=?,notes=?,investigator_id=?,manager_id=? WHERE id=?;'
        assert args[1] == ['1905', '1908', 'This is a comment.', None, None, 279]

        list_items = list_ctrl.GetObjects()
        assert len(list_items) == 31
        model_idx = view.get_selected_idx()
        assert model_idx == 6
        item = list_items[model_idx]
        assert item.id == 279
        assert item.name == 'LIP 19-111 (Prescott)'
        assert item.full_name == 'LIP 19-111 Prescott'
        assert item.investigator == None
        assert item.manager == None
        assert list_ctrl.GetItemText(model_idx, 1) == '05/19'
        assert list_ctrl.GetItemText(model_idx, 2) == '08/19'
        assert item.frum == '1905'
        assert item.thru == '1908'

        prj_model = self.presenter.model[model_idx]
        assert prj_model.id == 279
        assert prj_model.name == 'LIP 19-111 (Prescott)'
        assert prj_model.full_name == 'LIP 19-111 Prescott'
        assert prj_model.frum == '1905'
        assert prj_model.thru == '1908'
        assert prj_model.investigator == None
        assert prj_model.investigator_id == None
        assert prj_model.manager == None
        assert prj_model.manager_id == None
        assert prj_model.notes == 'This is a comment.'
        assert prj_model.active == 1

        assert len(model[model_idx].asns) == 1
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 1
        assert asn_items[0].employee == 'SEEYLE,SARAH'
        assert asn_items[0].employee_id == 278
        assert model[model_idx].asns[0].frum == '1904'
        assert model[model_idx].asns[0].thru == '1909'
        assert asn_list_ctrl.GetItemText(0, 1) == '04/19'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/19'

    @patch('presenters.presenter.uil.confirm', return_value=True)
    @patch('presenters.presenter.Dao._Dao__write', return_value=1)
    def testDropUpdatesModelAndView(self, write_mock, confirm_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        model_idx = 6
        click_list_ctrl(list_ctrl, model_idx)
        item = view.get_selection()
        assert item.id == 279
        assert item.name == 'LIP 19-111 (Prescott)'
        assert item.full_name == 'LIP 19-111 Prescott'
        assert item.investigator == None
        assert item.manager == 'LUGINBILL,KAITLYN A'
        assert list_ctrl.GetItemText(model_idx, 1) == '04/19'
        assert list_ctrl.GetItemText(model_idx, 2) == '09/19'
        assert item.frum == '1904'
        assert item.thru == '1909'
        assert model[model_idx].frum == '1904'
        assert model[model_idx].thru == '1909'
        assert view.get_button_label() == 'Update Project'

        # Check the details form
        assert view.get_name() == 'LIP 19-111 (Prescott)'
        assert view.get_full_name() == 'LIP 19-111 Prescott'
        assert view.frum_ctrl.GetValue() == '04/19'
        assert view.thru_ctrl.GetValue() == '09/19'
        assert view.get_frum() == '1904'
        assert view.get_thru() == '1909'
        assert view.pi_ctrl.GetCount() == 29
        assert view.pm_ctrl.GetCount() == 128
        assert view.get_pi() == None
        assert view.pi_ctrl.get_selection_id() == None
        assert view.get_pm().name == 'LUGINBILL,KAITLYN A'
        assert view.pm_ctrl.get_selection_id() == 120

        # Check the assignments list
        assert len(model[model_idx].asns) == 1
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 1
        assert asn_items[0].employee == 'SEEYLE,SARAH'
        assert asn_items[0].employee_id == 278
        assert model[model_idx].asns[0].frum == '1904'
        assert model[model_idx].asns[0].thru == '1909'
        assert asn_list_ctrl.GetItemText(0, 1) == '04/19'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/19'

        click_button(view.drop_btn)

        assert confirm_mock.call_count == 1
        args, kwargs = confirm_mock.call_args
        assert len(args) == 2
        assert len(kwargs) == 0
        assert args[1] == 'Drop selected project?'

        assert write_mock.call_count == 1
        args, kwargs = write_mock.call_args
        assert len(args) == 2
        assert len(kwargs) ==0
        assert args[0] == 'UPDATE projects SET active=0 WHERE id=?'
        assert args[1] == (279,)

        model_idx = view.get_selected_idx()
        item = view.get_selection()
        assert item.id == 280
        assert item.name == 'LIP 19-112 (Kullgren-DeWitt) Visceral MDM'
        assert item.full_name == 'LIP 19-112 Understanding the Influence of Patient and Provider Visceral Factors on Clinical Decision-Making (Kullgren-DeWitt)'
        assert item.investigator == None
        assert item.manager == 'DEWITT,JEFFREY,POSTDOC'
        assert list_ctrl.GetItemText(model_idx, 1) == '03/19'
        assert list_ctrl.GetItemText(model_idx, 2) == '09/20'
        assert item.frum == '1903'
        assert item.thru == '2009'
        assert model[model_idx].frum == '1903'
        assert model[model_idx].thru == '2009'
        assert view.get_button_label() == 'Update Project'

        # Check the details form
        assert view.get_name() == 'LIP 19-112 (Kullgren-DeWitt) Visceral MDM'
        assert view.get_full_name() == 'LIP 19-112 Understanding the Influence of Patient and Provider Visceral Factors on Clinical Decision-Making (Kullgren-DeWitt)'
        assert view.frum_ctrl.GetValue() == '03/19'
        assert view.thru_ctrl.GetValue() == '09/20'
        assert view.get_frum() == '1903'
        assert view.get_thru() == '2009'
        assert view.pi_ctrl.GetCount() == 29
        assert view.pm_ctrl.GetCount() == 128
        assert view.get_pi() == None
        assert view.pi_ctrl.get_selection_id() == None
        assert view.get_pm().name == 'DEWITT,JEFFREY,POSTDOC'
        assert view.pm_ctrl.get_selection_id() == 284

        # Check the assignments list
        assert len(model[model_idx].asns) == 5
        asn_idx = 0
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 5
        asn_ids = [2055, 2056, 2057, 2058, 2400]
        assert [asn.id for asn in asn_items] == asn_ids
        assert [asn.id for asn in model[model_idx].asns] == asn_ids
        assert asn_items[asn_idx].employee == 'DEWITT,JEFFREY,POSTDOC'
        assert asn_items[asn_idx].employee_id == 284
        assert model[model_idx].asns[asn_idx].frum == '1903'
        assert model[model_idx].asns[asn_idx].thru == '1909'
        assert asn_list_ctrl.GetItemText(0, 1) == '03/19'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/19'

    @patch('presenters.presenter.uil.confirm', return_value=True)
    @patch('presenters.presenter.Dao._Dao__write', return_value=1)
    def testDropLastRecUpdatesModelAndView(self, write_mock, confirm_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        model_idx = 30
        click_list_ctrl(list_ctrl, model_idx)
        item = view.get_selection()
        assert item.id == 300
        assert item.name == 'VERAM CHRT (Adams)'
        assert item.full_name == 'VERAM Assessing the Capacity of Community-based Providers to Care for Older Veterans (Adams)'
        assert item.investigator == None
        assert item.manager == 'SAFFAR,DARCY A'
        assert list_ctrl.GetItemText(model_idx, 1) == '04/19'
        assert list_ctrl.GetItemText(model_idx, 2) == '09/19'
        assert item.frum == '1904'
        assert item.thru == '1909'
        assert model[model_idx].frum == '1904'
        assert model[model_idx].thru == '1909'
        assert view.get_button_label() == 'Update Project'

        # Check the details form
        assert view.get_name() == 'VERAM CHRT (Adams)'
        assert view.get_full_name() == 'VERAM Assessing the Capacity of Community-based Providers to Care for Older Veterans (Adams)'
        assert view.frum_ctrl.GetValue() == '04/19'
        assert view.thru_ctrl.GetValue() == '09/19'
        assert view.get_frum() == '1904'
        assert view.get_thru() == '1909'
        assert view.pi_ctrl.GetCount() == 29
        assert view.pm_ctrl.GetCount() == 128
        assert view.get_pi() == None
        assert view.pi_ctrl.get_selection_id() == None
        assert view.get_pm().name == 'SAFFAR,DARCY A'
        assert view.pm_ctrl.get_selection_id() == 22

        # Check the assignments list
        assert len(model[model_idx].asns) == 5
        asn_idx = 0
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 5
        asn_ids = [2290, 2291, 2292, 2293, 2398]
        assert [asn.id for asn in asn_items] == asn_ids
        assert [asn.id for asn in model[model_idx].asns] == asn_ids
        assert asn_items[asn_idx].employee == 'SAFFAR,DARCY A'
        assert asn_items[asn_idx].employee_id == 22
        assert model[model_idx].asns[asn_idx].frum == '1904'
        assert model[model_idx].asns[asn_idx].thru == '1904'
        assert asn_list_ctrl.GetItemText(0, 1) == '04/19'
        assert asn_list_ctrl.GetItemText(0, 2) == '04/19'

        click_button(view.drop_btn)

        assert confirm_mock.call_count == 1
        args, kwargs = confirm_mock.call_args
        assert len(args) == 2
        assert len(kwargs) == 0
        assert args[1] == 'Drop selected project?'

        assert write_mock.call_count == 1
        args, kwargs = write_mock.call_args
        assert len(args) == 2
        assert len(kwargs) ==0
        assert args[0] == 'UPDATE projects SET active=0 WHERE id=?'
        assert args[1] == (300,)

        model_idx = view.get_selected_idx()
        item = view.get_selection()
        assert item.id == 310
        assert item.name == 'UM_RO1 (Ilgen & LIn)'
        assert item.full_name == 'Enhancing the impact of behavioral pain management on MAT outcomes (Ilgen & Lin)'
        assert item.investigator == 'ILGEN,MARK PHD'
        assert item.manager == 'LEWIS (STINCHOMB),MANDY'
        assert list_ctrl.GetItemText(model_idx, 1) == '09/19'
        assert list_ctrl.GetItemText(model_idx, 2) == '08/23'
        assert item.frum == '1909'
        assert item.thru == '2308'
        assert model[model_idx].frum == '1909'
        assert model[model_idx].thru == '2308'
        assert view.get_button_label() == 'Update Project'

        # Check the details form
        assert view.get_name() == 'UM_RO1 (Ilgen & LIn)'
        assert view.get_full_name() == 'Enhancing the impact of behavioral pain management on MAT outcomes (Ilgen & Lin)'
        assert view.frum_ctrl.GetValue() == '09/19'
        assert view.thru_ctrl.GetValue() == '08/23'
        assert view.get_frum() == '1909'
        assert view.get_thru() == '2308'
        assert view.pi_ctrl.GetCount() == 29
        assert view.pm_ctrl.GetCount() == 128
        assert view.get_pi().name == 'ILGEN,MARK PHD'
        assert view.pi_ctrl.get_selection_id() == 73
        assert view.get_pm().name == 'LEWIS (STINCHOMB),MANDY'
        assert view.pm_ctrl.get_selection_id() == 250

        # Check the assignments list
        assert len(model[model_idx].asns) == 1
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 1
        assert asn_items[0].employee == 'LEWIS (STINCHOMB),MANDY'
        assert asn_items[0].employee_id == 250
        assert model[model_idx].asns[0].frum == '1910'
        assert model[model_idx].asns[0].thru == '2009'
        assert asn_list_ctrl.GetItemText(0, 1) == '10/19'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/20'

    @patch('presenters.presenter.AsnDlg.ShowModal')
    def testAddAsnLoadsForm(self, show_modal_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        model_idx = 6
        click_list_ctrl(list_ctrl, model_idx)
        item = view.get_selection()
        assert item.id == 279

        click_button(view.add_asn_btn)

        assert view.Children[2].Name == 'AsnDlg'
        asn_view = self.presenter.asn_presenter.view
        assert asn_view.Name == 'AssignmentPanel'

        assert asn_view.owner_lbl.GetLabelText() == 'Project: LIP 19-111 (Prescott)'
        assert asn_view.assignee_lbl.GetLabelText() == 'Employee: '
        assert not isinstance(asn_view.assignee, str)
        assert asn_view.assignee.Count == 156
        assert asn_view.assignee.CurrentSelection == -1
        assert asn_view.get_frum() == ''
        assert asn_view.get_thru() == ''
        assert asn_view.get_effort() == ''
        assert asn_view.get_notes() == ''

    @patch('presenters.presenter.AsnDlg.ShowModal')
    def testEditAsnLoadsForm(self, show_modal_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        model_idx = 0
        click_list_ctrl(list_ctrl, model_idx)
        item = view.get_selection()
        assert item.id == 303

        click_list_ctrl(asn_list_ctrl, 2)

        assert view.Children[2].Name == 'AsnDlg'
        asn_view = self.presenter.asn_presenter.view
        assert asn_view.Name == 'AssignmentPanel'

        assert asn_view.owner_lbl.GetLabelText() == 'Project: Biosimilar Merit_Waljee'
        assert asn_view.assignee_lbl.GetLabelText() == 'Employee: WIITALA,WYNDY L'
        assert isinstance(asn_view.assignee, str)
        assert asn_view.get_frum() == '2001'
        assert asn_view.get_thru() == '2009'
        assert asn_view.get_effort() == '2'
        assert asn_view.get_notes() == 'Per set form submitted 9/25'

    @patch('presenters.presenter.uil.show_error')
    def testDropAsnNoneSelected(self, show_error_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select project
        model_idx = 0
        click_list_ctrl(list_ctrl, model_idx)
        item = view.get_selection()
        assert item.id == 303

        # Make no selection

        # Check assignments
        asn_idx = 0
        assert len(model[model_idx].asns) == 5
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 5
        asn_ids = [2320, 2321, 2322, 2323, 2324]
        assert [asn.id for asn in asn_items] == asn_ids
        assert [asn.id for asn in model[model_idx].asns] == asn_ids
        assert asn_items[asn_idx].employee == 'ARASIM,MARIA E'
        assert asn_items[asn_idx].employee_id == 80
        assert model[model_idx].asns[asn_idx].frum == '2001'
        assert model[model_idx].asns[asn_idx].thru == '2009'
        assert asn_list_ctrl.GetItemText(0, 1) == '01/20'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/20'

        click_button(view.drop_asn_btn)

        args, kwargs = show_error_mock.call_args
        assert len(args) == 1
        assert len(kwargs) == 0
        assert args[0] == 'No assignments selected!'

        # No change in assignments
        assert len(model[model_idx].asns) == 5
        asn_idx = 0
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 5
        asn_ids = [2320, 2321, 2322, 2323, 2324]
        assert [asn.id for asn in asn_items] == asn_ids
        assert [asn.id for asn in model[model_idx].asns] == asn_ids
        assert asn_items[asn_idx].employee == 'ARASIM,MARIA E'
        assert asn_items[asn_idx].employee_id == 80
        assert model[model_idx].asns[asn_idx].frum == '2001'
        assert model[model_idx].asns[asn_idx].thru == '2009'
        assert asn_list_ctrl.GetItemText(0, 1) == '01/20'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/20'

    @patch('presenters.presenter.uil.confirm', return_value=False)
    def testDropAsnCancel(self, confirm_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select project
        model_idx = 0
        click_list_ctrl(list_ctrl, model_idx)
        item = view.get_selection()
        assert item.id == 303

        # Select assignment
        asn_list_ctrl = asn_list_ctrl
        asn_list_ctrl.Select(2)

        # Check assignments
        assert len(model[model_idx].asns) == 5
        asn_idx = 0
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 5
        asn_ids = [2320, 2321, 2322, 2323, 2324]
        assert [asn.id for asn in asn_items] == asn_ids
        assert [asn.id for asn in model[model_idx].asns] == asn_ids
        assert asn_items[asn_idx].employee == 'ARASIM,MARIA E'
        assert asn_items[asn_idx].employee_id == 80
        assert model[model_idx].asns[asn_idx].frum == '2001'
        assert model[model_idx].asns[asn_idx].thru == '2009'
        assert asn_list_ctrl.GetItemText(0, 1) == '01/20'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/20'

        click_button(view.drop_asn_btn)

        assert confirm_mock.call_count == 1
        args, kwargs = confirm_mock.call_args
        assert len(args) == 2
        assert len(kwargs) == 0
        assert args[1] == 'Drop selected assignments?'

        # Check assignments
        assert len(model[model_idx].asns) == 5
        asn_idx = 0
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 5
        asn_ids = [2320, 2321, 2322, 2323, 2324]
        assert [asn.id for asn in asn_items] == asn_ids
        assert [asn.id for asn in model[model_idx].asns] == asn_ids
        assert asn_items[asn_idx].employee == 'ARASIM,MARIA E'
        assert asn_items[asn_idx].employee_id == 80
        assert model[model_idx].asns[asn_idx].frum == '2001'
        assert model[model_idx].asns[asn_idx].thru == '2009'
        assert asn_list_ctrl.GetItemText(0, 1) == '01/20'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/20'

    @patch('presenters.presenter.uil.confirm', return_value=True)
    @patch('presenters.presenter.Dao._Dao__write', return_value=None)
    def testDropOneAsnUpdatesViewAndModel(self, write_mock, confirm_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select project
        model_idx = 0
        click_list_ctrl(list_ctrl, model_idx)
        item = view.get_selection()
        assert item.id == 303

        # Select assignment
        asn_list_ctrl = asn_list_ctrl
        asn_list_ctrl.Select(2)

        # Check assignments
        assert len(model[model_idx].asns) == 5
        asn_idx = 0
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 5
        asn_ids = [2320, 2321, 2322, 2323, 2324]
        assert [asn.id for asn in asn_items] == asn_ids
        assert [asn.id for asn in model[model_idx].asns] == asn_ids
        assert asn_items[asn_idx].employee == 'ARASIM,MARIA E'
        assert asn_items[asn_idx].employee_id == 80
        assert model[model_idx].asns[asn_idx].frum == '2001'
        assert model[model_idx].asns[asn_idx].thru == '2009'
        assert asn_list_ctrl.GetItemText(0, 1) == '01/20'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/20'

        click_button(view.drop_asn_btn)

        assert confirm_mock.call_count == 1
        calls = confirm_mock.call_args_list[0][0]
        prompt = 'Drop selected assignments?'
        assert calls[1] == prompt

        assert write_mock.call_count == 1
        args, kwargs = write_mock.call_args
        assert len(args) == 2
        assert len(kwargs) ==0
        assert args[0] == 'UPDATE assignments SET active=0 WHERE id IN (?)'
        assert args[1] == [2322]

        # Check assignments
        assert len(model[model_idx].asns) == 4
        asn_idx = 0
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 4
        asn_ids = [2320, 2321, 2323, 2324]
        assert [asn.id for asn in asn_items] == asn_ids
        assert [asn.id for asn in model[model_idx].asns] == asn_ids
        assert asn_items[asn_idx].employee == 'ARASIM,MARIA E'
        assert asn_items[asn_idx].employee_id == 80
        assert model[model_idx].asns[asn_idx].frum == '2001'
        assert model[model_idx].asns[asn_idx].thru == '2009'
        assert asn_list_ctrl.GetItemText(0, 1) == '01/20'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/20'

    @patch('presenters.presenter.uil.confirm', return_value=True)
    @patch('presenters.presenter.Dao._Dao__write', return_value=None)
    def testDropLastAsnUpdatesViewAndModel(self, write_mock, confirm_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select project
        model_idx = 0
        click_list_ctrl(list_ctrl, model_idx)
        item = view.get_selection()
        assert item.id == 303

        # Select assignment
        asn_list_ctrl = asn_list_ctrl
        asn_list_ctrl.Select(4)

        # Check assignments
        assert len(model[model_idx].asns) == 5
        asn_idx = 0
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 5
        asn_ids = [2320, 2321, 2322, 2323, 2324]
        assert [asn.id for asn in asn_items] == asn_ids
        assert [asn.id for asn in model[model_idx].asns] == asn_ids
        assert asn_items[asn_idx].employee == 'ARASIM,MARIA E'
        assert asn_items[asn_idx].employee_id == 80
        assert model[model_idx].asns[asn_idx].frum == '2001'
        assert model[model_idx].asns[asn_idx].thru == '2009'
        assert asn_list_ctrl.GetItemText(0, 1) == '01/20'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/20'

        click_button(view.drop_asn_btn)

        assert confirm_mock.call_count == 1
        args, kwargs = confirm_mock.call_args
        assert len(args) == 2
        assert len(kwargs) == 0
        assert args[1] == 'Drop selected assignments?'

        assert write_mock.call_count == 1
        args, kwargs = write_mock.call_args
        assert len(args) == 2
        assert len(kwargs) ==0
        assert args[0] == 'UPDATE assignments SET active=0 WHERE id IN (?)'
        assert args[1] == [2324]

        # Check assignments
        assert len(model[model_idx].asns) == 4
        asn_idx = 0
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 4
        asn_ids = [2320, 2321, 2322, 2323]
        assert [asn.id for asn in asn_items] == asn_ids
        assert [asn.id for asn in model[model_idx].asns] == asn_ids
        assert asn_items[asn_idx].employee == 'ARASIM,MARIA E'
        assert asn_items[asn_idx].employee_id == 80
        assert model[model_idx].asns[asn_idx].frum == '2001'
        assert model[model_idx].asns[asn_idx].thru == '2009'
        assert asn_list_ctrl.GetItemText(0, 1) == '01/20'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/20'

    @patch('presenters.presenter.uil.confirm', return_value=True)
    @patch('presenters.presenter.Dao._Dao__write', return_value=None)
    def testDropMultipleAsnsUpdatesViewAndModel(self, write_mock, confirm_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select project
        model_idx = 0
        click_list_ctrl(list_ctrl, model_idx)
        item = view.get_selection()
        assert item.id == 303

        # Select assignment
        asn_list_ctrl = asn_list_ctrl
        asn_list_ctrl.SelectObjects([
            model[model_idx].asns[1],
            model[model_idx].asns[3]
        ])

        # Check assignments
        assert len(model[model_idx].asns) == 5
        asn_idx = 0
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 5
        asn_ids = [2320, 2321, 2322, 2323, 2324]
        assert [asn.id for asn in asn_items] == asn_ids
        assert [asn.id for asn in model[model_idx].asns] == asn_ids
        assert asn_items[asn_idx].employee == 'ARASIM,MARIA E'
        assert asn_items[asn_idx].employee_id == 80
        assert model[model_idx].asns[asn_idx].frum == '2001'
        assert model[model_idx].asns[asn_idx].thru == '2009'
        assert asn_list_ctrl.GetItemText(0, 1) == '01/20'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/20'

        click_button(view.drop_asn_btn)

        assert confirm_mock.call_count == 1
        args, kwargs = confirm_mock.call_args
        assert len(args) == 2
        assert len(kwargs) == 0
        assert args[1] == 'Drop selected assignments?'

        assert write_mock.call_count == 1
        args, kwargs = write_mock.call_args
        assert len(args) == 2
        assert len(kwargs) ==0
        assert args[0] == 'UPDATE assignments SET active=0 WHERE id IN (?,?)'
        assert args[1] == [2321, 2323]

        # Check assignments
        assert len(model[model_idx].asns) == 3
        asn_idx = 0
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 3
        asn_ids = [2320, 2322, 2324]
        assert [asn.id for asn in asn_items] == asn_ids
        assert [asn.id for asn in model[model_idx].asns] == asn_ids
        assert asn_items[asn_idx].employee == 'ARASIM,MARIA E'
        assert asn_items[asn_idx].employee_id == 80
        assert model[model_idx].asns[asn_idx].frum == '2001'
        assert model[model_idx].asns[asn_idx].thru == '2009'
        assert asn_list_ctrl.GetItemText(0, 1) == '01/20'
        assert asn_list_ctrl.GetItemText(0, 2) == '09/20'
