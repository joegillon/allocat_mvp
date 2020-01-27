import wx


def click_button(button):
    evt = wx.CommandEvent(wx.EVT_BUTTON.typeId)
    evt.SetEventObject(button)
    evt.SetId(button.GetId())
    button.GetEventHandler().ProcessEvent(evt)

def click_search_ctrl(ctrl):
    evt = wx.CommandEvent(wx.EVT_SEARCHCTRL_CANCEL_BTN.typeId)
    evt.SetEventObject(ctrl)
    evt.SetId(ctrl.GetId())
    ctrl.GetEventHandler().ProcessEvent(evt)

def click_list_ctrl(ctrl, idx):
    ctrl.Select(idx)
    evt = wx.ListEvent(wx.EVT_LIST_ITEM_ACTIVATED.typeId)
    evt.SetEventObject(ctrl)
    evt.SetId(ctrl.GetId())
    ctrl.GetEventHandler().ProcessEvent(evt)

def click_multi_list_ctrl(ctrl, objs):
    ctrl.SelectObjects(objs)
    evt = wx.ListEvent(wx.EVT_LIST_ITEM_ACTIVATED.typeId)
    evt.SetEventObject(ctrl)
    evt.SetId(ctrl.GetId())
    ctrl.GetEventHandler().ProcessEvent(evt)
