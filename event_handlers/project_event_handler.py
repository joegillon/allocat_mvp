import wx
import lib.ui_lib as uil


class ProjectEventHandler(object):

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
        view.fullNameCtrl.Bind(wx.EVT_TEXT, self.OnDataFieldUpdated)
        view.frumCtrl.Bind(wx.EVT_TEXT, self.OnDataFieldUpdated)
        view.thruCtrl.Bind(wx.EVT_TEXT, self.OnDataFieldUpdated)

        view.clearBtn.Bind(wx.EVT_BUTTON, self.OnClear)
        view.saveBtn.Bind(wx.EVT_BUTTON, self.OnSave)
        view.dropBtn.Bind(wx.EVT_BUTTON, self.OnDrop)

        view.addAsnBtn.Bind(wx.EVT_BUTTON, self.OnAsnAdd)
        view.dropAsnBtn.Bind(wx.EVT_BUTTON, self.OnAsnDrop)
        view.asnListCtrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnAsnListDblClick)

    def OnFltr(self, evt):
        ctrl = evt.EventObject.Parent.Name
        c = chr(evt.GetUnicodeKey())
        target = evt.EventObject.GetValue()
        self.presenter.applyFilter(ctrl, c, target)
        evt.Skip()

    def OnFltrCancel(self, evt):
        self.presenter.cancelFilter(evt.EventObject)
        evt.Skip()

    def OnHelpClick(self, evt):
        self.presenter.showHelp()

    def OnClear(self, evt):
        self.presenter.clear()

    def OnSave(self, evt):
        self.presenter.save()

    def OnDrop(self, evt):
        if uil.confirm(self.view, 'Drop selected project?'):
            self.presenter.drop()

    def OnListSelect(self, evt):
        self.presenter.loadDetails()

    def OnAsnAdd(self, evt):
        self.presenter.addAsn()

    def OnAsnDrop(self, evt):
        self.presenter.dropAsn()

    def OnAsnListDblClick(self, evt):
        self.presenter.editAsn(evt.EventObject.GetSelectedObject())

    def OnDataFieldUpdated(self, evt):
        self.presenter.dataFieldUpdated()
