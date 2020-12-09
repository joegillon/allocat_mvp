import unittest
from unittest.mock import patch
from tests.helpers import *
import globals as gbl
from models.dataset import AllocatDataSet
from presenters.employee_presenter import EmployeePresenter


class TestEmployeePresenter(unittest.TestCase):

    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None)

        gbl.COLOR_SCHEME = gbl.SKINS[gbl.pick_scheme()]
        gbl.DB_PATH = 'c:/bench/allocat/tests/allocat.db'

        gbl.dataset = AllocatDataSet(None)

        self.presenter = EmployeePresenter(self.frame)
        self.presenter.init_view()

    def tearDown(self):
        self.frame.Destroy()
        self.app.Destroy()

    def get_vars(self):
        return self.presenter.view, self.presenter.model, self.presenter.view.list_ctrl, self.presenter.view.asn_list_ctrl

    def testViewLoaded(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Check the employee list
        self.assertEqual(list_ctrl.GetObjects(), model)

        # No list click made
        self.assertEqual(view.get_selected_idx(), 0)

        # Check the details form
        expected = {
            'name': 'AARON,HENRY',
            'fte': 100,
            'investigator': False,
            'intern': False,
            'pm': False,
            'org': 'CCMR',
            'notes': 'Aaron note'
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check the assignments
        self.assertEqual(asn_list_ctrl.GetObjects(), model[0].asns)

    def testEmpListSelectWithAsns(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select 2nd employee
        model_idx = 1
        click_list_ctrl(list_ctrl, model_idx)

        # Check list
        self.assertEqual(view.get_selection(), model[model_idx])

        # Check form
        expected = {
            'name': 'BANKS,ERNEST',
            'fte': 100,
            'investigator': False,
            'intern': False,
            'pm': False,
            'org': 'CCMR',
            'notes': None,
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check assignments
        self.assertEqual(asn_list_ctrl.GetObjects(), model[model_idx].asns)

    def testSelectEmpListInvestigator(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select 5th employee
        model_idx = 5
        click_list_ctrl(list_ctrl, model_idx)

        # Check list
        self.assertEqual(view.get_selection(), model[model_idx])

        # Check form
        expected = {
            'name': 'GEHRIG,HENRY LOUIS',
            'fte': 50,
            'investigator': True,
            'intern': False,
            'pm': False,
            'org': 'SMITREC',
            'notes': 'Gehrig note',
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check assignments
        self.assertEqual(asn_list_ctrl.GetObjects(), model[model_idx].asns)

    def testSelectEmpListPM(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select 95th employee
        model_idx = 2
        click_list_ctrl(list_ctrl, model_idx)

        # Check list
        self.assertEqual(view.get_selection(), model[model_idx])

        # Check form
        expected = {
            'name': 'BERRA,LAWRENCE P',
            'fte': 80,
            'investigator': False,
            'intern': False,
            'pm': True,
            'org': 'CCMR',
            'notes': None,
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check assignments
        self.assertEqual(asn_list_ctrl.GetObjects(), model[model_idx].asns)

    def testSelectEmpListNoNotes(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select 95th employee
        model_idx = 2
        click_list_ctrl(list_ctrl, model_idx)

        # Check list
        self.assertEqual(view.get_selection(), model[model_idx])

        # Check form
        expected = {
            'name': 'BERRA,LAWRENCE P',
            'fte': 80,
            'investigator': False,
            'intern': False,
            'pm': True,
            'org': 'CCMR',
            'notes': None,
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check assignments
        self.assertEqual(asn_list_ctrl.GetObjects(), model[model_idx].asns)

    def testSelectEmpListWithNotes(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select 95th employee
        model_idx = 6
        click_list_ctrl(list_ctrl, model_idx)

        # Check list
        self.assertEqual(view.get_selection(), model[model_idx])

        # Check form
        expected = {
            'name': 'JETER,DEREK',
            'fte': 100,
            'investigator': False,
            'intern': True,
            'pm': False,
            'org': 'CCMR',
            'notes': 'Intern',
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check assignments
        self.assertEqual(asn_list_ctrl.GetObjects(), model[model_idx].asns)

    def testSelectEmpListNoEmail(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select 2nd employee
        model_idx = 1
        click_list_ctrl(list_ctrl, model_idx)

        # Check list
        self.assertEqual(view.get_selection(), model[model_idx])

        # Check form
        expected = {
            'name': 'BANKS,ERNEST',
            'fte': 100,
            'investigator': False,
            'intern': False,
            'pm': False,
            'org': 'CCMR',
            'notes': None,
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check assignments
        self.assertEqual(asn_list_ctrl.GetObjects(), model[model_idx].asns)

    def testSelectEmpListVAEmailOnly(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select 95th employee
        model_idx = 4
        click_list_ctrl(list_ctrl, model_idx)

        # Check list
        self.assertEqual(view.get_selection(), model[model_idx])

        # Check form
        expected = {
            'name': 'FORD,EDWARD C',
            'fte': 100,
            'investigator': False,
            'intern': False,
            'pm': True,
            'org': 'CCMR',
            'notes': None,
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check assignments
        self.assertEqual(asn_list_ctrl.GetObjects(), model[model_idx].asns)

    def testSelectEmpListNonVAEmailOnly(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select 95th employee
        model_idx = 12
        click_list_ctrl(list_ctrl, model_idx)

        # Check list
        self.assertEqual(view.get_selection(), model[model_idx])

        # Check form
        expected = {
            'name': 'WILLIAMS,THEODORE',
            'fte': 62,
            'investigator': True,
            'intern': False,
            'pm': False,
            'org': 'RCA',
            'notes': None,
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check assignments
        self.assertEqual(asn_list_ctrl.GetObjects(), model[model_idx].asns)

    def testSelectEmpListBothEmails(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select 2nd employee
        model_idx = 0
        click_list_ctrl(list_ctrl, model_idx)

        # Check list
        self.assertEqual(view.get_selection(), model[model_idx])

        # Check form
        expected = {
            'name': 'AARON,HENRY',
            'fte': 100,
            'investigator': False,
            'intern': False,
            'pm': False,
            'org': 'CCMR',
            'notes': 'Aaron note'
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check assignments
        self.assertEqual(asn_list_ctrl.GetObjects(), model[model_idx].asns)

    def testEmpNameFilter(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Search with no matches
        self.presenter.apply_filter('name_fltr_ctrl', 'z', '')

        self.assertEqual(list_ctrl.GetItemCount(), 0)

        # Check empty details form
        expected = {
            'name': None,
            'fte': None,
            'investigator': False,
            'intern': False,
            'pm': False,
            'org': None,
            'notes': None,
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check empty assignment list
        self.assertEqual(len(asn_list_ctrl.GetObjects()), 0)

        # Search for all projects with 'k'
        self.presenter.apply_filter('name_fltr_ctrl', 'k', '')

        expected = [e for e in model if 'K' in e.name]
        self.assertEqual(list_ctrl.GetFilteredObjects(), expected)

        # Check details
        expected = {
            'name': 'BANKS,ERNEST',
            'fte': 100,
            'investigator': False,
            'intern': False,
            'pm': False,
            'org': 'CCMR',
            'notes': None,
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check the assignments list
        expected = gbl.dataset.get_emp_rec(14).asns
        self.assertEqual(asn_list_ctrl.GetObjects(), expected)

        # Filter for 'ka'
        self.presenter.apply_filter('name_fltr_ctrl', 'a', 'k')

        expected = [e for e in model if 'KA' in e.name]
        self.assertEqual(list_ctrl.GetFilteredObjects(), expected)

        # Check details
        expected = {
            'name': 'KALINE,ALBERT W',
            'fte': 100,
            'investigator': False,
            'intern': False,
            'pm': False,
            'org': 'CCMR',
            'notes': 'Kaline note',
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check the assignments list
        expected = gbl.dataset.get_emp_rec(6).asns
        self.assertEqual(asn_list_ctrl.GetObjects(), expected)

        # And now backspace
        self.presenter.apply_filter('name_fltr_ctrl', '\b', 'ka')

        expected = [e for e in model if 'K' in e.name]
        self.assertEqual(list_ctrl.GetFilteredObjects(), expected)

        # Check details
        expected = {
            'name': 'BANKS,ERNEST',
            'fte': 100,
            'investigator': False,
            'intern': False,
            'pm': False,
            'org': 'CCMR',
            'notes': None,
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check the assignments list
        expected = gbl.dataset.get_emp_rec(14).asns
        self.assertEqual(asn_list_ctrl.GetObjects(), expected)

        # And now Cancel
        click_search_ctrl(view.name_fltr_ctrl)

        # Check the project list
        self.assertEqual(list_ctrl.GetObjects(), model)

        # Check that the first project has been selected by default
        model_idx = 0

        # No list click made

        # Check the details form
        expected = {
            'name': 'AARON,HENRY',
            'fte': 100,
            'investigator': False,
            'intern': False,
            'pm': False,
            'org': 'CCMR',
            'notes': 'Aaron note'
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check the assignments list
        self.assertEqual(asn_list_ctrl.GetObjects(), model[model_idx].asns)

    def testEmpNotesFilter(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Search with no matches
        self.presenter.apply_filter('notes_fltr_ctrl', 'x', '')

        self.assertEqual(list_ctrl.GetItemCount(), 0)

        # Check empty details form
        expected = {
            'name': None,
            'fte': None,
            'investigator': False,
            'intern': False,
            'pm': False,
            'org': None,
            'notes': None,
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check empty assignment list
        self.assertEqual(len(asn_list_ctrl.GetObjects()), 0)

        # Match '3'
        self.presenter.apply_filter('notes_fltr_ctrl', 'n', '')

        expected = [p for p in model if p.notes and 'n' in p.notes]
        self.assertEqual(list_ctrl.GetFilteredObjects(), expected)

        # Check details
        expected = {
            'name': 'AARON,HENRY',
            'fte': 100,
            'investigator': False,
            'intern': False,
            'pm': False,
            'org': 'CCMR',
            'notes': 'Aaron note',
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check the assignments list
        expected = gbl.dataset.get_emp_rec(44).asns
        self.assertEqual(asn_list_ctrl.GetObjects(), expected)

        # Filter for '31'
        self.presenter.apply_filter('notes_fltr_ctrl', 't', 'n')

        expected = [p for p in model if p.notes and 'nt' in p.notes]
        self.assertEqual(list_ctrl.GetFilteredObjects(), expected)

        # Check details
        expected = {
            'name': 'JETER,DEREK',
            'fte': 100,
            'investigator': False,
            'intern': True,
            'pm': False,
            'org': 'CCMR',
            'notes': 'Intern',
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check the assignments list
        expected = gbl.dataset.get_emp_rec(2).asns
        self.assertEqual(asn_list_ctrl.GetObjects(), expected)

        # And now backspace
        self.presenter.apply_filter('notes_fltr_ctrl', '\b', 'nt')

        expected = [p for p in model if p.notes and 'n' in p.notes]
        self.assertEqual(list_ctrl.GetFilteredObjects(), expected)

        # Check details
        expected = {
            'name': 'AARON,HENRY',
            'fte': 100,
            'investigator': False,
            'intern': False,
            'pm': False,
            'org': 'CCMR',
            'notes': 'Aaron note',
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check the assignments list
        expected = gbl.dataset.get_emp_rec(44).asns
        self.assertEqual(asn_list_ctrl.GetObjects(), expected)

        # And now Cancel
        click_search_ctrl(view.notes_fltr_ctrl)

        # Check the project list
        self.assertEqual(list_ctrl.GetObjects(), model)

        # Check that the first project has been selected by default
        model_idx = 0

        # No list click made

        # Check the details form
        expected = {
            'name': 'AARON,HENRY',
            'fte': 100,
            'investigator': False,
            'intern': False,
            'pm': False,
            'org': 'CCMR',
            'notes': 'Aaron note',
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check the assignments list
        self.assertEqual(asn_list_ctrl.GetObjects(), model[model_idx].asns)

    def testClearForm(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        click_button(view.clear_btn)

        # Check list has no selections
        self.assertEqual(view.get_selected_idx(), -1)

        # Check form is cleared
        expected = {
            'name': None,
            'fte': None,
            'investigator': False,
            'intern': False,
            'pm': False,
            'org': None,
            'notes': None,
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        self.assertEqual(len(asn_list_ctrl.GetObjects()), 0)

        self.assertEqual(view.get_save_button_label(), 'Add Employee')

    def testButtonLabelChange(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        self.assertEqual(view.get_save_button_label(), 'Update Employee')
        click_button(view.clear_btn)
        self.assertEqual(view.get_save_button_label(), 'Add Employee')
        dbl_click_list_ctrl(list_ctrl, 1)
        self.assertEqual(view.get_save_button_label(), 'Update Employee')

    def testValidateEmployeeFormOnAdd(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        click_button(view.clear_btn)

        # No name entered
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'Employee name required!')

        # Duplicate name
        view.set_name('FORD,EDWARDC')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'Employee name not unique!')

        # Invalid name
        view.set_name('GROUCHO MARX')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'Employee name invalid!')

        view.set_name('MARX')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'Employee name invalid!')

        view.set_name('MARX,GROUCHO:')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'Employee name invalid!')

        view.set_name('_MARX,GROUCHO')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'Employee name invalid!')

        view.set_name('_MARX,GROUCHO')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'Employee name invalid!')

        view.set_name('MARX,GROUCHO')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'FTE required!')

        view.set_fte('101')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'FTE must be number between 0-100!')

    def testValidateEmployeeFormOnUpdate(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        click_list_ctrl(list_ctrl, 0)
        self.assertEqual(self.presenter.get_selection(), model[0])

        view.set_name('')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'Employee name required!')

        view.set_name('KALINE,ALBERTW')
        err_msg = self.presenter.validate()
        assert err_msg == 'Employee name not unique!'

        # Note the space after the comma. Gets fixed later.
        view.set_name('MARX, GROUCHO')

        view.set_fte('101')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'FTE must be number between 0-100!')

    def testAddEmp(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        self.assertEqual(view.list_ctrl.GetItemCount(), 13)
        self.assertIsNone(gbl.dataset.get_emp_rec(45))

        click_button(view.clear_btn)

        # Fill in the form. No emails since that's done by ledger user.
        view.set_name('MARX, GROUCHO')
        view.set_fte('80')
        view.set_investigator(True)
        view.set_intern(False)
        view.set_pm(False)
        view.set_org('CCMR')
        view.set_notes('Bla bla bla')

        with patch('lib.ui_lib.show_msg') as mock_popup:
            mock_popup.return_value = True
            with patch('dal.dao.Dao._Dao__write') as mock_write:
                mock_write.return_value = 45
                click_button(view.save_btn)

        # Check the INSERT
        self.assertEqual(mock_write.call_count, 1)
        args, kwargs = mock_write.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 0)
        sql = ("INSERT INTO employees "
               "(name,fte,investigator,intern,pm,org,notes,active) "
               "VALUES (?,?,?,?,?,?,?,?)")
        self.assertEqual(args[0], sql)
        self.assertEqual(args[1], [
            'MARX,GROUCHO', 80, True, False, False, 'CCMR', 'Bla bla bla', 1])

        # Check model and list have been updated
        new_emp = gbl.dataset.get_emp_rec(45)
        item = view.get_selection()
        self.assertEqual(new_emp, item)
        self.assertEqual(view.list_ctrl.GetItemCount(), 14)

        # Check the new item is in the right spot alphabetically
        model_idx = view.get_selected_idx()
        self.assertEqual(model_idx, 10)
        self.assertEqual(list_ctrl.GetItemText(model_idx - 1, 0), 'MANTLE,MICKEY')
        self.assertEqual(list_ctrl.GetItemText(model_idx + 1, 0), 'MAYS,WILLIE HOWARD JR')

        # Check the YN display items
        self.assertEqual(list_ctrl.GetItemText(model_idx, 2), 'Y')
        self.assertEqual(list_ctrl.GetItemText(model_idx, 3), 'N')

        # No assignments
        self.assertEqual(asn_list_ctrl.GetItemCount(), 0)

        mock_popup.assert_called_once_with('Employee added!', 'Hallelujah!')

    def testUpdateEmp(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        self.assertEqual(view.list_ctrl.GetItemCount(), 13)

        model_idx = 6
        click_list_ctrl(list_ctrl, model_idx)

        emp = model[model_idx]
        self.assertEqual(view.get_selection(), emp)

        self.assertEqual(view.get_save_button_label(), 'Update Employee')

        # Check details
        expected = {
            'name': 'JETER,DEREK',
            'fte': 100,
            'investigator': False,
            'intern': True,
            'pm': False,
            'org': 'CCMR',
            'notes': 'Intern',
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check the assignments
        self.assertEqual(asn_list_ctrl.GetObjects(), model[model_idx].asns)

        # Edit the form
        view.set_name('MARX, GROUCHO')
        view.set_fte(80)
        view.set_investigator(True)
        view.set_intern(False)
        view.set_pm(False)
        view.set_org('Some Org')
        view.set_notes('Bla bla bla')

        with patch('lib.ui_lib.show_msg') as mock_popup:
            mock_popup.return_value = True
            with patch('dal.dao.Dao._Dao__write') as mock_write:
                mock_write.return_value = 1
                click_button(view.save_btn)

        # Check the UPDATE
        self.assertEqual(mock_write.call_count, 1)
        args, kwargs = mock_write.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 0)
        sql = ("UPDATE employees "
               "SET name=?,fte=?,investigator=?,intern=?,pm=?,org=?,notes=? "
               "WHERE id=?;")
        self.assertEqual(args[0], sql)
        self.assertEqual(args[1], [
            'MARX,GROUCHO', 80, True, False, False, 'Some Org', 'Bla bla bla', 2])

        # Check model and list have been updated
        updated_emp = gbl.dataset.get_emp_rec(2)
        item = view.get_selection()
        self.assertEqual(updated_emp, item)
        self.assertEqual(view.list_ctrl.GetItemCount(), 13)

        # Should be no change to assignments
        self.assertEqual(asn_list_ctrl.GetItemCount(), 1)
        self.assertEqual(emp.asns, updated_emp.asns)
        self.assertEqual(updated_emp.asns, asn_list_ctrl.GetObjects())

        mock_popup.assert_called_once_with('Employee updated!', 'Hallelujah!')

    def testDropEmp(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        self.assertEqual(view.list_ctrl.GetItemCount(), 13)
        self.assertEqual(len(model), 13)

        model_idx = 6
        click_list_ctrl(list_ctrl, model_idx)

        emp = gbl.dataset.get_emp_rec(2)
        self.assertEqual(view.get_selection(), emp)

        self.assertEqual(view.get_save_button_label(), 'Update Employee')

        # Check details
        expected = {
            'name': 'JETER,DEREK',
            'fte': 100,
            'investigator': False,
            'intern': True,
            'pm': False,
            'org': 'CCMR',
            'notes': 'Intern',
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check the assignments list
        self.assertEqual(asn_list_ctrl.GetObjects(), emp.asns)

        # User changes mind, cancels deletion
        with patch('lib.ui_lib.confirm') as mock_popup:
            mock_popup.return_value = False
            click_button(view.drop_btn)

        mock_popup.assert_called_once_with(view, 'Drop selected employee?')

        # Check no change
        self.assertEqual(view.get_selection(), emp)

        # Check details
        expected = {
            'name': 'JETER,DEREK',
            'fte': 100,
            'investigator': False,
            'intern': True,
            'pm': False,
            'org': 'CCMR',
            'notes': 'Intern',
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check the assignments list
        self.assertEqual(asn_list_ctrl.GetObjects(), emp.asns)

        # User confirms deletion
        with patch('lib.ui_lib.confirm') as mock_popup:
            mock_popup.return_value = True
            with patch('dal.dao.Dao._Dao__write') as mock_write:
                mock_write.return_value = 1
                click_button(view.drop_btn)

        # Check the confirmation
        mock_popup.assert_called_once_with(view, 'Drop selected employee?')

        # Check the SQL
        self.assertEqual(mock_write.call_count, 1)
        args, kwargs = mock_write.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 0)
        self.assertEqual(args[0], 'UPDATE employees SET active=0 WHERE id=?')
        self.assertEqual(args[1], (2,))

        # Check that employee removed from dataset
        # Need to test against new emp model in global dataset
        self.assertEqual(len(gbl.dataset.get_emp_data()), 12)
        self.assertIsNone(gbl.dataset.get_emp_rec(2))

        # Check that project removed from list
        self.assertEqual(view.list_ctrl.GetItemCount(), 12)
        emp_ids = [e.id for e in view.list_ctrl.GetObjects()]
        self.assertNotIn(2, emp_ids)

        # Check that first project is now selected
        model_idx = view.get_selected_idx()
        self.assertEqual(model_idx, 0)

        # Check the details form
        expected = {
            'name': 'AARON,HENRY',
            'fte': 100,
            'investigator': False,
            'intern': False,
            'pm': False,
            'org': 'CCMR',
            'notes': 'Aaron note',
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check the assignments list
        self.assertEqual(asn_list_ctrl.GetObjects(), model[model_idx].asns)

        self.assertEqual(view.get_save_button_label(), 'Update Employee')

    def testDropLastRec(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        model_idx = len(model) - 1
        click_list_ctrl(list_ctrl, model_idx)

        # User confirms deletion
        with patch('lib.ui_lib.confirm') as mock_popup:
            mock_popup.return_value = True
            with patch('dal.dao.Dao._Dao__write') as mock_write:
                mock_write.return_value = 1
                click_button(view.drop_btn)

        # Check the confirmation
        mock_popup.assert_called_once_with(view, 'Drop selected employee?')

        # Check the SQL
        self.assertEqual(mock_write.call_count, 1)
        args, kwargs = mock_write.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 0)
        self.assertEqual(args[0], 'UPDATE employees SET active=0 WHERE id=?')
        self.assertEqual(args[1], (9,))

        # Check that project removed from dataset
        # Need to test against new prj model in global dataset
        self.assertEqual(len(gbl.dataset.get_emp_data()), 12)
        self.assertIsNone(gbl.dataset.get_emp_rec(9))

        # Check that project removed from list
        self.assertEqual(view.list_ctrl.GetItemCount(), 12)
        emp_ids = [e.id for e in view.list_ctrl.GetObjects()]
        self.assertNotIn(9, emp_ids)

        # Check that first project is now selected
        model_idx = view.get_selected_idx()
        self.assertEqual(model_idx, 0)

        # Check the details form
        expected = {
            'name': 'AARON,HENRY',
            'fte': 100,
            'investigator': False,
            'intern': False,
            'pm': False,
            'org': 'CCMR',
            'notes': 'Aaron note',
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check the assignments list
        self.assertEqual(asn_list_ctrl.GetObjects(), model[model_idx].asns)

        self.assertEqual(view.get_save_button_label(), 'Update Employee')

    def testAddAsnLoadsForm(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        model_idx = 3
        click_list_ctrl(list_ctrl, model_idx)
        self.assertEqual(view.get_selection(), gbl.dataset.get_emp_rec(5))

        with patch('views.asn_dlg.AsnDlg.ShowModal') as mock_modal:
            click_button(view.add_asn_btn)

        mock_modal.assert_called_once()

        asn_view = self.presenter.asn_presenter.view
        self.assertEqual(asn_view.Name, 'AssignmentPanel')

        self.assertEqual(asn_view.owner_lbl.GetLabelText(), 'DIMAGGIO,JOSEPH P')
        self.assertEqual(asn_view.assignee_lbl.GetLabelText(), 'Project: ')
        self.assertNotIsInstance(asn_view.assignee, str)
        assignees = [''] + [p.name for p in gbl.dataset.get_prj_data()]
        self.assertEqual(asn_view.assignee.GetItems(), assignees)
        self.assertEqual(asn_view.assignee.CurrentSelection, -1)

        expected = {
            'employee_id': 5,
            'project_id': None,
            'frum': None,
            'thru': None,
            'effort': None,
            'notes': None
        }
        self.assertEqual(self.presenter.asn_presenter.get_form_values(), expected)

    def testEditAsnLoadsForm(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        model_idx = 3
        click_list_ctrl(list_ctrl, model_idx)
        self.assertEqual(view.get_selection(), gbl.dataset.get_emp_rec(5))

        with patch('views.asn_dlg.AsnDlg.ShowModal') as mock_modal:
            dbl_click_list_ctrl(asn_list_ctrl, 1)

        mock_modal.assert_called_once()

        asn_view = self.presenter.asn_presenter.view
        self.assertEqual(asn_view.Name, 'AssignmentPanel')

        self.assertEqual(asn_view.owner_lbl.GetLabelText(), 'DIMAGGIO,JOSEPH P')
        self.assertEqual(asn_view.assignee_lbl.GetLabelText(), 'Project: Prj 311')

        expected = {
            'employee_id': 5,
            'project_id': 311,
            'frum': '1910',
            'thru': '2009',
            'effort': '3',
            'notes': None
        }
        self.assertEqual(self.presenter.asn_presenter.get_form_values(), expected)

    def testDropAsnNoneSelected(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select employee
        model_idx = 4
        click_list_ctrl(list_ctrl, model_idx)
        self.assertEqual(view.get_selection(), gbl.dataset.get_emp_rec(16))

        # Check assignments
        expected = gbl.dataset.get_emp_rec(16).asns
        self.assertEqual(asn_list_ctrl.GetObjects(), expected)

        # Make no selection

        with patch('lib.ui_lib.show_error') as mock_popup:
            mock_popup.return_value = None
            click_button(view.drop_asn_btn)

        mock_popup.assert_called_once_with('No assignments selected!')

        # No change in assignments
        self.assertEqual(asn_list_ctrl.GetObjects(), expected)

    def testDropAsnCancel(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select project
        model_idx = 4
        click_list_ctrl(list_ctrl, model_idx)
        self.assertEqual(view.get_selection(), gbl.dataset.get_emp_rec(16))

        # Check assignments
        expected = gbl.dataset.get_emp_rec(16).asns
        self.assertEqual(asn_list_ctrl.GetObjects(), expected)

        # Select an assignment
        asn_list_ctrl.Select(0)

        with patch('lib.ui_lib.confirm') as mock_popup:
            mock_popup.return_value = False
            click_button(view.drop_asn_btn)

        mock_popup.assert_called_once_with(view, 'Drop selected assignments?')

        # No change in assignments

        self.assertEqual(asn_list_ctrl.GetObjects(), expected)

    def testDropOneAsn(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select project
        model_idx = 3
        click_list_ctrl(list_ctrl, model_idx)
        self.assertEqual(view.get_selection(), gbl.dataset.get_emp_rec(5))

        # Check assignments
        before_asns = [a for a in gbl.dataset.get_emp_rec(5).asns]
        self.assertEqual(asn_list_ctrl.GetObjects(), before_asns)

        # Select an assignment
        asn_list_ctrl.Select(0)

        with patch('lib.ui_lib.confirm') as mock_popup:
            mock_popup.return_value = True
            with patch('dal.dao.Dao._Dao__write') as mock_write:
                mock_write.return_value = 1
                click_button(view.drop_asn_btn)

        mock_popup.assert_called_once_with(view, 'Drop selected assignments?')

        # Check DB call
        self.assertEqual(mock_write.call_count, 1)
        args, kwargs = mock_write.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 0)
        self.assertEqual(args[0], 'UPDATE assignments SET active=0 WHERE id IN (?)')
        self.assertEqual(args[1], [2275])

        # Check gbl.dataset
        after_asns = [a for a in before_asns if a.id != 2275]
        self.assertEqual(asn_list_ctrl.GetObjects(), after_asns)

    def testDropLastAsn(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select project
        model_idx = 3
        click_list_ctrl(list_ctrl, model_idx)
        self.assertEqual(view.get_selection(), gbl.dataset.get_emp_rec(5))

        # Check assignments
        before_asns = [a for a in gbl.dataset.get_emp_rec(5).asns]
        self.assertEqual(asn_list_ctrl.GetObjects(), before_asns)

        # Select an assignment
        asn_list_ctrl.Select(1)

        with patch('lib.ui_lib.confirm') as mock_popup:
            mock_popup.return_value = True
            with patch('dal.dao.Dao._Dao__write') as mock_write:
                mock_write.return_value = 1
                click_button(view.drop_asn_btn)

        mock_popup.assert_called_once_with(view, 'Drop selected assignments?')

        # Check DB call
        self.assertEqual(mock_write.call_count, 1)
        args, kwargs = mock_write.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 0)
        self.assertEqual(args[0], 'UPDATE assignments SET active=0 WHERE id IN (?)')
        self.assertEqual(args[1], [2379])

        # Check gbl.dataset
        after_asns = [a for a in before_asns if a.id != 2379]
        self.assertEqual(asn_list_ctrl.GetObjects(), after_asns)

    def testDropMultipleAsnsUpdatesViewAndModel(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select project
        model_idx = 0
        click_list_ctrl(list_ctrl, model_idx)
        self.assertEqual(view.get_selection(), gbl.dataset.get_emp_rec(44))

        # Check assignments
        before_asns = [a for a in gbl.dataset.get_emp_rec(44).asns]
        self.assertEqual(asn_list_ctrl.GetObjects(), before_asns)

        # Select assignments
        asn_list_ctrl.SelectObjects([before_asns[0], before_asns[1]])

        with patch('lib.ui_lib.confirm') as mock_popup:
            mock_popup.return_value = True
            with patch('dal.dao.Dao._Dao__write') as mock_write:
                mock_write.return_value = 2
                click_button(view.drop_asn_btn)

        mock_popup.assert_called_once_with(view, 'Drop selected assignments?')

        # Check DB call
        self.assertEqual(mock_write.call_count, 1)
        args, kwargs = mock_write.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 0)
        self.assertEqual(args[0], 'UPDATE assignments SET active=0 WHERE id IN (?,?)')
        self.assertEqual(args[1], [2280, 2375])

        # Check gbl.dataset
        self.assertEqual(asn_list_ctrl.GetObjects(), [])
