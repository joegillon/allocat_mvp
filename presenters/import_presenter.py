import wx
import globals as gbl
import lib.ui_lib as uil
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
        self.mismatches = []

    def get_file(self):
        folder = 'c:/bench/allocat/data'
        dlg = wx.FileDialog(self.view, 'Open', folder, '',
                            'Excel files (*.xls;*.xlsx)|*.xls;*.xlsx',
                            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        dlg.ShowModal()
        file = dlg.GetPath()
        dlg.Destroy()
        self.import_file(file)

    def import_file(self, file):
        import lib.excel_lib as xl
        from models.spreadsheet_record import SpreadsheetRecord

        wb = xl.open_wb(file)
        sheet = wb.sheet_by_index(0)
        rex = [SpreadsheetRecord(
                    {'name': rec[0], 'salary': rec[14], 'fringe': round(rec[17], 2)})
                        for rec in sheet._cell_values[1:]]
        self.mismatches = self.get_mismatches(rex)

        self.view.display(rex)

    def get_mismatches(self, ss_rex):
        from fuzzywuzzy import process

        emp_names = [e.name for e in self.emps]
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
        match = self.view.get_match_selection()
        if not match:
            uil.show_error('No match selected!')
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
