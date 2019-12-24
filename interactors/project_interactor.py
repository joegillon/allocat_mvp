import wx
import lib.ui_lib as uil


class ProjectInteractor(object):

    def Install(self, presenter, view):
        self.presenter = presenter
        self.view = view

        view.listCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListSelect)
        view.nameFltrCtrl.Bind(wx.EVT_CHAR, self.OnFltr)
        view.nameFltrCtrl.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnFltrCancel)
        view.notesFltrCtrl.Bind(wx.EVT_CHAR, self.OnFltr)
        view.notesFltrCtrl.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnFltrCancel)
        view.helpBtn.Bind(wx.EVT_BUTTON, self.OnHelpClick)

        view.nameCtrl.Bind(wx.EVT_TEXT, self.OnDataFieldUpdated)
        view.nicknameCtrl.Bind(wx.EVT_TEXT, self.OnDataFieldUpdated)
        view.frumCtrl.Bind(wx.EVT_TEXT, self.OnDataFieldUpdated)
        view.thruCtrl.Bind(wx.EVT_TEXT, self.OnDataFieldUpdated)

        view.clearBtn.Bind(wx.EVT_BUTTON, self.OnClear)
        view.saveBtn.Bind(wx.EVT_BUTTON, self.OnSave)
        view.dropBtn.Bind(wx.EVT_BUTTON, self.OnDrop)

        view.addAsnBtn.Bind(wx.EVT_BUTTON, self.OnAsnAdd)

    def OnFltr(self, evt):
        self.presenter.applyFilter(evt)

    def OnFltrCancel(self, evt):
        self.presenter.cancelFilter(evt)

    def OnHelpClick(self, evt):
        self.presenter.showHelp()

    def OnClear(self, evt):
        self.presenter.clear()

    def OnSave(self, evt):
        self.presenter.save()

    def OnDrop(self, evt):
        self.presenter.drop()

    def OnListSelect(self, evt):
        self.presenter.loadDetails()

    def OnAsnAdd(self, evt):
        self.presenter.addAsn()

    def OnDataFieldUpdated(self, evt):
        self.presenter.dataFieldUpdated()
