import ObjectListView as olv
import globals as gbl
import lib.ui_lib as uil
from dal.dao import Dao
from views.asn_dlg import AsnDlg
from models.assignment import Assignment

# These imports are needed for the klass bit
from models.project import Project
from models.employee import Employee


class Presenter(object):

    def __init__(self, get_model, view, actor, model_name):
        self.model = None
        self.get_model = get_model
        self.model_name = model_name
        self.view = view
        actor.install(self, view, model_name)
        self.is_listening = True
        gbl.dataset.bind_to('assignments', self.refresh_asn_list)

    def init_view(self, ):
        self.load_view()

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

    def refresh_list(self, idx=None):
        self.model = self.get_model()
        self.view.set_list(self.model)

        if idx:
            self.set_selection(idx)
        else:
            self.set_selection(0)

    def toggle_active(self):
        lbl_txt = self.view.get_active_button_label()
        if lbl_txt == 'Active':
            gbl.dataset.set_active_only(True)
            self.view.set_active_button_label('All')
        else:
            gbl.dataset.set_active_only(False)
            self.view.set_active_button_label('Active')
        self.refresh_list()

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
        self.view.set_save_button_label('Add ' + self.model_name)

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

    def get_new_model_values(self, form_values):
            raise NotImplementedError("Please Implement this method")

    def update_model(self, form_values):
        model = self.model[self.view.get_selected_idx()]
        try:
            model.update(Dao(), form_values)
        except Exception as ex:
            uil.show_error(str(ex))
            return

    def update_model_values(self, model, form_values):
            raise NotImplementedError("Please Implement this method")

    def drop(self, action):
        idx = self.view.get_selected_idx()

        if action == 'Undrop':
            self.undrop(idx)
            return

        try:
            self.model[idx].drop(Dao())
        except Exception as ex:
            uil.show_error(str(ex))
            return

    def undrop(self, idx):
        try:
            self.model[idx].undrop(Dao())
            self.model[idx].active = 1
            self.model[idx].asns = []
        except Exception as ex:
            uil.show_error(str(ex))
            return

        self.refresh_list()
        if idx >= len(self.model):
            idx = len(self.model) - 1
        self.set_selection(idx)

        self.view.set_details_active(True, self.model_name)

    def refresh_asn_list(self):
        me = self.view.get_selection()
        self.view.set_asn_list(me.asns)

    def set_asn_selection(self, idx):
        self.view.set_selection(idx)

    def get_asn_selection(self):
        return self.view.get_selection()

    def add_asn(self):
        idx = self.view.get_selected_idx()
        owner = self.model[idx]
        assignee = self.get_assignee_ctrl()
        dlg = AsnDlg(self.view, -1, 'New Assignment', owner, assignee)
        self.asn_presenter = dlg.presenter
        dlg.ShowModal()
        dlg.Destroy()

    def get_assignee_ctrl(self):
            raise NotImplementedError("Please Implement this method")

    def edit_asn(self, asn):
        idx = self.view.get_selected_idx()
        owner = self.view.get_selection()
        assignee = self.get_assignee_str(asn)
        dlg = AsnDlg(self.view, -1, 'Assignment Details', owner, assignee, asn)
        self.asn_presenter = dlg.presenter
        dlg.ShowModal()
        dlg.Destroy()

    def get_assignee_str(self, asn):
            raise NotImplementedError("Please Implement this method")

    def drop_asn(self):
        selections = self.view.get_selected_asns()
        ids = [x.id for x in selections]
        if not ids:
            uil.show_error('No assignments selected!')
            return

        if uil.confirm(self.view, 'Drop selected assignments?'):
            try:
                Assignment.drop_many(Dao(), ids)
            except Exception as ex:
                uil.show_error(str(ex))
                return

    def show_help(self):
        import lib.ui_lib as uil

        uil.show_list_help()

