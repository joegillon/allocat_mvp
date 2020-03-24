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

    def __init__(self, model, view, actor, model_name):
        self.model = model
        self.model_name = model_name
        self.view = view
        actor.install(self, view, model_name)
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
        if gbl.active_only:
            self.view.set_list([model for model in self.model  if model.active])
        else:
            self.view.set_list(self.model)

    def toggle_active(self):
        lbl_txt = self.view.get_active_button_label()
        if lbl_txt == 'Active':
            gbl.active_only = True
            self.view.set_active_button_label('All')
        else:
            gbl.active_only = False
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

        del self.model[idx]
        self.refresh_list()
        if idx >= len(self.model):
            idx = len(self.model) - 1
        self.set_selection(idx)

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
        # self.view.set_drop_asn_btn_lbl('Undrop Assignments')

    def set_asn_selection(self, idx):
        self.view.set_selection(idx)

    def get_asn_selection(self):
        return self.view.get_selection()

    def add_asn(self):
        idx = self.view.get_selected_idx()
        owner = [rec for rec in self.model if rec.active][idx] if gbl.active_only else self.model[idx]
        assignee = self.get_assignee_ctrl()
        dlg = AsnDlg(self.view, -1, 'New Assignment', owner, assignee)
        self.asn_presenter = dlg.presenter
        dlg.ShowModal()
        dlg.Destroy()
        new_asn = gbl.dataset.grab_bag['saved_asn']
        gbl.dataset.asn_rex.append(new_asn)
        owner.asns.append(new_asn)
        self.view.set_asn_list(owner.asns)

    def get_assignee_ctrl(self):
            raise NotImplementedError("Please Implement this method")

    def edit_asn(self, asn):
        idx = self.view.get_selected_idx()
        owner = [rec for rec in self.model if rec.active][idx] if gbl.active_only else self.model[idx]
        # owner = self.model[self.view.get_selected_idx()]
        assignee = self.get_assignee_str(asn)
        dlg = AsnDlg(self.view, -1, 'Assignment Details', owner, assignee, asn)
        self.asn_presenter = dlg.presenter
        dlg.ShowModal()
        dlg.Destroy()
        edited_asn = gbl.dataset.grab_bag['saved_asn']
        self.view.set_asn_list(owner.asns)


    def get_assignee_str(self, asn):
            raise NotImplementedError("Please Implement this method")

    def drop_asn(self):
        model = self.model[self.view.get_selected_idx()]
        selections = self.view.get_selected_asns()
        ids = [x.id for x in selections]
        if not ids:
            uil.show_error('No assignments selected!')
            return

        # if action == 'Undrop':
        #     self.undrop_asn(ids)
        #     return

        if uil.confirm(self.view, 'Drop selected assignments?'):
            try:
                Assignment.drop_many(Dao(), ids)
            except Exception as ex:
                uil.show_error(str(ex))
                return

            new_list = [asn for asn in model.asns if asn.id not in ids]
            model.asns = new_list
            self.view.set_asn_list(new_list)

    # def undrop_asn(self, ids):
    #     if uil.confirm(self.view, 'Undrop selected assignments?'):
    #         try:
    #             Assignment.undrop_many(Dao(), ids)
    #         except Exception as ex:
    #             uil.show_error(str(ex))
    #             return

    def show_help(self):
        import lib.ui_lib as uil

        uil.show_list_help()

