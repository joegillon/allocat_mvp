import unittest
from unittest.mock import patch
import wx
import globals as gbl
from models.dataset import AllocatDataSet
from presenters.employee_presenter import EmployeePresenter


class TestEmployeePresenter(unittest.TestCase):

    def setUp(self):
        gbl.dataset = AllocatDataSet(db_path='c:/bench/allocat/tests/allocat.db')
        self.app = wx.App()
        self.frame = wx.Frame(None)

        self.presenter = EmployeePresenter(self.frame)
        self.presenter.init_view()

    def tearDown(self):
        self.frame.Destroy()
        self.app.Destroy()

    def testViewLoaded(self):
        idx = 0
        list_items = self.presenter.view.list_ctrl.GetObjects()
        assert len(list_items) == 155
        item = list_items[idx]
        assert item.id == 28
        assert item.name == 'ABRAHAM,KRISTEN'
        assert item.fte == 5
        assert item.investigator == False
        assert item.intern == False
        assert item.org == 'SMITREC'
        assert item.notes == ''

        # Check the details form
        assert self.presenter.view.get_name() == 'ABRAHAM,KRISTEN'
        assert self.presenter.view.get_fte() == '5'
        assert self.presenter.view.get_investigator() == False
        assert self.presenter.view.get_intern() == False
        assert self.presenter.view.get_org() == 'SMITREC'
        assert self.presenter.view.get_notes() == ''
        assert self.presenter.view.get_button_label() == 'Update Employee'

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 0
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 0

    def testEmpListSelectWithAsns(self):
        idx = 142
        self.presenter.set_selection(idx)
        item = self.presenter.view.get_selection()
        assert item.id == 6
        assert item.name == 'VISNIC,STEPHANIE G'
        assert item.fte == 100
        assert item.investigator == False
        assert item.intern == False
        assert item.org == 'CCMR'

        # Check the details form
        assert self.presenter.view.get_name() == 'VISNIC,STEPHANIE G'
        assert self.presenter.view.get_fte() == '100'
        assert self.presenter.view.get_investigator() == False
        assert self.presenter.view.get_intern() == False
        assert self.presenter.view.get_org() == 'CCMR'
        assert self.presenter.view.get_notes() == ''
        assert self.presenter.view.get_button_label() == 'Update Employee'

        # Check the assignments list
        asns = self.presenter.model[idx].asns
        assert len(asns) == 2
        assert asns[0].id == 2346
        assert asns[0].employee_id == 6
        assert asns[0].project_id == 304
        assert asns[0].frum == '2004'
        assert asns[0].thru == '2009'
        assert asns[0].effort == 15
        assert asns[0].notes == ''
        assert asns[0].active == True
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 2
        assert ass_items[0].project == 'NIA VA Aim _PtCare (Maust)'
        assert ass_items[0].project_id == 304
        assert ass_items[0].frum == '2004'
        assert ass_items[0].thru == '2009'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 1) == '04/20'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 2) == '09/20'
        assert ass_items[0].effort == 15
        assert ass_items[0].notes == ''

    def testSelectEmpListInvestigator(self):
        idx = 94
        self.presenter.set_selection(idx)
        item = self.presenter.view.get_selection()
        assert item.id == 12
        assert item.name == 'MCCARTHY,JOHN'
        assert item.fte == 100
        assert item.investigator == True
        assert item.intern == False
        assert item.org == 'SMITREC'

        # Check the details form
        assert self.presenter.view.get_name() == 'MCCARTHY,JOHN'
        assert self.presenter.view.get_fte() == '100'
        assert self.presenter.view.get_investigator() == True
        assert self.presenter.view.get_intern() == False
        assert self.presenter.view.get_org() == 'SMITREC'
        assert self.presenter.view.get_notes() == ''
        assert self.presenter.view.get_button_label() == 'Update Employee'

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 0
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 0

    def testSelectEmpListWithNotes(self):
        idx = 14
        self.presenter.set_selection(idx)
        item = self.presenter.view.get_selection()
        assert item.id == 297
        assert item.name == 'BRYANT, COREY'
        assert item.fte == 100
        assert item.investigator == False
        assert item.intern == False
        assert item.org == 'CCMR'

        # Check the details form
        assert self.presenter.view.get_name() == 'BRYANT, COREY'
        assert self.presenter.view.get_fte() == '100'
        assert self.presenter.view.get_investigator() == False
        assert self.presenter.view.get_intern() == False
        assert self.presenter.view.get_org() == 'CCMR'
        assert self.presenter.view.get_notes() == 'Start date is 9/22/19 per Mike Robertson'
        assert self.presenter.view.get_button_label() == 'Update Employee'

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 0
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 0

    def testEmpNameFilter(self):
        self.presenter.apply_filter('name_fltr_ctrl', 'x', '')
        assert self.presenter.view.list_ctrl.GetItemCount() == 4
        objs = self.presenter.view.list_ctrl.GetFilteredObjects()
        assert [obj.id for obj in objs] == [23, 103, 285, 301]
        assert [obj.name for obj in objs] == [
            'BOWERSOX,NICHOLAS W',
            'EXE,CHRISTINE L',
            'FIDEL,ALEX',
            'MONAHAN, MAX'
        ]
        idx = self.presenter.view.get_selected_idx()
        assert idx == 0

        item = self.presenter.view.get_selection()
        assert item.id == 23
        assert item.name == 'BOWERSOX,NICHOLAS W'
        assert item.fte == 80
        assert item.investigator == False
        assert item.intern == False
        assert item.org == 'CCMR'
        assert item.notes == ''
        assert self.presenter.view.get_button_label() == 'Update Employee'

        # Check the details form
        assert self.presenter.view.get_name() == 'BOWERSOX,NICHOLAS W'
        assert self.presenter.view.get_fte() == '80'
        assert self.presenter.view.get_investigator() == False
        assert self.presenter.view.get_intern() == False
        assert self.presenter.view.get_org() == 'CCMR'
        assert self.presenter.view.get_notes() == ''

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 0
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 0

    def testCancelEmpNameFilter(self):
        evt = wx.CommandEvent(wx.EVT_SEARCHCTRL_CANCEL_BTN.typeId)
        obj = self.presenter.view.name_fltr_ctrl
        evt.SetEventObject(obj)
        evt.SetId(obj.GetId())
        obj.GetEventHandler().ProcessEvent(evt)

        idx = self.presenter.view.get_selected_idx()
        list_items = self.presenter.view.list_ctrl.GetObjects()
        assert len(list_items) == 155
        item = list_items[idx]
        assert item.id == 28
        assert item.name == 'ABRAHAM,KRISTEN'
        assert item.fte == 5
        assert item.investigator == False
        assert item.intern == False
        assert item.org == 'SMITREC'

        # Check the details form
        assert self.presenter.view.get_name() == 'ABRAHAM,KRISTEN'
        assert self.presenter.view.get_fte() == '5'
        assert self.presenter.view.get_investigator() == False
        assert self.presenter.view.get_intern() == False
        assert self.presenter.view.get_org() == 'SMITREC'
        assert self.presenter.view.get_notes() == ''
        assert self.presenter.view.get_button_label() == 'Update Employee'

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 0
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 0

    def testEmpNotesFilter(self):
        self.presenter.apply_filter('notes_fltr_ctrl', 'r', 'inte')
        assert self.presenter.view.list_ctrl.GetItemCount() == 4
        objs = self.presenter.view.list_ctrl.GetFilteredObjects()
        assert [obj.id for obj in objs] == [296, 293, 286, 287]
        assert [obj.name for obj in objs] == [
            'LIU, DAVID',
            'SAINII, RYAN',
            'SHANMUGASUNDARAM, PRIYA',
            'VUONG, KIM'
        ]
        idx = 2
        self.presenter.set_selection(idx)
        item = self.presenter.view.get_selection()
        assert item.id == 286
        assert item.name == 'SHANMUGASUNDARAM, PRIYA'
        assert item.fte == 0
        assert item.investigator == False
        assert item.intern == True
        assert item.notes == 'Informatics Intern'
        assert item.org == 'CCMR'

        # Check the details form
        assert self.presenter.view.get_name() == 'SHANMUGASUNDARAM, PRIYA'
        assert self.presenter.view.get_fte() == '0'
        assert self.presenter.view.get_investigator() == False
        assert self.presenter.view.get_intern() == True
        assert self.presenter.view.get_notes() == 'Informatics Intern'
        assert self.presenter.view.get_org() == 'CCMR'

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 0
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 0

    def testCancelEmpNotesFilter(self):
        evt = wx.CommandEvent(wx.EVT_SEARCHCTRL_CANCEL_BTN.typeId)
        obj = self.presenter.view.name_fltr_ctrl
        evt.SetEventObject(obj)
        evt.SetId(obj.GetId())
        obj.GetEventHandler().ProcessEvent(evt)

        idx = self.presenter.view.get_selected_idx()
        list_items = self.presenter.view.list_ctrl.GetObjects()
        assert len(list_items) == 155
        item = list_items[idx]
        assert item.id == 28
        assert item.name == 'ABRAHAM,KRISTEN'
        assert item.fte == 5
        assert item.investigator == False
        assert item.intern == False
        assert item.org == 'SMITREC'

        # Check the details form
        assert self.presenter.view.get_name() == 'ABRAHAM,KRISTEN'
        assert self.presenter.view.get_fte() == '5'
        assert self.presenter.view.get_investigator() == False
        assert self.presenter.view.get_intern() == False
        assert self.presenter.view.get_org() == 'SMITREC'
        assert self.presenter.view.get_notes() == ''
        assert self.presenter.view.get_button_label() == 'Update Employee'

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 0
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 0

    def testClearForm(self):
        evt = wx.CommandEvent(wx.EVT_BUTTON.typeId)
        obj = self.presenter.view.clear_btn
        evt.SetEventObject(obj)
        evt.SetId(obj.GetId())
        obj.GetEventHandler().ProcessEvent(evt)

        assert self.presenter.view.get_selected_idx() == -1
        assert self.presenter.view.name_ctrl.GetValue() == ''
        assert self.presenter.view.fte_ctrl.GetValue().strip() == ''
        assert self.presenter.view.investigator_ctrl.GetValue() == False
        assert self.presenter.view.intern_ctrl.GetValue() == False
        assert self.presenter.view.org_ctrl.GetValue() == ''
        assert self.presenter.view.notes_ctrl.GetValue() == ''
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 0
        assert self.presenter.view.get_button_label() == 'Add Employee'

    def testButtonLabelChange(self):
        assert self.presenter.view.get_button_label() == 'Update Employee'
        self.presenter.clear()
        assert self.presenter.view.get_button_label() == 'Add Employee'
        self.presenter.set_selection(1)
        assert self.presenter.view.get_button_label() == 'Update Employee'

    def testValidateEmployeeFormOnAdd(self):
        self.presenter.clear()

        # No name entered
        err_msg = self.presenter.validate()
        assert err_msg == 'Employee name required!'

        # Duplicate name
        self.presenter.view.set_name('GILLON,LEAH R')
        err_msg = self.presenter.validate()
        assert err_msg == 'Employee name not unique!'

        self.presenter.view.set_name('GILLON, LEAHR')
        err_msg = self.presenter.validate()
        assert err_msg == 'Employee name not unique!'

        # Invalid name
        self.presenter.view.set_name('GROUCHO MARX')
        err_msg = self.presenter.validate()
        assert err_msg == 'Employee name invalid!'

        self.presenter.view.set_name('MARX')
        err_msg = self.presenter.validate()
        assert err_msg == 'Employee name invalid!'

        self.presenter.view.set_name('MARX,GROUCHO:')
        err_msg = self.presenter.validate()
        assert err_msg == 'Employee name invalid!'

        self.presenter.view.set_name('_MARX,GROUCHO')
        err_msg = self.presenter.validate()
        assert err_msg == 'Employee name invalid!'

        self.presenter.view.set_name('_MARX,GROUCHO')
        err_msg = self.presenter.validate()
        assert err_msg == 'Employee name invalid!'

        self.presenter.view.set_name('MARX,GROUCHO')
        err_msg = self.presenter.validate()
        assert err_msg == 'FTE required!'

        self.presenter.view.set_fte('101')
        err_msg = self.presenter.validate()
        assert err_msg == 'FTE must be number between 0-100!'

    def testValidateEmployeeFormOnUpdate(self):
        self.presenter.set_selection(0)
        assert self.presenter.view.get_name() == 'ABRAHAM,KRISTEN'

        self.presenter.view.set_name('')
        err_msg = self.presenter.validate()
        assert err_msg == 'Employee name required!'

        self.presenter.view.set_name('GILLON,LEAH R')
        err_msg = self.presenter.validate()
        assert err_msg == 'Employee name not unique!'

        self.presenter.view.set_name('ABRAHAM,  KRISTEN')
        self.presenter.view.set_fte('101')
        err_msg = self.presenter.validate()
        assert err_msg == 'FTE must be number between 0-100!'

    @patch('presenters.presenter.Employee.add')
    def testAddUpdatesModelAndView(self, add_mock):
        self.presenter.clear()
        self.presenter.view.set_name('MARX,GROUCHO')
        self.presenter.view.set_fte('80')
        self.presenter.view.set_investigator(True)
        self.presenter.view.set_intern(False)
        self.presenter.view.set_org('CCMR')
        self.presenter.view.set_notes('Bla bla bla')

        add_mock.return_value = 306
        self.presenter.save()

        list_items = self.presenter.view.list_ctrl.GetObjects()
        assert len(list_items) == 156
        idx = self.presenter.view.get_selected_idx()
        assert idx == 94
        assert self.presenter.view.list_ctrl.GetItemText(idx - 1, 0) == 'MARINEC,NICOLLE A'
        assert self.presenter.view.list_ctrl.GetItemText(idx + 1, 0) == 'MCCARTHY,JOHN'
        item = list_items[idx]
        assert item.id == 306
        assert item.name == 'MARX,GROUCHO'
        assert item.fte == '80'
        assert item.investigator == True
        assert self.presenter.view.list_ctrl.GetItemText(idx, 2) == 'Y'
        assert item.intern == False
        assert self.presenter.view.list_ctrl.GetItemText(idx, 3) == 'N'
        assert item.org == 'CCMR'
        assert item.notes == 'Bla bla bla'

        emp_model = self.presenter.model[idx]
        assert emp_model.id == 306
        assert emp_model.name == 'MARX,GROUCHO'
        assert emp_model.fte == '80'
        assert emp_model.investigator == True
        assert emp_model.intern == False
        assert emp_model.org == 'CCMR'
        assert emp_model.notes == 'Bla bla bla'
        assert emp_model.active == 1
        assert emp_model.asns == []

        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 0

    @patch('presenters.presenter.Employee.do_update')
    def testUpdateUpdatesModelAndView(self, do_update_mock):
        idx = 6
        self.presenter.set_selection(idx)
        item = self.presenter.view.get_selection()
        assert item.id == 292
        assert item.name == 'BELANCOURT, PAT'
        assert item.fte == 100
        assert item.investigator == False
        assert item.intern == False
        assert item.org == 'CCMR'
        assert item.notes == ''
        assert self.presenter.view.get_button_label() == 'Update Employee'

        assert self.presenter.view.get_name() == 'BELANCOURT, PAT'
        assert self.presenter.view.get_fte() == '100'
        assert self.presenter.view.get_investigator() == False
        assert self.presenter.view.get_intern() == False
        assert self.presenter.view.get_org() == 'CCMR'
        assert self.presenter.view.get_notes() == ''

        assert len(self.presenter.model[idx].asns) == 1
        asn_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(asn_items) == 1
        assert asn_items[0].id == 2240
        assert asn_items[0].employee == 'BELANCOURT, PAT'
        assert asn_items[0].employee_id == 292
        assert asn_items[0].project == 'IIR 17-269 Morphomics (Su)'
        assert asn_items[0].project_id == 293
        assert asn_items[0].frum == '1906'
        assert asn_items[0].thru == '2009'

        self.presenter.view.set_name('BELANCOURT,PAT')
        self.presenter.view.set_fte(80)
        self.presenter.view.set_investigator(True)
        self.presenter.view.set_intern(True)
        self.presenter.view.set_org('Some Org')
        self.presenter.view.set_notes('Bla bla bla')

        do_update_mock.return_value = 1
        self.presenter.save()

        list_items = self.presenter.view.list_ctrl.GetObjects()
        assert len(list_items) == 155
        idx = self.presenter.view.get_selected_idx()
        assert idx == 6
        item = list_items[idx]
        assert item.id == 292
        assert item.name == 'BELANCOURT,PAT'
        assert item.fte == '80'
        assert item.investigator == True
        assert item.intern == True
        assert item.org == 'Some Org'
        assert item.notes == 'Bla bla bla'

        emp_model = self.presenter.model[idx]
        assert emp_model.id == 292
        assert emp_model.name == 'BELANCOURT,PAT'
        assert emp_model.fte == '80'
        assert emp_model.investigator == True
        assert emp_model.intern == True
        assert emp_model.org == 'Some Org'
        assert emp_model.notes == 'Bla bla bla'
        assert emp_model.active == 1

        assert len(self.presenter.model[idx].asns) == 1
        asn_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(asn_items) == 1
        assert asn_items[0].id == 2240
        assert asn_items[0].employee == 'BELANCOURT, PAT'
        assert asn_items[0].employee_id == 292
        assert asn_items[0].project == 'IIR 17-269 Morphomics (Su)'
        assert asn_items[0].project_id == 293
        assert asn_items[0].frum == '1906'
        assert asn_items[0].thru == '2009'

    @patch('presenters.presenter.Employee.drop')
    def testDropUpdatesModelAndView(self, drop_mock):
        idx = 6
        self.presenter.set_selection(idx)
        item = self.presenter.view.get_selection()
        assert item.id == 292
        assert item.name == 'BELANCOURT, PAT'
        assert item.fte == 100
        assert item.investigator == False
        assert item.intern == False
        assert item.org == 'CCMR'
        assert item.notes == ''
        assert self.presenter.view.get_button_label() == 'Update Employee'

        assert self.presenter.view.get_name() == 'BELANCOURT, PAT'
        assert self.presenter.view.get_fte() == '100'
        assert self.presenter.view.get_investigator() == False
        assert self.presenter.view.get_intern() == False
        assert self.presenter.view.get_org() == 'CCMR'
        assert self.presenter.view.get_notes() == ''

        assert len(self.presenter.model[idx].asns) == 1
        asn_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(asn_items) == 1
        assert asn_items[0].id == 2240
        assert asn_items[0].employee == 'BELANCOURT, PAT'
        assert asn_items[0].employee_id == 292
        assert asn_items[0].project == 'IIR 17-269 Morphomics (Su)'
        assert asn_items[0].project_id == 293
        assert asn_items[0].frum == '1906'
        assert asn_items[0].thru == '2009'

        drop_mock.return_value = 1
        self.presenter.drop()

        idx = self.presenter.view.get_selected_idx()
        assert idx == 6
        item = self.presenter.view.get_selection()
        assert item.id == 47
        assert item.name == 'BLOW,FREDERIC PHD'
        assert item.fte == 63
        assert item.investigator == True
        assert item.intern == False
        assert self.presenter.view.list_ctrl.GetItemText(idx, 2) == 'Y'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 3) == 'N'
        assert item.org == 'SMITREC'
        assert item.notes == ''
        assert self.presenter.view.get_button_label() == 'Update Employee'

        # Check the details form
        assert self.presenter.view.get_name() == 'BLOW,FREDERIC PHD'
        assert self.presenter.view.get_fte() == '63'
        assert self.presenter.view.get_investigator() == True
        assert self.presenter.view.get_intern() == False
        assert self.presenter.view.get_org() == 'SMITREC'
        assert self.presenter.view.get_notes() == ''

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 0
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 0

    @patch('presenters.presenter.Employee.drop')
    def testDropLastRecUpdatesModelAndView(self, drop_mock):
        idx = 154
        self.presenter.set_selection(idx)
        item = self.presenter.view.get_selection()
        assert item.id == 69
        assert item.name == 'ZIVIN,KARA'
        assert item.fte == 63
        assert item.investigator == False
        assert item.intern == False
        assert item.org == 'CCMR'
        assert item.notes == ''
        assert self.presenter.view.list_ctrl.GetItemText(idx, 2) == 'N'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 3) == 'N'
        assert self.presenter.view.get_button_label() == 'Update Employee'

        # Check the details form
        assert self.presenter.view.get_name() == 'ZIVIN,KARA'
        assert self.presenter.view.get_fte() == '63'
        assert self.presenter.view.get_investigator() == False
        assert self.presenter.view.get_intern() == False
        assert self.presenter.view.get_org() == 'CCMR'
        assert self.presenter.view.get_notes() == ''

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 0
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 0

        drop_mock.return_value = 1
        self.presenter.drop()

        idx = self.presenter.view.get_selected_idx()
        assert idx == 153
        item = self.presenter.view.get_selection()
        assert item.id == 86
        assert item.name == 'YOULES,BRADLEY W'
        assert item.fte == 100
        assert item.investigator == False
        assert item.intern == False
        assert self.presenter.view.list_ctrl.GetItemText(idx, 2) == 'N'
        assert self.presenter.view.list_ctrl.GetItemText(idx, 3) == 'N'
        assert item.org == 'CCMR'
        assert item.notes == ''
        assert self.presenter.view.get_button_label() == 'Update Employee'

        # Check the details form
        assert self.presenter.view.get_name() == 'YOULES,BRADLEY W'
        assert self.presenter.view.get_fte() == '100'
        assert self.presenter.view.get_investigator() == False
        assert self.presenter.view.get_intern() == False
        assert self.presenter.view.get_org() == 'CCMR'
        assert self.presenter.view.get_notes() == ''

        # Check the assignments list
        assert len(self.presenter.model[idx].asns) == 6
        ass_items = self.presenter.view.asn_list_ctrl.GetObjects()
        assert len(ass_items) == 6
        assert ass_items[0].employee == 'YOULES,BRADLEY W'
        assert ass_items[0].employee_id == 86
        assert ass_items[0].project == 'ProAccess (Saini)'
        assert ass_items[0].project_id == 278
        assert self.presenter.model[idx].asns[0].frum == '1902'
        assert self.presenter.model[idx].asns[0].thru == '1906'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 1) == '02/19'
        assert self.presenter.view.asn_list_ctrl.GetItemText(0, 2) == '06/19'
