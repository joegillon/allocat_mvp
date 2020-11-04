import wx


class ImportInteractor(object):

    def install(self, presenter, view):
        self.presenter = presenter

        view.import_btn.Bind(wx.EVT_BUTTON, self.on_import_click)
        view.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_list_select)
        view.update_allocat_btn.Bind(wx.EVT_BUTTON, self.on_update_allocat_click)
        view.match_btn.Bind(wx.EVT_BUTTON, self.on_match_click)
        view.no_match_btn.Bind(wx.EVT_BUTTON, self.on_no_match_click)

    def on_import_click(self, evt):
        self.presenter.import_data()

    def on_list_select(self, evt):
        self.presenter.load_mismatch_list()

    def on_update_allocat_click(self, evt):
        self.presenter.update_allocat()

    def on_match_click(self, evt):
        self.presenter.match()

    def on_no_match_click(self, evt):
        self.presenter.no_match()
