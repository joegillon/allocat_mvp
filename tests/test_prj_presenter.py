import unittest
from unittest.mock import patch
from tests.helpers import *
import globals as gbl
import tests.allocat_data.test_data as test_data
from models.dataset import AllocatDataSet
from presenters.project_presenter import ProjectPresenter


class TestProjectPresenter(unittest.TestCase):

    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None)

        gbl.COLOR_SCHEME = gbl.SKINS[gbl.pick_scheme()]
        gbl.DB_PATH = 'c:/bench/allocat/tests/allocat.db'

        gbl.dataset = AllocatDataSet(None)

        self.presenter = ProjectPresenter(self.frame)
        self.presenter.init_view()

    def tearDown(self):
        self.frame.Destroy()
        self.app.Destroy()

    def get_vars(self):
        return self.presenter.view, self.presenter.model, self.presenter.view.list_ctrl, self.presenter.view.asn_list_ctrl

    def testViewLoadedPIAndPM(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Check the project list (also their assignments)
        self.assertEqual(list_ctrl.GetObjects(), model)

        # Check that the dropdowns are populated
        emps = gbl.dataset.get_emp_data()
        expected = [''] + [e.name for e in emps if e.investigator]
        self.assertEqual(view.pi_ctrl.GetItems(), expected)
        expected = [''] + [e.name for e in emps if e.pm]
        self.assertEqual(view.pm_ctrl.GetItems(), expected)

        # Check that the first project has been selected by default
        model_idx = view.get_selected_idx()
        self.assertEqual(model_idx, 0)

        # No list click

        # Check the details form
        expected = {
            'name': 'Prj 297',
            'full_name': 'Prj Full Name 297',
            'frum': '1901',
            'thru': '1912',
            'pi': gbl.dataset.get_emp_rec(24),
            'pm': gbl.dataset.get_emp_rec(5),
            'notes': 'Note 297'
        }
        self.assertEqual(self.presenter.get_form_values(), expected)
        
        # Check dates displayed properly
        self.assertEqual(view.frum_ctrl.GetValue(), '01/19')
        self.assertEqual(view.thru_ctrl.GetValue(), '12/19')

        # Check the assignments list
        self.assertEqual(asn_list_ctrl.GetObjects(), model[model_idx].asns)
        self.assertEqual(asn_list_ctrl.GetItemText(0, 1), '10/19')
        self.assertEqual(asn_list_ctrl.GetItemText(0, 2), '12/19')
        self.assertEqual(asn_list_ctrl.GetItemText(1, 1), '10/19')
        self.assertEqual(asn_list_ctrl.GetItemText(1, 2), '12/19')

        self.assertEqual(view.get_save_button_label(), 'Update Project')

    def testPrjListSelectPIAndPM(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        model_idx = 4
        click_list_ctrl(list_ctrl, model_idx)

        # Check the details form
        expected = {
            'name': 'Prj 309',
            'full_name': 'Prj Full Name 309',
            'frum': '1908',
            'thru': '2009',
            'pi': gbl.dataset.get_emp_rec(9),
            'pm': gbl.dataset.get_emp_rec(32),
            'notes': 'Note 309'
        }
        self.assertEqual(self.presenter.get_form_values(), expected)
        self.assertEqual(view.frum_ctrl.GetValue(), '08/19')
        self.assertEqual(view.thru_ctrl.GetValue(), '09/20')

        # Check the assignments list
        self.assertEqual(asn_list_ctrl.GetObjects(), model[model_idx].asns)
        self.assertEqual(asn_list_ctrl.GetItemText(0, 1), '10/19')
        self.assertEqual(asn_list_ctrl.GetItemText(0, 2), '09/20')
        self.assertEqual(asn_list_ctrl.GetItemText(1, 1), '02/20')
        self.assertEqual(asn_list_ctrl.GetItemText(1, 2), '09/20')
        self.assertEqual(asn_list_ctrl.GetItemText(2, 1), '02/20')
        self.assertEqual(asn_list_ctrl.GetItemText(2, 2), '02/20')

    def testPrjListSelectNoPINoAsns(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        model_idx = 1
        click_list_ctrl(list_ctrl, model_idx)

        # Check the details form
        expected = {
            'name': 'Prj 298',
            'full_name': 'Prj Full Name 298',
            'frum': '1907',
            'thru': '2406',
            'pi': None,
            'pm': gbl.dataset.get_emp_rec(5),
            'notes': 'Note 298'
        }
        self.assertEqual(self.presenter.get_form_values(), expected)
        self.assertEqual(view.frum_ctrl.GetValue(), '07/19')
        self.assertEqual(view.thru_ctrl.GetValue(), '06/24')

        # Check the assignments list
        self.assertEqual(asn_list_ctrl.GetObjects(), model[model_idx].asns)

    def testPrjListSelectNoPM(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        model_idx = 2
        click_list_ctrl(list_ctrl, model_idx)

        # Check the details form
        expected = {
            'name': 'Prj 299',
            'full_name': 'Prj Full Name 299',
            'frum': '1907',
            'thru': '2106',
            'pi': gbl.dataset.get_emp_rec(24),
            'pm': None,
            'notes': None
        }
        self.assertEqual(self.presenter.get_form_values(), expected)
        self.assertEqual(view.frum_ctrl.GetValue(), '07/19')
        self.assertEqual(view.thru_ctrl.GetValue(), '06/21')

        # Check the assignments list
        self.assertEqual(asn_list_ctrl.GetObjects(), model[model_idx].asns)
        self.assertEqual(asn_list_ctrl.GetItemText(0, 1), '02/20')
        self.assertEqual(asn_list_ctrl.GetItemText(0, 2), '03/20')
        self.assertEqual(asn_list_ctrl.GetItemText(1, 1), '07/19')
        self.assertEqual(asn_list_ctrl.GetItemText(1, 2), '06/21')

    def testPrjNameFilter(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Search with no matches
        self.presenter.apply_filter('name_fltr_ctrl', 'x', '')

        self.assertEqual(list_ctrl.GetItemCount(), 0)
        
        # Check empty details form
        expected = {
            'name': None,
            'full_name': None,
            'frum': None,
            'thru': None,
            'pi': None,
            'pm': None,
            'notes': None
        }
        self.assertEqual(self.presenter.get_form_values(), expected)
        
        # Check empty assignment list
        self.assertEqual(len(asn_list_ctrl.GetObjects()), 0)

        # Search for all projects with '3'
        self.presenter.apply_filter('name_fltr_ctrl', '3', '')

        expected = [p for p in model if '3' in p.name]
        self.assertEqual(list_ctrl.GetFilteredObjects(), expected)
        
        # Check details
        expected = {
            'name': 'Prj 301',
            'full_name': 'Prj Full Name 301',
            'frum': '1904',
            'thru': '1909',
            'pi': None,
            'pm': None,
            'notes': None
        }
        self.assertEqual(self.presenter.get_form_values(), expected)
        self.assertEqual(view.frum_ctrl.GetValue(), '04/19')
        self.assertEqual(view.thru_ctrl.GetValue(), '09/19')

        # Check the assignments list
        expected = gbl.dataset.get_prj_rec(301).asns
        self.assertEqual(asn_list_ctrl.GetObjects(), expected)

        # Filter for '31'
        self.presenter.apply_filter('name_fltr_ctrl', '1', '3')

        expected = [p for p in model if '31' in p.name]
        self.assertEqual(list_ctrl.GetFilteredObjects(), expected)

        # Check details
        expected = {
            'name': 'Prj 311',
            'full_name': 'Prj Full Name 311',
            'frum': '1910',
            'thru': '2009',
            'pi': None,
            'pm': gbl.dataset.get_emp_rec(32),
            'notes': None
        }
        self.assertEqual(self.presenter.get_form_values(), expected)
        self.assertEqual(view.frum_ctrl.GetValue(), '10/19')
        self.assertEqual(view.thru_ctrl.GetValue(), '09/20')

        # Check the assignments list
        expected = gbl.dataset.get_prj_rec(311).asns
        self.assertEqual(asn_list_ctrl.GetObjects(), expected)
        
        # And now backspace
        self.presenter.apply_filter('name_fltr_ctrl', '\b', '31')

        expected = [p for p in model if '3' in p.name]
        self.assertEqual(list_ctrl.GetFilteredObjects(), expected)
        
        # Check details
        expected = {
            'name': 'Prj 301',
            'full_name': 'Prj Full Name 301',
            'frum': '1904',
            'thru': '1909',
            'pi': None,
            'pm': None,
            'notes': None
        }
        self.assertEqual(self.presenter.get_form_values(), expected)
        self.assertEqual(view.frum_ctrl.GetValue(), '04/19')
        self.assertEqual(view.thru_ctrl.GetValue(), '09/19')

        # Check the assignments list
        expected = gbl.dataset.get_prj_rec(301).asns
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
            'name': 'Prj 297',
            'full_name': 'Prj Full Name 297',
            'frum': '1901',
            'thru': '1912',
            'pi': gbl.dataset.get_emp_rec(24),
            'pm': gbl.dataset.get_emp_rec(5),
            'notes': 'Note 297'
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check dates displayed properly
        self.assertEqual(view.frum_ctrl.GetValue(), '01/19')
        self.assertEqual(view.thru_ctrl.GetValue(), '12/19')

        # Check the assignments list
        self.assertEqual(asn_list_ctrl.GetObjects(), model[model_idx].asns)
        self.assertEqual(asn_list_ctrl.GetItemText(0, 1), '10/19')
        self.assertEqual(asn_list_ctrl.GetItemText(0, 2), '12/19')
        self.assertEqual(asn_list_ctrl.GetItemText(1, 1), '10/19')
        self.assertEqual(asn_list_ctrl.GetItemText(1, 2), '12/19')

    def testPrjNotesFilter(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Search with no matches
        self.presenter.apply_filter('notes_fltr_ctrl', 'x', '')

        self.assertEqual(list_ctrl.GetItemCount(), 0)

        # Check empty details form
        expected = {
            'name': None,
            'full_name': None,
            'frum': None,
            'thru': None,
            'pi': None,
            'pm': None,
            'notes': None
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check empty assignment list
        self.assertEqual(len(asn_list_ctrl.GetObjects()), 0)

        # Match '3'
        self.presenter.apply_filter('notes_fltr_ctrl', '3', '')

        expected = [p for p in model if p.notes and '3' in p.notes]
        self.assertEqual(list_ctrl.GetFilteredObjects(), expected)

        # Check details
        expected = {
            'name': 'Prj 309',
            'full_name': 'Prj Full Name 309',
            'frum': '1908',
            'thru': '2009',
            'pi': gbl.dataset.get_emp_rec(9),
            'pm': gbl.dataset.get_emp_rec(32),
            'notes': 'Note 309'
        }
        self.assertEqual(self.presenter.get_form_values(), expected)
        self.assertEqual(view.frum_ctrl.GetValue(), '08/19')
        self.assertEqual(view.thru_ctrl.GetValue(), '09/20')

        # Check the assignments list
        expected = gbl.dataset.get_prj_rec(309).asns
        self.assertEqual(asn_list_ctrl.GetObjects(), expected)

        # Filter for '31'
        self.presenter.apply_filter('notes_fltr_ctrl', '1', '3')

        expected = [p for p in model if p.notes and '31' in p.notes]
        self.assertEqual(list_ctrl.GetFilteredObjects(), expected)

        # Check details
        expected = {
            'name': 'Prj 312',
            'full_name': 'Prj Full Name 312',
            'frum': '1909',
            'thru': '2109',
            'pi': gbl.dataset.get_emp_rec(9),
            'pm': None,
            'notes': 'Note 312'
        }
        self.assertEqual(self.presenter.get_form_values(), expected)
        self.assertEqual(view.frum_ctrl.GetValue(), '09/19')
        self.assertEqual(view.thru_ctrl.GetValue(), '09/21')

        # Check the assignments list
        expected = gbl.dataset.get_prj_rec(312).asns
        self.assertEqual(asn_list_ctrl.GetObjects(), expected)

        # And now backspace
        self.presenter.apply_filter('notes_fltr_ctrl', '\b', '31')

        expected = [p for p in model if p.notes and '3' in p.notes]
        self.assertEqual(list_ctrl.GetFilteredObjects(), expected)

        # Check details
        expected = {
            'name': 'Prj 309',
            'full_name': 'Prj Full Name 309',
            'frum': '1908',
            'thru': '2009',
            'pi': gbl.dataset.get_emp_rec(9),
            'pm': gbl.dataset.get_emp_rec(32),
            'notes': 'Note 309'
        }
        self.assertEqual(self.presenter.get_form_values(), expected)
        self.assertEqual(view.frum_ctrl.GetValue(), '08/19')
        self.assertEqual(view.thru_ctrl.GetValue(), '09/20')

        # Check the assignments list
        expected = gbl.dataset.get_prj_rec(309).asns
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
            'name': 'Prj 297',
            'full_name': 'Prj Full Name 297',
            'frum': '1901',
            'thru': '1912',
            'pi': gbl.dataset.get_emp_rec(24),
            'pm': gbl.dataset.get_emp_rec(5),
            'notes': 'Note 297'
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check dates displayed properly
        self.assertEqual(view.frum_ctrl.GetValue(), '01/19')
        self.assertEqual(view.thru_ctrl.GetValue(), '12/19')

        # Check the assignments list
        self.assertEqual(asn_list_ctrl.GetObjects(), model[model_idx].asns)
        self.assertEqual(asn_list_ctrl.GetItemText(0, 1), '10/19')
        self.assertEqual(asn_list_ctrl.GetItemText(0, 2), '12/19')
        self.assertEqual(asn_list_ctrl.GetItemText(1, 1), '10/19')
        self.assertEqual(asn_list_ctrl.GetItemText(1, 2), '12/19')

    def testClearForm(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        click_button(view.clear_btn)

        # Check list has no selection
        self.assertEqual(view.get_selected_idx(), -1)

        # Check the form is cleared
        expected = {
            'name': None,
            'full_name': None,
            'frum': None,
            'thru': None,
            'pi': None,
            'pm': None,
            'notes': None
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        self.assertEqual(view.pi_ctrl.CurrentSelection, 0)
        self.assertEqual(view.pm_ctrl.CurrentSelection, 0)
        self.assertEqual(len(asn_list_ctrl.GetObjects()), 0)

        self.assertEqual(view.get_save_button_label(), 'Add Project')

    def testButtonLabelChange(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        self.assertEqual(view.get_save_button_label(), 'Update Project')
        click_button(view.clear_btn)
        self.assertEqual(view.get_save_button_label(), 'Add Project')
        dbl_click_list_ctrl(list_ctrl, 1)
        self.assertEqual(view.get_save_button_label(), 'Update Project')

    def testValidateProjectFormOnAdd(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        click_button(view.clear_btn)

        # No project name entered
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'Project name required!')

        # Duplicate project name
        view.set_name('Prj 309')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'Project name not unique!')

        # Set to unique name
        view.set_name('Test Prj 1')

        # No full name entered
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'Project full name required!')

        # Duplicate full name
        view.set_full_name('Prj full name 297')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'Project full name not unique!')

        # Set to unique full name
        view.set_full_name('Test Project One')

        # No frum date
        # The control defaults to 00/00, so validate can be called without a
        # call to prettify via set_frum, set_thru. Also the user can enter 00/00.
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'From, Thru dates required!')

        # Bogus and empty from, thru dates tested in test_month_lib.py
        # prettify throws exception

        # Set a valid frum date, thru date still empty
        view.set_thru('2001')

        # See above not re 00/00 default
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'From, Thru dates required!')

        # Any date set by the user passes thru prettify and so only valid
        # dates need to be tested here.

        # Frum date later than thru date
        view.set_frum('2001')
        view.set_thru('1912')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'From date must precede thru date!')

        view.set_thru('2001')   # 1 month project
        err_msg = self.presenter.validate()
        self.assertIsNone(err_msg)
        self.assertEqual(view.get_frum(), '2001')
        self.assertEqual(view.frum_ctrl.GetValue(), '01/20')
        self.assertEqual(view.get_thru(), '2001')
        self.assertEqual(view.thru_ctrl.GetValue(), '01/20')

        view.set_thru('2002')
        err_msg = self.presenter.validate()
        self.assertIsNone(err_msg)
        self.assertEqual(view.get_thru(), '2002')
        self.assertEqual(view.thru_ctrl.GetValue(), '02/20')

    def testValidateProjectFormOnUpdate(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        dbl_click_list_ctrl(list_ctrl, 1)
        self.assertEqual(view.get_name(), 'Prj 298')

        # No project name entered
        view.set_name('')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'Project name required!')

        # Can't steal name from another project
        view.set_name('PRJ299')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'Project name not unique!')

        # Duplicate project name OK since it's the same project
        view.set_name('PRJ298')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, None)

        # Can rename the project with a unique name
        view.set_name('Test Prj 1')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, None)

        # No project full name entered
        view.set_full_name('')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'Project full name required!')

        # Can't steal full name from another project
        view.set_full_name('PRJFULLNAME309')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'Project full name not unique!')

        # Duplicate project frull name OK since it's the same project
        view.set_full_name('prjfullname298')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, None)

        # Can rename the project with a unique name
        view.set_full_name('Test Project One')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, None)

        # User enters 00/00
        view.frum_ctrl.SetValue('0000')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'From, Thru dates required!')

        # Bogus and empty from, thru dates tested in test_month_lib.py
        # prettify throws exception

        # Set a valid frum date, thru date still empty
        view.set_thru('2001')

        # See above not re 00/00 default
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'From, Thru dates required!')

        # Any date set by the user passes thru prettify and so only valid
        # dates need to be tested here.

        # Frum date later than thru date
        view.set_frum('2001')
        view.set_thru('1912')
        err_msg = self.presenter.validate()
        self.assertEqual(err_msg, 'From date must precede thru date!')

        # TODO: test for dates outside assignment dates

        view.set_thru('2001')   # 1 month project
        err_msg = self.presenter.validate()
        self.assertIsNone(err_msg)
        self.assertEqual(view.get_frum(), '2001')
        self.assertEqual(view.frum_ctrl.GetValue(), '01/20')
        self.assertEqual(view.get_thru(), '2001')
        self.assertEqual(view.thru_ctrl.GetValue(), '01/20')

        view.set_thru('2002')
        err_msg = self.presenter.validate()
        self.assertIsNone(err_msg)
        self.assertEqual(view.get_thru(), '2002')
        self.assertEqual(view.thru_ctrl.GetValue(), '02/20')

    # This test has all valid data. See above invalid tests
    def testAddPrj(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        self.assertEqual(view.list_ctrl.GetItemCount(), 8)
        self.assertIsNone(gbl.dataset.get_prj_rec(316))

        click_button(view.clear_btn)

        view.set_name('Test Prj 5')
        view.set_full_name('Test Project Five')
        view.set_frum('1911')
        view.set_thru('2004')
        view.set_pi('WILLIAMS,THEODORE')
        view.set_pm('RUTH,GEORGE HERMAN')
        view.set_notes('This is a comment.')

        with patch('lib.ui_lib.show_msg') as mock_popup:
            mock_popup.return_value = True
            with patch('dal.dao.Dao._Dao__write') as mock_write:
                mock_write.return_value = 316
                click_button(view.save_btn)

        # Check the call to the DB
        self.assertEqual(mock_write.call_count, 1)
        args, kwargs = mock_write.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 0)
        sql = ("INSERT INTO projects "
               "(name,full_name,frum,thru,investigator_id,manager_id,notes,active) "
               "VALUES (?,?,?,?,?,?,?,?)")
        vals = [
            'Test Prj 5', 'Test Project Five',
            '1911', '2004',
            9, 3, 'This is a comment.', 1
        ]
        self.assertEqual(args[0], sql)
        self.assertEqual(args[1], vals)

        # Check model and list have been updated
        model = gbl.dataset.get_prj_rec(316)
        item = view.get_selection()
        self.assertEqual(model, item)
        self.assertEqual(view.list_ctrl.GetItemCount(), 9)
        item_idx = view.get_selected_idx()
        self.assertEqual(list_ctrl.GetItemText(item_idx, 1), '11/19')
        self.assertEqual(list_ctrl.GetItemText(item_idx, 2), '04/20')

        # No assignments
        self.assertEqual(asn_list_ctrl.GetItemCount(), 0)

        mock_popup.assert_called_once_with('Project added!', 'Hallelujah!')

    # This test has all valid data. See above invalid tests
    def testUpdatePrj(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        self.assertEqual(view.list_ctrl.GetItemCount(), 8)

        # Select a project
        model_idx = 4
        click_list_ctrl(list_ctrl, model_idx)

        prj = model[model_idx]
        self.assertEqual(view.get_selection(), prj)
        self.assertEqual(list_ctrl.GetItemText(model_idx, 1), '08/19')
        self.assertEqual(list_ctrl.GetItemText(model_idx, 2), '09/20')

        self.assertEqual(view.get_save_button_label(), 'Update Project')

        # Check the details form
        expected = {
            'name': 'Prj 309',
            'full_name': 'Prj Full Name 309',
            'frum': '1908',
            'thru': '2009',
            'pi': gbl.dataset.get_emp_rec(9),
            'pm': gbl.dataset.get_emp_rec(32),
            'notes': 'Note 309'
        }
        self.assertEqual(self.presenter.get_form_values(), expected)
        self.assertEqual(view.frum_ctrl.GetValue(), '08/19')
        self.assertEqual(view.thru_ctrl.GetValue(), '09/20')

        # Check the assignments list
        self.assertEqual(asn_list_ctrl.GetObjects(), prj.asns)
        self.assertEqual(asn_list_ctrl.GetItemText(0, 1), '10/19')
        self.assertEqual(asn_list_ctrl.GetItemText(0, 2), '09/20')
        self.assertEqual(asn_list_ctrl.GetItemText(1, 1), '02/20')
        self.assertEqual(asn_list_ctrl.GetItemText(1, 2), '09/20')
        self.assertEqual(asn_list_ctrl.GetItemText(2, 1), '02/20')
        self.assertEqual(asn_list_ctrl.GetItemText(2, 2), '02/20')

        # Edit the form
        view.set_name('Test Prj 5')
        view.set_full_name('Test Project Five')
        view.set_frum('1905')
        view.set_thru('2009')
        view.set_pi('MAYS,WILLIE HOWARD JR')
        view.set_pm('RUTH,GEORGE HERMAN')
        view.set_notes('This is a comment.')

        # Mock the save
        with patch('lib.ui_lib.show_msg') as mock_popup:
            mock_popup.return_value = True
            with patch('dal.dao.Dao._Dao__write') as mock_write:
                mock_write.return_value = 1
                click_button(view.save_btn)

        # Check the SQL
        self.assertEqual(mock_write.call_count, 1)
        args, kwargs = mock_write.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 0)
        sql = ("UPDATE projects "
               "SET name=?,full_name=?,frum=?,thru=?,notes=?,investigator_id=?,manager_id=? "
               "WHERE id=?;")
        vals = [
            'Test Prj 5', 'Test Project Five',
            '1905', '2009',
            'This is a comment.',
            24, 3, 309
        ]
        self.assertEqual(args[0], sql)
        self.assertEqual(args[1], vals)

        # Check model and list have been updated
        updated_prj = gbl.dataset.get_prj_rec(309)
        item = view.get_selection()
        self.assertEqual(updated_prj, item)
        self.assertEqual(view.list_ctrl.GetItemCount(), 8)
        item_idx = view.get_selected_idx()
        self.assertEqual(list_ctrl.GetItemText(item_idx, 1), '05/19')
        self.assertEqual(list_ctrl.GetItemText(item_idx, 2), '09/20')

        # Check assignments
        self.assertEqual(asn_list_ctrl.GetItemCount(), 3)
        self.assertEqual(prj.asns, updated_prj.asns)
        self.assertEqual(updated_prj.asns, asn_list_ctrl.GetObjects())

        mock_popup.assert_called_once_with('Project updated!', 'Hallelujah!')

    # This time update with no name, full name change and no PI or PM
    def testUpdatePrj2(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        self.assertEqual(view.list_ctrl.GetItemCount(), 8)

        # Select a project
        model_idx = 4
        click_list_ctrl(list_ctrl, model_idx)

        prj = gbl.dataset.get_prj_rec(309)
        self.assertEqual(view.get_selection(), prj)
        self.assertEqual(list_ctrl.GetItemText(model_idx, 1), '08/19')
        self.assertEqual(list_ctrl.GetItemText(model_idx, 2), '09/20')

        self.assertEqual(view.get_save_button_label(), 'Update Project')

        # Check the details form
        expected = {
            'name': 'Prj 309',
            'full_name': 'Prj Full Name 309',
            'frum': '1908',
            'thru': '2009',
            'pi': gbl.dataset.get_emp_rec(9),
            'pm': gbl.dataset.get_emp_rec(32),
            'notes': 'Note 309'
        }
        self.assertEqual(self.presenter.get_form_values(), expected)
        self.assertEqual(view.frum_ctrl.GetValue(), '08/19')
        self.assertEqual(view.thru_ctrl.GetValue(), '09/20')

        # Check the assignments list
        self.assertEqual(asn_list_ctrl.GetObjects(), prj.asns)
        self.assertEqual(asn_list_ctrl.GetItemText(0, 1), '10/19')
        self.assertEqual(asn_list_ctrl.GetItemText(0, 2), '09/20')
        self.assertEqual(asn_list_ctrl.GetItemText(1, 1), '02/20')
        self.assertEqual(asn_list_ctrl.GetItemText(1, 2), '09/20')
        self.assertEqual(asn_list_ctrl.GetItemText(2, 1), '02/20')
        self.assertEqual(asn_list_ctrl.GetItemText(2, 2), '02/20')

        # Edit the form
        view.set_frum('1905')
        view.set_thru('2009')
        view.set_pi(None)
        view.set_pm(None)
        view.set_notes('This is a comment.')

        # Mock the save
        with patch('lib.ui_lib.show_msg') as mock_popup:
            mock_popup.return_value = True
            with patch('dal.dao.Dao._Dao__write') as mock_write:
                mock_write.return_value = 1
                click_button(view.save_btn)

        # Check the SQL
        self.assertEqual(mock_write.call_count, 1)
        args, kwargs = mock_write.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 0)
        sql = ("UPDATE projects "
               "SET frum=?,thru=?,notes=?,investigator_id=?,manager_id=? "
               "WHERE id=?;")
        vals = [
            '1905', '2009',
            'This is a comment.',
            None, None, 309
        ]
        self.assertEqual(args[0], sql)
        self.assertEqual(args[1], vals)

        # Check model and list have been updated
        model = gbl.dataset.get_prj_rec(309)
        item = view.get_selection()
        self.assertEqual(model, item)
        self.assertEqual(view.list_ctrl.GetItemCount(), 8)
        item_idx = view.get_selected_idx()
        self.assertEqual(list_ctrl.GetItemText(item_idx, 1), '05/19')
        self.assertEqual(list_ctrl.GetItemText(item_idx, 2), '09/20')

        # Check assignments
        self.assertEqual(asn_list_ctrl.GetItemCount(), 3)
        self.assertEqual(prj.asns, model.asns)
        self.assertEqual(model.asns, asn_list_ctrl.GetObjects())

        mock_popup.assert_called_once_with('Project updated!', 'Hallelujah!')

    def testDropPrj(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        self.assertEqual(view.list_ctrl.GetItemCount(), 8)
        self.assertEqual(len(model), 8)

        # Select a project
        model_idx = 4
        click_list_ctrl(list_ctrl, model_idx)

        prj = gbl.dataset.get_prj_rec(309)
        self.assertEqual(view.get_selection(), prj)
        self.assertEqual(list_ctrl.GetItemText(model_idx, 1), '08/19')
        self.assertEqual(list_ctrl.GetItemText(model_idx, 2), '09/20')

        self.assertEqual(view.get_save_button_label(), 'Update Project')

        # Check the details form
        expected = {
            'name': 'Prj 309',
            'full_name': 'Prj Full Name 309',
            'frum': '1908',
            'thru': '2009',
            'pi': gbl.dataset.get_emp_rec(9),
            'pm': gbl.dataset.get_emp_rec(32),
            'notes': 'Note 309'
        }
        self.assertEqual(self.presenter.get_form_values(), expected)
        self.assertEqual(view.frum_ctrl.GetValue(), '08/19')
        self.assertEqual(view.thru_ctrl.GetValue(), '09/20')

        # Check the assignments list
        self.assertEqual(asn_list_ctrl.GetObjects(), prj.asns)
        self.assertEqual(asn_list_ctrl.GetItemText(0, 1), '10/19')
        self.assertEqual(asn_list_ctrl.GetItemText(0, 2), '09/20')
        self.assertEqual(asn_list_ctrl.GetItemText(1, 1), '02/20')
        self.assertEqual(asn_list_ctrl.GetItemText(1, 2), '09/20')
        self.assertEqual(asn_list_ctrl.GetItemText(2, 1), '02/20')
        self.assertEqual(asn_list_ctrl.GetItemText(2, 2), '02/20')

        # User changes mind, cancels deletion
        with patch('lib.ui_lib.confirm') as mock_popup:
            mock_popup.return_value = False
            click_button(view.drop_btn)

        mock_popup.assert_called_once_with(view, 'Drop selected project?')

        # Check no change
        self.assertEqual(view.get_selection(), prj)
        self.assertEqual(list_ctrl.GetItemText(model_idx, 1), '08/19')
        self.assertEqual(list_ctrl.GetItemText(model_idx, 2), '09/20')

        self.assertEqual(view.get_save_button_label(), 'Update Project')

        # Check the details form
        expected = {
            'name': 'Prj 309',
            'full_name': 'Prj Full Name 309',
            'frum': '1908',
            'thru': '2009',
            'pi': gbl.dataset.get_emp_rec(9),
            'pm': gbl.dataset.get_emp_rec(32),
            'notes': 'Note 309'
        }
        self.assertEqual(self.presenter.get_form_values(), expected)
        self.assertEqual(view.frum_ctrl.GetValue(), '08/19')
        self.assertEqual(view.thru_ctrl.GetValue(), '09/20')

        # Check the assignments list
        self.assertEqual(asn_list_ctrl.GetObjects(), prj.asns)
        self.assertEqual(asn_list_ctrl.GetItemText(0, 1), '10/19')
        self.assertEqual(asn_list_ctrl.GetItemText(0, 2), '09/20')
        self.assertEqual(asn_list_ctrl.GetItemText(1, 1), '02/20')
        self.assertEqual(asn_list_ctrl.GetItemText(1, 2), '09/20')
        self.assertEqual(asn_list_ctrl.GetItemText(2, 1), '02/20')
        self.assertEqual(asn_list_ctrl.GetItemText(2, 2), '02/20')

        # User confirms deletion
        with patch('lib.ui_lib.confirm') as mock_popup:
            mock_popup.return_value = True
            with patch('dal.dao.Dao._Dao__write') as mock_write:
                mock_write.return_value = 1
                click_button(view.drop_btn)

        # Check the confirmation
        mock_popup.assert_called_once_with(view, 'Drop selected project?')

        # Check the SQL
        self.assertEqual(mock_write.call_count, 1)
        args, kwargs = mock_write.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 0)
        self.assertEqual(args[0], 'UPDATE projects SET active=0 WHERE id=?')
        self.assertEqual(args[1], (309,))

        # Check that project removed from dataset
        # Need to test against new prj model in global dataset
        self.assertEqual(len(gbl.dataset.get_prj_data()), 7)
        self.assertIsNone(gbl.dataset.get_prj_rec(309))

        # Check that project removed from list
        self.assertEqual(view.list_ctrl.GetItemCount(), 7)
        prj_ids = [p.id for p in view.list_ctrl.GetObjects()]
        self.assertNotIn(309, prj_ids)

        # Check that first project is now selected
        model_idx = view.get_selected_idx()
        self.assertEqual(model_idx, 0)

        # Check the details form
        expected = {
            'name': 'Prj 297',
            'full_name': 'Prj Full Name 297',
            'frum': '1901',
            'thru': '1912',
            'pi': gbl.dataset.get_emp_rec(24),
            'pm': gbl.dataset.get_emp_rec(5),
            'notes': 'Note 297'
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check dates displayed properly
        self.assertEqual(view.frum_ctrl.GetValue(), '01/19')
        self.assertEqual(view.thru_ctrl.GetValue(), '12/19')

        # Check the assignments list
        self.assertEqual(asn_list_ctrl.GetObjects(), model[model_idx].asns)
        self.assertEqual(asn_list_ctrl.GetItemText(0, 1), '10/19')
        self.assertEqual(asn_list_ctrl.GetItemText(0, 2), '12/19')
        self.assertEqual(asn_list_ctrl.GetItemText(1, 1), '10/19')
        self.assertEqual(asn_list_ctrl.GetItemText(1, 2), '12/19')

        self.assertEqual(view.get_save_button_label(), 'Update Project')

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
        mock_popup.assert_called_once_with(view, 'Drop selected project?')

        # Check the SQL
        self.assertEqual(mock_write.call_count, 1)
        args, kwargs = mock_write.call_args
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 0)
        self.assertEqual(args[0], 'UPDATE projects SET active=0 WHERE id=?')
        self.assertEqual(args[1], (315,))

        # Check that project removed from dataset
        # Need to test against new prj model in global dataset
        self.assertEqual(len(gbl.dataset.get_prj_data()), 7)
        self.assertIsNone(gbl.dataset.get_prj_rec(315))

        # Check that project removed from list
        self.assertEqual(view.list_ctrl.GetItemCount(), 7)
        prj_ids = [p.id for p in view.list_ctrl.GetObjects()]
        self.assertNotIn(315, prj_ids)

        # Check that first project is now selected
        model_idx = view.get_selected_idx()
        self.assertEqual(model_idx, 0)

        # Check the details form
        expected = {
            'name': 'Prj 297',
            'full_name': 'Prj Full Name 297',
            'frum': '1901',
            'thru': '1912',
            'pi': gbl.dataset.get_emp_rec(24),
            'pm': gbl.dataset.get_emp_rec(5),
            'notes': 'Note 297'
        }
        self.assertEqual(self.presenter.get_form_values(), expected)

        # Check dates displayed properly
        self.assertEqual(view.frum_ctrl.GetValue(), '01/19')
        self.assertEqual(view.thru_ctrl.GetValue(), '12/19')

        # Check the assignments list
        self.assertEqual(asn_list_ctrl.GetObjects(), model[model_idx].asns)
        self.assertEqual(asn_list_ctrl.GetItemText(0, 1), '10/19')
        self.assertEqual(asn_list_ctrl.GetItemText(0, 2), '12/19')
        self.assertEqual(asn_list_ctrl.GetItemText(1, 1), '10/19')
        self.assertEqual(asn_list_ctrl.GetItemText(1, 2), '12/19')

        self.assertEqual(view.get_save_button_label(), 'Update Project')

    def testAddAsnLoadsForm(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        model_idx = 4
        click_list_ctrl(list_ctrl, model_idx)
        self.assertEqual(view.get_selection(), gbl.dataset.get_prj_rec(309))

        with patch('views.asn_dlg.AsnDlg.ShowModal') as mock_modal:
            click_button(view.add_asn_btn)

        mock_modal.assert_called_once()

        asn_view = self.presenter.asn_presenter.view
        self.assertEqual(asn_view.Name, 'AssignmentPanel')

        self.assertEqual(asn_view.owner_lbl.GetLabelText(), 'Prj 309')
        self.assertEqual(asn_view.assignee_lbl.GetLabelText(), 'Employee: ')
        self.assertNotIsInstance(asn_view.assignee, str)
        assignees = [''] + [e.name for e in gbl.dataset.get_emp_data()]
        self.assertEqual(asn_view.assignee.GetItems(), assignees)
        self.assertEqual(asn_view.assignee.CurrentSelection, -1)

        expected = {
            'employee_id': None,
            'project_id': 309,
            'frum': None,
            'thru': None,
            'effort': None,
            'notes': None
        }
        self.assertEqual(self.presenter.asn_presenter.get_form_values(), expected)

    def testEditAsnLoadsForm(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        model_idx = 4
        click_list_ctrl(list_ctrl, model_idx)
        self.assertEqual(view.get_selection(), gbl.dataset.get_prj_rec(309))

        with patch('views.asn_dlg.AsnDlg.ShowModal') as mock_modal:
            dbl_click_list_ctrl(asn_list_ctrl, 2)

        mock_modal.assert_called_once()

        asn_view = self.presenter.asn_presenter.view
        self.assertEqual(asn_view.Name, 'AssignmentPanel')

        self.assertEqual(asn_view.owner_lbl.GetLabelText(), 'Prj 309')
        self.assertEqual(asn_view.assignee_lbl.GetLabelText(), 'Employee: MAYS,WILLIE HOWARD JR')

        expected = {
            'employee_id': 24,
            'project_id': 309,
            'frum': '2002',
            'thru': '2002',
            'effort': '10',
            'notes': 'Yawn'
        }
        self.assertEqual(self.presenter.asn_presenter.get_form_values(), expected)

        self.assertEqual(asn_view.frum_ctrl.GetValue(), '02/20')
        self.assertEqual(asn_view.thru_ctrl.GetValue(), '02/20')

    def testDropAsnNoneSelected(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select project
        model_idx = 4
        click_list_ctrl(list_ctrl, model_idx)
        self.assertEqual(view.get_selection(), gbl.dataset.get_prj_rec(309))

        # Check assignments
        expected = gbl.dataset.get_prj_rec(309).asns
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
        self.assertEqual(view.get_selection(), gbl.dataset.get_prj_rec(309))

        # Check assignments
        expected = gbl.dataset.get_prj_rec(309).asns
        self.assertEqual(asn_list_ctrl.GetObjects(), expected)

        # Select an assignment
        asn_list_ctrl.Select(2)

        with patch('lib.ui_lib.confirm') as mock_popup:
            mock_popup.return_value = False
            click_button(view.drop_asn_btn)

        mock_popup.assert_called_once_with(view, 'Drop selected assignments?')

        # No change in assignments

        self.assertEqual(asn_list_ctrl.GetObjects(), expected)

    def testDropOneAsn(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select project
        model_idx = 4
        click_list_ctrl(list_ctrl, model_idx)
        self.assertEqual(view.get_selection(), gbl.dataset.get_prj_rec(309))

        # Check assignments
        before_asns = [a for a in gbl.dataset.get_prj_rec(309).asns]
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
        self.assertEqual(args[1], [2375])

        # Check gbl.dataset
        after_asns = [a for a in before_asns if a.id != 2375]
        self.assertEqual(asn_list_ctrl.GetObjects(), after_asns)

    def testDropLastAsn(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select project
        model_idx = 4
        click_list_ctrl(list_ctrl, model_idx)
        self.assertEqual(view.get_selection(), gbl.dataset.get_prj_rec(309))

        # Check assignments
        before_asns = [a for a in gbl.dataset.get_prj_rec(309).asns]
        self.assertEqual(asn_list_ctrl.GetObjects(), before_asns)

        # Select an assignment
        asn_list_ctrl.Select(2)

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
        self.assertEqual(args[1], [2382])

        # Check gbl.dataset
        after_asns = [a for a in before_asns if a.id != 2382]
        self.assertEqual(asn_list_ctrl.GetObjects(), after_asns)

    def testDropMultipleAsns(self):
        view, model, list_ctrl, asn_list_ctrl = self.get_vars()

        # Select project
        model_idx = 4
        click_list_ctrl(list_ctrl, model_idx)
        self.assertEqual(view.get_selection(), gbl.dataset.get_prj_rec(309))

        # Check assignments
        before_asns = [a for a in gbl.dataset.get_prj_rec(309).asns]
        self.assertEqual(asn_list_ctrl.GetObjects(), before_asns)

        # Select assignments
        asn_list_ctrl.SelectObjects([before_asns[0], before_asns[2]])

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
        self.assertEqual(args[1], [2365, 2382])

        # Check gbl.dataset
        self.assertEqual(asn_list_ctrl.GetObjects(), [before_asns[1]])
