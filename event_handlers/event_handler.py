import wx
import lib.ui_lib as uil


class EventHandler(object):

    def Install(self, presenter, view, model_name):
        self.presenter = presenter
        self.view = view
        self.model_name = model_name

        view.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_list_select)
        view.name_fltr_ctrl.Bind(wx.EVT_CHAR, self.on_filter)
        view.name_fltr_ctrl.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.on_filter_cancel)
        view.notes_fltr_ctrl.Bind(wx.EVT_CHAR, self.on_filter)
        view.notes_fltr_ctrl.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.on_filter_cancel)
        view.help_btn.Bind(wx.EVT_BUTTON, self.on_help_click)

        view.name_ctrl.Bind(wx.EVT_TEXT, self.OnDataFieldUpdated)
        self.bind_form_events(view)

        view.clear_btn.Bind(wx.EVT_BUTTON, self.on_clear)
        view.save_btn.Bind(wx.EVT_BUTTON, self.on_save)
        view.drop_btn.Bind(wx.EVT_BUTTON, self.on_drop)

        view.add_asn_btn.Bind(wx.EVT_BUTTON, self.on_asn_add)
        view.drop_asn_btn.Bind(wx.EVT_BUTTON, self.on_asn_drop)
        view.asn_list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_asn_list_dblclick)

    def bind_form_events(self, view):
        raise NotImplementedError("Please Implement this method")

    def on_filter(self, evt):
        ctrl = evt.EventObject.Parent.Name
        c = chr(evt.GetUnicodeKey())
        target = evt.EventObject.GetValue()
        self.presenter.apply_filter(ctrl, c, target)
        evt.Skip()

    def on_filter_cancel(self, evt):
        self.presenter.cancel_filter(evt.EventObject)
        evt.Skip()

    def on_help_click(self, evt):
        self.presenter.show_help()

    def on_clear(self, evt):
        self.presenter.clear()

    def on_save(self, evt):
        self.presenter.save()

    def on_drop(self, evt):
        if uil.confirm(self.view, 'Drop selected ' + self.model_name + '?' ):
            self.presenter.drop()

    def on_list_select(self, evt):
        self.presenter.load_details()

    def on_asn_add(self, evt):
        self.presenter.addAsn()

    def on_asn_drop(self, evt):
        self.presenter.dropAsn()

    def on_asn_list_dblclick(self, evt):
        self.presenter.editAsn(evt.EventObject.GetSelectedObject())

    def OnDataFieldUpdated(self, evt):
        self.presenter.dataFieldUpdated()
