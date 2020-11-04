import wx
import globals as gbl
import lib.ui_lib as uil
import lib.excel_lib as xl
from dal.dao import Dao
from models.employee import Employee
from views.import_panel import ImportPanel
from event_handlers.import_event_handler import ImportInteractor


class ImportPresenter(object):

    def __init__(self, panel):
        self.model = None
        self.view = ImportPanel(panel)
        actor = ImportInteractor()
        actor.install(self, self.view)

        self.emps = gbl.dataset.get_emp_data()
        # self.ss_rex = []
        self.mismatches = []

    def import_data(self):
        file = xl.get_file(self.view)
        wb = xl.open_wb(file)
        sheet = wb.sheet_by_index(0)
        ss_rex = self.get_data(sheet)
        self.view.display(ss_rex)
        self.mismatches = self.get_mismatches(ss_rex)

    def get_data(self, sheet):
        from models.spreadsheet_record import SpreadsheetRecord

        rows = xl.get_sheet_data(sheet)
        return [SpreadsheetRecord({
            'name': fld['Name'],
            'salary': fld['Salary'],
            'fringe': round(fld['Fringe %'], 3),
            'step_date': xl.to_date(fld['Step Sched. '])
        }) for fld in rows]

    def get_mismatches(self, ss_rex):
        from fuzzywuzzy import process

        emp_names = [e.name.upper() for e in self.emps]
        mismatches = {}
        for rec in ss_rex:
            matches = process.extract(rec.name, emp_names)
            if matches[0][1] == 100:
                rec.matched = True
            else:
                rec.matched = False
                mismatches[rec.name] = matches

        return mismatches

    def load_mismatch_list(self):
        obj = self.view.get_list_selection()
        if not obj.matched:
            results = []
            for tuple in self.mismatches[obj.name]:
                results.append({'name': tuple[0], 'score': tuple[1]})
            self.view.load_mismatch_list(results)

    def update_allocat(self):
        rex = self.view.get_rex()
        new_rex = []
        for rec in rex:
            new_rec = {
                'id': next((x.id for x in self.emps if x.name == rec.name), None),
                'salary': rec.salary,
                'fringe': rec.fringe
            }
            if not new_rec['id']:
                uil.show_error('Uh oh! No employee record for ' + rec.name)
                return
            new_rex.append(new_rec)

        dao = Dao(stateful=True)
        try:
            Employee.update_salaries(dao, new_rex)
            uil.show_msg('Hurray!', 'Done!')
        except Exception as e:
            uil.show_error(str(e))
        finally:
            dao.close()

    def match(self):
        match, idx = self.view.get_match_selection()
        if not match:
            uil.show_error('No match selected!')
            return

        if idx != 0:
            if not uil.confirm(self.view, 'Not the highest score! Are you sure?'):
                return

        objs = self.view.get_list()
        selection = self.view.get_list_selection()
        selection.matched = True
        self.view.display(objs)
        try:
            result = Employee.update_name(Dao(),
                                          match['name'], selection.name)
        except Exception as e:
            uil.show_error(str(e))

    def no_match(self):
        match = self.view.get_match_selection()
        if match:
            uil.show_error("But you've selected a match!")
            self.view.set_match_selection(match)
            return
        selection = self.view.get_list_selection()
        objs = self.view.get_list()
        selection.matched = True
        self.view.display(objs)
        try:
            result = Employee.add_name(Dao(), selection.name)
        except Exception as e:
            uil.show_error(str(e))
