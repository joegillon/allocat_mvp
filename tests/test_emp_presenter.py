import unittest
from unittest.mock import patch
from tests.helpers import *
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

        self.first_item = {
            'id': 28,
            'name': 'ABRAHAM,KRISTEN',
            'fte': 5,
            'investigator': False,
            'intern': False,
            'org': 'SMITREC',
            'notes': '',
            'active': True,
            'asns': []
        }

        self.first_item_form_vals = {
            'name': 'ABRAHAM,KRISTEN',
            'fte': 5,
            'investigator': False,
            'intern': False,
            'org': 'SMITREC',
            'notes': ''
        }

    def tearDown(self):
        self.frame.Destroy()
        self.app.Destroy()

    def get_vars(self):
        return self.presenter.view, self.presenter.model, self.presenter.view.list_ctrl, self.presenter.view.asn_list_ctrl

    def testViewLoaded(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # No list click made
        assert view.get_selected_idx() == 0

        # Check list has model and is sorted
        list_items = list_ctrl.GetObjects()
        assert list_items == model
        assert list_items[0].id == model[0].id == 28
        assert list_items[-1].id == model[-1].id == 69

        # Check form
        assert self.presenter.get_form_values() == self.first_item_form_vals
        assert view.get_save_button_label() == 'Update Employee'

        # Check assignments
        assert asn_list_ctrl.GetObjects() == model[0].asns == []

    def testEmpListSelectWithAsns(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select 143rd employee
        model_idx = 142
        click_list_ctrl(list_ctrl, model_idx)

        # Check list
        item = view.get_selection()
        assert item == model[model_idx]
        assert item.id == model[model_idx].id == 6

        # Check form
        expected_vals = {
            'name': 'VISNIC,STEPHANIE G',
            'fte': 100,
            'investigator': False,
            'intern': False,
            'org': 'CCMR',
            'notes': '',
        }
        assert self.presenter.get_form_values() == expected_vals

        # Check assignments
        asn_items = asn_list_ctrl.GetObjects()
        assert [asn.id for asn in asn_items] == [2346, 2348]
        assert model[model_idx].asns == asn_items

    def testSelectEmpListInvestigator(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select 95th employee
        model_idx = 94
        click_list_ctrl(list_ctrl, model_idx)

        # Check list
        item = view.get_selection()
        assert item == model[model_idx]
        assert item.id == model[model_idx].id == 12

        # Check form
        expected_vals = {
            'name': 'MCCARTHY,JOHN',
            'fte': 100,
            'investigator': True,
            'intern': False,
            'org': 'SMITREC',
            'notes': '',
        }
        assert self.presenter.get_form_values() == expected_vals
        assert view.get_save_button_label() == 'Update Employee'

        # Check assignments
        assert asn_list_ctrl.GetObjects() == model[model_idx].asns == []

    def testSelectEmpListWithNotes(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select 15th employee
        model_idx = 14
        click_list_ctrl(list_ctrl, model_idx)

        # Check list
        item = view.get_selection()
        assert item == model[model_idx]
        assert item.id == model[model_idx].id == 297

        # Check form
        expected_vals = {
            'name': 'BRYANT, COREY',
            'fte': 100,
            'investigator': False,
            'intern': False,
            'org': 'CCMR',
            'notes': 'Start date is 9/22/19 per Mike Robertson',
        }
        assert self.presenter.get_form_values() == expected_vals
        assert view.get_save_button_label() == 'Update Employee'

        # Check assignments
        assert model[model_idx].asns == asn_list_ctrl.GetObjects() == []

    def testEmpNameFilter(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Filter text box is empty, 'x' is entered
        self.presenter.apply_filter('name_fltr_ctrl', 'x', '')

        # Check filtered list
        assert list_ctrl.GetItemCount() == 4
        filtered_items = list_ctrl.GetFilteredObjects()
        assert [item.id for item in filtered_items] == [23, 103, 285, 301]

        # Check that the first item is selected
        model_idx = view.get_selected_idx()
        assert model_idx == 0
        assert view.get_selection() == [x for x in model if x.id==23][0]

        # Check form
        expected_vals = {
            'name': 'BOWERSOX,NICHOLAS W',
            'fte': 80,
            'investigator': False,
            'intern': False,
            'org': 'CCMR',
            'notes': '',
        }
        assert self.presenter.get_form_values() == expected_vals
        assert view.get_save_button_label() == 'Update Employee'

        # Check assignments
        assert model[model_idx].asns == asn_list_ctrl.GetObjects() == []

    def testCancelEmpNameFilter(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        click_button(view.name_fltr_ctrl)

        # Check list has model, is sorted with first item selected
        list_items = list_ctrl.GetObjects()
        assert list_items == model
        assert list_items[0].id == model[0].id == 28
        assert list_items[-1].id == model[-1].id == 69
        assert view.get_selected_idx() == 0

        # Check form
        assert self.presenter.get_form_values() == self.first_item_form_vals
        assert view.get_save_button_label() == 'Update Employee'

        # Check assignments
        assert asn_list_ctrl.GetObjects() == model[0].asns == []

    def testEmpNotesFilter(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Filter text box has 'inte', 'r' is typed
        self.presenter.apply_filter('notes_fltr_ctrl', 'r', 'inte')

        # Check filtered list
        assert list_ctrl.GetItemCount() == 4
        filtered_items = list_ctrl.GetFilteredObjects()
        assert [item.id for item in filtered_items] == [296, 293, 286, 287]

        # Select 3rd item
        model_idx = 2
        click_list_ctrl(list_ctrl, model_idx)

        # Check list
        item = view.get_selection()
        assert item.id == 286
        assert view.get_selection() == [x for x in model if x.id==286][0]

        # Check form
        expected_vals = {
            'name': 'SHANMUGASUNDARAM, PRIYA',
            'fte': 0,
            'investigator': False,
            'intern': True,
            'org': 'CCMR',
            'notes': 'Informatics Intern',
        }
        assert self.presenter.get_form_values() == expected_vals
        assert view.get_save_button_label() == 'Update Employee'

        # Check assignments
        assert model[model_idx].asns == asn_list_ctrl.GetObjects() == []

    def testCancelEmpNotesFilter(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        click_button(view.notes_fltr_ctrl)

        # Check list has model, is sorted with first item selected
        list_items = list_ctrl.GetObjects()
        assert list_items == model
        assert list_items[0].id == model[0].id == 28
        assert list_items[-1].id == model[-1].id == 69
        assert view.get_selected_idx() == 0

        # Check form
        assert self.presenter.get_form_values() == self.first_item_form_vals
        assert view.get_save_button_label() == 'Update Employee'

        # Check assignments
        assert asn_list_ctrl.GetObjects() == model[0].asns == []

    def testClearForm(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        click_button(view.clear_btn)

        # Check list has no selections
        assert view.get_selected_idx() == -1

        # Check form is cleared
        expected_vals = {
            'name': '',
            'fte': None,
            'investigator': False,
            'intern': False,
            'org': '',
            'notes': '',
        }
        assert self.presenter.get_form_values() == expected_vals
        assert view.get_save_button_label() == 'Add Employee'

        # Check assignments list is empty
        assert asn_list_ctrl.GetObjects() == []

    def testButtonLabelChange(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        assert view.get_save_button_label() == 'Update Employee'
        click_button(view.clear_btn)
        assert view.get_save_button_label() == 'Add Employee'
        click_list_ctrl(list_ctrl, 1)
        assert view.get_save_button_label() == 'Update Employee'

    def testValidateEmployeeFormOnAdd(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        self.presenter.clear()

        # No name entered
        err_msg = self.presenter.validate()
        assert err_msg == 'Employee name required!'

        # Duplicate name
        view.set_name('GILLON,LEAH R')
        err_msg = self.presenter.validate()
        assert err_msg == 'Employee name not unique!'

        view.set_name('GILLON, LEAHR')
        err_msg = self.presenter.validate()
        assert err_msg == 'Employee name not unique!'

        # Invalid name
        view.set_name('GROUCHO MARX')
        err_msg = self.presenter.validate()
        assert err_msg == 'Employee name invalid!'

        view.set_name('MARX')
        err_msg = self.presenter.validate()
        assert err_msg == 'Employee name invalid!'

        view.set_name('MARX,GROUCHO:')
        err_msg = self.presenter.validate()
        assert err_msg == 'Employee name invalid!'

        view.set_name('_MARX,GROUCHO')
        err_msg = self.presenter.validate()
        assert err_msg == 'Employee name invalid!'

        view.set_name('_MARX,GROUCHO')
        err_msg = self.presenter.validate()
        assert err_msg == 'Employee name invalid!'

        view.set_name('MARX,GROUCHO')
        err_msg = self.presenter.validate()
        assert err_msg == 'FTE required!'

        view.set_fte('101')
        err_msg = self.presenter.validate()
        assert err_msg == 'FTE must be number between 0-100!'

    def testValidateEmployeeFormOnUpdate(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        click_list_ctrl(list_ctrl, 0)
        assert self.presenter.get_selection().__dict__ == self.first_item

        view.set_name('')
        err_msg = self.presenter.validate()
        assert err_msg == 'Employee name required!'

        view.set_name('GILLON,LEAH R')
        err_msg = self.presenter.validate()
        assert err_msg == 'Employee name not unique!'

        view.set_name('ABRAHAM,  KRISTEN')
        view.set_fte('101')
        err_msg = self.presenter.validate()
        assert err_msg == 'FTE must be number between 0-100!'

    @patch('presenters.presenter.Dao._Dao__write', return_value=306)
    def testAddUpdatesModelAndView(self, write_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        click_button(view.clear_btn)

        # Fill in the form
        view.set_name('MARX,GROUCHO')
        view.set_fte('80')
        view.set_investigator(True)
        view.set_intern(False)
        view.set_org('CCMR')
        view.set_notes('Bla bla bla')

        click_button(view.save_btn)

        # Check the INSERT
        assert write_mock.call_count == 1
        args, kwargs = write_mock.call_args
        assert len(args) == 2
        assert len(kwargs) == 0
        assert args[0] == 'INSERT INTO employees (name,fte,investigator,intern,org,notes,active) VALUES (?,?,?,?,?,?,?)'
        assert args[1] == ['MARX,GROUCHO', 80, True, False, 'CCMR', 'Bla bla bla', 1]

        # Check list has new item
        list_items = list_ctrl.GetObjects()
        assert len(list_items) == 156

        # Gotta update our local model with the new stuff. Just for this test.
        model = self.presenter.model

        # Check the new item is in the right spot alphabetically
        model_idx = view.get_selected_idx()
        assert model_idx == 94
        assert list_ctrl.GetItemText(model_idx - 1, 0) == 'MARINEC,NICOLLE A'
        assert list_ctrl.GetItemText(model_idx + 1, 0) == 'MCCARTHY,JOHN'

        # Check the correct new item
        item = list_items[model_idx]
        assert item.id == 306
        assert item.name == 'MARX,GROUCHO'
        assert item.fte == 80
        assert item.investigator == True
        assert item.intern == False
        assert item.org == 'CCMR'
        assert item.notes == 'Bla bla bla'

        # Check the YN display items
        assert list_ctrl.GetItemText(model_idx, 2) == 'Y'
        assert list_ctrl.GetItemText(model_idx, 3) == 'N'

        # Check the new model
        assert item == model[model_idx]

        # Check assignments list is empty
        assert asn_list_ctrl.GetObjects() == model[model_idx].asns == []

    @patch('presenters.presenter.Dao._Dao__write', return_value=1)
    def testUpdateUpdatesModelAndView(self, write_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        model_idx = 6
        click_list_ctrl(list_ctrl, model_idx)

        # Check list
        assert view.get_selection() == model[model_idx]

        # Check details
        expected_vals = {
            'name': 'BELANCOURT, PAT',
            'fte': 100,
            'investigator': False,
            'intern': False,
            'org': 'CCMR',
            'notes': '',
        }
        assert self.presenter.get_form_values() == expected_vals
        assert view.get_save_button_label() == 'Update Employee'

        # Check the assignments
        assert asn_list_ctrl.GetObjects() == model[model_idx].asns

        # New data
        view.set_name('BELANCOURT,PAT')
        view.set_fte(80)
        view.set_investigator(True)
        view.set_intern(True)
        view.set_org('Some Org')
        view.set_notes('Bla bla bla')

        click_button(view.save_btn)

        # Check the UPDATE
        assert write_mock.call_count == 1
        args, kwargs = write_mock.call_args
        assert len(args) == 2
        assert len(kwargs) == 0
        assert args[0] == 'UPDATE employees SET name=?,fte=?,investigator=?,intern=?,org=?,notes=? WHERE id=?;'
        assert args[1] == ['BELANCOURT,PAT', 80, True, True, 'Some Org', 'Bla bla bla', 292]

        # Check the list - still same number of items
        list_items = list_ctrl.GetObjects()
        assert len(list_items) == 155

        # New stuff should be in both list and model
        assert list_items == model

        # Check updated item to make sure data has changed
        model_idx = view.get_selected_idx()
        assert model_idx == 6
        item = list_items[model_idx]

        expected_vals = {
            'name': 'BELANCOURT,PAT',
            'fte': 80,
            'investigator': True,
            'intern': True,
            'org': 'Some Org',
            'notes': 'Bla bla bla',
        }
        assert self.presenter.get_form_values() == expected_vals
        assert view.get_save_button_label() == 'Update Employee'
        assert item == model[model_idx]

        # Should be no change to assignments
        assert asn_list_ctrl.GetObjects() == model[model_idx].asns

    @patch('presenters.presenter.uil.confirm', return_value=True)
    @patch('presenters.presenter.Dao._Dao__write', return_value=1)
    def testDropUpdatesModelAndView(self, write_mock, confirm_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        model_idx = 6
        click_list_ctrl(list_ctrl, model_idx)

        # Check the number of items & number of models
        items = list_ctrl.GetObjects()
        assert len(items) == len(model) == 155

        # The item to be dropped
        item = view.get_selection()
        assert item.id == 292

        # Get form values
        expected_vals = {
            'name': 'BELANCOURT, PAT',
            'fte': 100,
            'investigator': False,
            'intern': False,
            'org': 'CCMR',
            'notes': '',
        }
        assert self.presenter.get_form_values() == expected_vals
        assert view.get_save_button_label() == 'Update Employee'

        # Has an assignment
        assert len(model[model_idx].asns) == 1
        assert model[model_idx].asns[0].id == 2240
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 1
        assert asn_items[0].id == 2240

        click_button(view.drop_btn)

        # Check that user confirmed drop
        assert confirm_mock.call_count == 1
        args, kwargs = confirm_mock.call_args
        assert len(args) == 2
        assert len(kwargs) == 0
        assert args[1] == 'Drop selected employee?'

        # Check the SQL
        assert write_mock.call_count == 1
        args, kwargs = write_mock.call_args
        assert len(args) == 2
        assert len(kwargs) ==0
        assert args[0] == 'UPDATE employees SET active=0 WHERE id=?'
        assert args[1] == (292,)

        # Check the list & model length
        items = list_ctrl.GetObjects()
        assert len(items) == len(model) == 154

        # Check list matches model
        assert items == model

        # Check that next item has been selected
        model_idx = view.get_selected_idx()
        assert model_idx == 6       # Still the same idx!
        expected_item = {
            'id': 47,
            'name': 'BLOW,FREDERIC PHD',
            'fte': 63,
            'investigator': True,
            'intern': False,
            'org': 'SMITREC',
            'notes': '',
            'active': True,
            'asns': []
        }
        item = view.get_selection()
        assert item.__dict__ == expected_item

        # Check the details form
        expected_vals = {
            'name': 'BLOW,FREDERIC PHD',
            'fte': 63,
            'investigator': True,
            'intern': False,
            'org': 'SMITREC',
            'notes': '',
        }
        assert self.presenter.get_form_values() == expected_vals
        assert view.get_save_button_label() == 'Update Employee'

        # Check the assignments list
        assert asn_list_ctrl.GetObjects() == model[model_idx].asns == []

    @patch('presenters.presenter.uil.confirm', return_value=True)
    @patch('presenters.presenter.Dao._Dao__write', return_value=1)
    def testDropLastRecUpdatesModelAndView(self, write_mock, confirm_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Full number of items and models
        assert list_ctrl.GetItemCount() == len(model) == 155

        # Select last item
        model_idx = 154
        click_list_ctrl(list_ctrl, model_idx)

        # Get the item
        item = view.get_selection()
        expected_item = {
            'id': 69,
            'name': 'ZIVIN,KARA',
            'fte': 63,
            'investigator': False,
            'intern': False,
            'org': 'CCMR',
            'notes': '',
            'active': True,
            'asns': []
        }
        assert item.__dict__ == expected_item
        assert list_ctrl.GetItemText(model_idx, 2) == 'N'
        assert list_ctrl.GetItemText(model_idx, 3) == 'N'

        # Check the details form
        expected_vals = {
            'name': 'ZIVIN,KARA',
            'fte': 63,
            'investigator': False,
            'intern': False,
            'org': 'CCMR',
            'notes': '',
        }
        assert self.presenter.get_form_values() == expected_vals
        assert view.get_save_button_label() == 'Update Employee'

        # Check the assignments list
        assert asn_list_ctrl.GetObjects() == []

        click_button(view.drop_btn)

        # Check confirmation
        assert confirm_mock.call_count == 1
        args, kwargs = confirm_mock.call_args
        assert len(args) == 2
        assert len(kwargs) == 0
        assert args[1] == 'Drop selected employee?'

        # Check SQL
        assert write_mock.call_count == 1
        args, kwargs = write_mock.call_args
        assert len(args) == 2
        assert len(kwargs) ==0
        assert args[0] == 'UPDATE employees SET active=0 WHERE id=?'
        assert args[1] == (69,)

        # One less item
        assert list_ctrl.GetItemCount() == 154
        assert len(model) == 154

        # Check the new selected item
        model_idx = view.get_selected_idx()
        assert model_idx == 153
        item = view.get_selection()
        expected_item = {
            'id': 86,
            'name': 'YOULES,BRADLEY W',
            'fte': 100,
            'investigator': False,
            'intern': False,
            'org': 'CCMR',
            'notes': '',
            'active': True,
            'asns': model[model_idx].asns
        }
        assert item.__dict__ == expected_item
        assert list_ctrl.GetItemText(model_idx, 2) == 'N'
        assert list_ctrl.GetItemText(model_idx, 3) == 'N'
        assert view.get_save_button_label() == 'Update Employee'

        # Check the details form
        expected_vals = {
            'name': 'YOULES,BRADLEY W',
            'fte': 100,
            'investigator': False,
            'intern': False,
            'org': 'CCMR',
            'notes': '',
        }
        assert self.presenter.get_form_values() == expected_vals

        # Check the assignments list
        assert asn_list_ctrl.GetObjects() == model[model_idx].asns

    @patch('presenters.presenter.AsnDlg.ShowModal')
    def testAddAsnLoadsForm(self, show_modal_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select employee
        model_idx = 111
        click_list_ctrl(list_ctrl, model_idx)
        item = view.get_selection()
        assert item.id == 295

        click_button(view.add_asn_btn)

        assert view.Children[2].Name == 'AsnDlg'
        asn_view = self.presenter.asn_presenter.view
        assert asn_view.Name == 'AssignmentPanel'

        assert asn_view.owner_lbl.GetLabelText() == 'Employee: RANUSCH, ALLISON'
        assert asn_view.assignee_lbl.GetLabelText() == 'Project: '
        assert not isinstance(asn_view.assignee, str)
        assert asn_view.assignee.Count == 32
        assert asn_view.assignee.CurrentSelection == -1
        assert asn_view.get_frum() == ''
        assert asn_view.get_thru() == ''
        assert asn_view.get_effort() == ''
        assert asn_view.get_notes() == ''

    @patch('presenters.presenter.AsnDlg.ShowModal')
    def testEditAsnLoadsForm(self, show_modal_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select employee
        model_idx = 111
        click_list_ctrl(list_ctrl, model_idx)
        item = view.get_selection()
        assert item.id == 295

        # Select first assignment
        asn_idx = 0
        click_list_ctrl(asn_list_ctrl, asn_idx)

        # Pop up dialog was called
        assert view.Children[2].Name == 'AsnDlg'
        asn_view = self.presenter.asn_presenter.view
        assert asn_view.Name == 'AssignmentPanel'

        assert asn_view.owner_lbl.GetLabelText() == 'Employee: RANUSCH, ALLISON'
        assert asn_view.assignee_lbl.GetLabelText() == 'Project: HRO Metrics Evaluation (Damschroder)'
        assert isinstance(asn_view.assignee, str)
        assert asn_view.get_frum() == '1907'
        assert asn_view.get_thru() == '2009'
        assert asn_view.get_effort() == '50'
        assert asn_view.get_notes() == ''

    @patch('presenters.presenter.uil.show_error')
    def testDropAsnNoneSelected(self, show_error_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select employee
        model_idx = 119
        click_list_ctrl(list_ctrl, model_idx)
        item = view.get_selection()
        assert item.id == 22

        # No assignmet selection made

        # Check assignments
        assert len(model[model_idx].asns) == 4
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 4
        asn_ids = [2030, 2290, 2293, 2398]
        assert [asn.id for asn in asn_items] == asn_ids
        assert [asn.id for asn in model[model_idx].asns] == asn_ids

        click_button(view.drop_asn_btn)

        args, kwargs = show_error_mock.call_args
        assert len(args) == 1
        assert len(kwargs) == 0
        assert args[0] == 'No assignments selected!'

        # No change in assignments
        assert len(model[model_idx].asns) == 4
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 4
        asn_ids = [2030, 2290, 2293, 2398]
        assert [asn.id for asn in asn_items] == asn_ids
        assert [asn.id for asn in model[model_idx].asns] == asn_ids

    @patch('presenters.presenter.uil.confirm', return_value=False)
    def testDropAsnCancel(self, confirm_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select employee
        model_idx = 119
        click_list_ctrl(list_ctrl, model_idx)
        item = view.get_selection()
        assert item.id == 22

        # Check assignments
        assert len(model[model_idx].asns) == 4
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 4
        assert [asn.id for asn in asn_items] == [2030, 2290, 2293, 2398]

        # Select assignment
        obj = asn_list_ctrl
        obj.Select(2)

        click_button(view.drop_asn_btn)

        assert confirm_mock.call_count == 1
        args, kwargs = confirm_mock.call_args
        assert len(args) == 2
        assert len(kwargs) == 0
        assert args[1] == 'Drop selected assignments?'

        # Check assignments
        assert len(model[model_idx].asns) == 4
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 4
        assert [asn.id for asn in asn_items] == [2030, 2290, 2293, 2398]

    @patch('presenters.presenter.uil.confirm', return_value=True)
    @patch('presenters.presenter.Dao._Dao__write', return_value=None)
    def testDropOneAsnUpdatesViewAndModel(self, write_mock, confirm_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select employee
        model_idx = 119
        self.presenter.set_selection(model_idx)
        item = view.get_selection()
        assert item.id == 22

        # Select assignment
        obj = asn_list_ctrl
        obj.Select(2)

        # Check assignments
        assert len(model[model_idx].asns) == 4
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 4
        assert [asn.id for asn in asn_items] == [2030, 2290, 2293, 2398]

        click_button(view.drop_asn_btn)

        assert confirm_mock.call_count == 1
        args, kwargs = confirm_mock.call_args
        assert len(args) == 2
        assert len(kwargs) ==0
        assert args[1] ==  'Drop selected assignments?'

        assert write_mock.call_count == 1
        args, kwargs = write_mock.call_args
        assert len(args) == 2
        assert len(kwargs) ==0
        assert args[0] == 'UPDATE assignments SET active=0 WHERE id IN (?)'
        assert args[1] == [2293]

        # Check assignments
        assert len(model[model_idx].asns) == 3
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 3
        assert [asn.id for asn in asn_items] == [2030, 2290, 2398]

    @patch('presenters.presenter.uil.confirm', return_value=True)
    @patch('presenters.presenter.Dao._Dao__write', return_value=None)
    def testDropLastAsnUpdatesViewAndModel(self, write_mock, confirm_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select employee
        model_idx = 119
        self.presenter.set_selection(model_idx)
        item = view.get_selection()
        assert item.id == 22

        # Select assignment
        obj = asn_list_ctrl
        obj.Select(3)

        # Check assignments
        assert len(model[model_idx].asns) == 4
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 4
        assert [asn.id for asn in asn_items] == [2030, 2290, 2293, 2398]

        click_button(view.drop_asn_btn)

        assert confirm_mock.call_count == 1
        args, kwargs = confirm_mock.call_args
        assert len(args) == 2
        assert len(kwargs) == 0
        assert args[1] ==  'Drop selected assignments?'

        assert write_mock.call_count == 1
        args, kwargs = write_mock.call_args
        assert len(args) == 2
        assert len(kwargs) ==0
        assert args[0] == 'UPDATE assignments SET active=0 WHERE id IN (?)'
        assert args[1] == [2398]

        # Check assignments
        assert len(model[model_idx].asns) == 3
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 3
        assert [asn.id for asn in asn_items] == [2030, 2290, 2293]

    @patch('presenters.presenter.uil.confirm', return_value=True)
    @patch('presenters.presenter.Dao._Dao__write', return_value=None)
    def testDropMultipleAsnsUpdatesViewAndModel(self, write_mock, confirm_mock):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select employee
        model_idx = 119
        click_list_ctrl(list_ctrl, model_idx)
        item = view.get_selection()
        assert item.id == 22

        # Select assignment
        selections = [
            model[model_idx].asns[1],
            model[model_idx].asns[3]
        ]
        asn_list_ctrl.SelectObjects(selections)

        # Check assignments
        assert len(model[model_idx].asns) == 4
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 4
        assert [asn.id for asn in asn_items] == [2030, 2290, 2293, 2398]

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
        assert args[1] == [2290, 2398]

        # Check assignments
        assert len(model[model_idx].asns) == 2
        asn_items = asn_list_ctrl.GetObjects()
        assert len(asn_items) == 2
        assert [asn.id for asn in asn_items] == [2030, 2293]
