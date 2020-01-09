import ObjectListView as olv
import lib.ui_lib as uil
from dal.dao import Dao

# These imports are needed for the klass bit
from models.project import Project
from models.employee import Employee


class Presenter(object):

    def __init__(self, model, view, actor, model_name):
        self.model = model
        self.model_name = model_name
        self.view = view
        actor.Install(self, view, model_name)
        self.is_listening = True

    def init_view(self, ):
        self.load_view()
        self.set_selection(0)

    def load_view(self):
        if self.is_listening:
            self.is_listening = False
            self.refresh_list()
            self.load_combos()
            self.is_listening = True

    def load_combos(self):
        raise NotImplementedError("Please Implement this method")

    def load_details(self):
        raise NotImplementedError("Please Implement this method")

    def refresh_list(self):
        self.view.set_list(self.model)

    def set_selection(self, idx):
        self.view.set_selection(idx)

    def get_selection(self):
        return self.view.get_selection()

    def apply_filter(self, ctrl, c, target):
        if not c.isalpha():
            if c == '\b':
                target = target[:-1]
        else:
            target += c
        the_list = self.view.list_ctrl
        col = the_list.columns[0:1]
        if ctrl == 'notes_fltr_ctrl':
            col = the_list.columns[4:1]
        the_list.SetFilter(olv.Filter.TextSearch(
            the_list, columns=col, text=target))
        the_list.RepopulateList()
        self.view.set_selection(0)

    def cancel_filter(self, ctrl):
        ctrl.Clear()
        the_list = self.view.list_ctrl
        the_list.SetFilter(None)
        the_list.RepopulateList()
        self.view.set_selection(0)

    def clear(self):
        self.view.clear_selection()
        self.view.set_name('')
        self.clear_model_values()
        self.view.set_notes('')
        self.view.set_asn_list([])
        self.view.set_button_label('Add ' + self.model_name)

    def clear_model_values(self):
        raise NotImplementedError("Please Implement this method")

    def get_form_values(self):
        raise NotImplementedError("Please Implement this method")

    def validate(self):
            raise NotImplementedError("Please Implement this method")

    def save(self):
        err_msg = self.validate()
        if err_msg:
            uil.show_error(err_msg)
            return

        form_values = self.get_form_values()
        if self.view.get_selected_idx() == -1:
            self.add_model(form_values)
        else:
            self.update_model(form_values)

    def add_model(self, form_values):
        klass = globals()[self.model_name]
        new_model = klass(self.get_new_model_values(form_values))

        try:
            new_model.id = new_model.add(Dao())
        except Exception as ex:
            uil.show_error(str(ex))
            return

        self.model.append(new_model)
        self.model = sorted(self.model, key=lambda i: i.name.lower())
        self.refresh_list()
        self.set_selection(self.model.index(new_model))

    def get_new_model_values(self, form_values):
            raise NotImplementedError("Please Implement this method")

    def update_model(self, form_values):
        model = self.model[self.view.get_selected_idx()]
        try:
            model.update(Dao(), form_values)
        except Exception as ex:
            uil.show_error(str(ex))
            return
        self.refresh_list()
        self.set_selection(self.model.index(model))

    def update_model_values(self, model, form_values):
            raise NotImplementedError("Please Implement this method")

    def drop(self):
        idx = self.view.get_selected_idx()

        try:
            self.model[idx].drop(Dao())
        except Exception as ex:
            uil.show_error(str(ex))
            return

        del self.model[idx]
        self.refresh_list()
        if idx >= len(self.model):
            idx = len(self.model) - 1
        self.set_selection(idx)

    # def addAsn(self):
    #     prj = self.view.getSelection()
    #     owner = 'Project: %s' % prj.name
    #     assignee = uil.ObjComboBox(self.view,
    #                            self.employees,
    #                            'name',
    #                            'Employee',
    #                            style=16)
    #
    #     dlg = AsnDlg(self.view, -1, 'New Assignment', owner, assignee)
    #     dlg.ShowModal()
    #
    # def dropAsn(self):
    #     prj = self.view.getSelection()
    #     selections = self.view.getAsnSelections()
    #     ids = [x.id for x in selections]
    #     if not ids:
    #         uil.showError('No assignments selected!')
    #         return
    #     if uil.confirm(self.view, 'Drop selected assignments?'):
    #         new_list = [asn for asn in prj.asns if asn.id not in ids]
    #         prj.asns = new_list
    #         self.view.setAsnList(new_list)
    #
    # def editAsn(self, asn):
    #     prj = self.view.getSelection()
    #     owner = 'Project: %s' % prj.name
    #     assignee = 'Employee: %s' % asn.employee
    #     dlg = AsnDlg(self.view, -1, 'Assignment Details', owner, assignee, asn)
    #     dlg.ShowModal()

    def show_help(self):
        import lib.ui_lib as uil

        uil.show_list_help()

