import wx


class SharedInteractor(object):

    def Install(self, presenter, view):
        self.presenter = presenter
        self.view = view

        view.theList.Bind(wx.EVT_LISTBOX, self.OnReloadNeeded)
        view.addBtn.Bind(wx.EVT_BUTTON, self.onAddBtnClick)
        view.nameCtrl.Bind(wx.EVT_TEXT, self.OnDataFieldUpdated)
        view.nicknameCtrl.Bind(wx.EVT_TEXT, self.OnDataFieldUpdated)
        view.frumCtrl.Bind(wx.EVT_TEXT, self.OnDataFieldUpdated)
        view.thruCtrl.Bind(wx.EVT_TEXT, self.OnDataFieldUpdated)

        view.clearBtn.Bind(wx.EVT_BUTTON, self.OnClear)
        view.saveBtn.Bind(wx.EVT_BUTTON, self.OnSave)
        view.dropBtn.Bind(wx.EVT_BUTTON, self.OnDrop)

    def OnClear(self, evt):
        self.presenter.clear()

    def OnSave(self, evt):
        self.presenter.save()

    def OnDrop(self, evt):
        self.presenter.drop()

    def OnReloadNeeded(self, evt):
        self.presenter.loadView()

    def OnDataFieldUpdated(self, evt):
        self.presenter.dataFieldUpdated()
