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


def dbl_click_list_ctrl(ctrl, idx):
    ctrl.Select(idx)
    # evt = wx.ListEvent(wx.EVT_LIST_ITEM_ACTIVATED.typeId)
    # evt.SetEventObject(ctrl)
    # evt.SetId(ctrl.GetId())
    # ctrl.GetEventHandler().ProcessEvent(evt)


def click_multi_list_ctrl(ctrl, objs):
    ctrl.SelectObjects(objs)
    evt = wx.ListEvent(wx.EVT_LIST_ITEM_ACTIVATED.typeId)
    evt.SetEventObject(ctrl)
    evt.SetId(ctrl.GetId())
    ctrl.GetEventHandler().ProcessEvent(evt)


def click_combobox_ctrl(ctrl, idx):
    ctrl.SetSelection(idx)
    evt = wx.ListEvent(wx.EVT_COMBOBOX.typeId)
    evt.SetEventObject(ctrl)
    evt.SetId(ctrl.GetId())
    ctrl.GetEventHandler().ProcessEvent(evt)


def check_checkbox_ctrl(ctrl):
    ctrl.SetValue(True)


def uncheck_checkbox_ctrl(ctrl):
    ctrl.SetValue(False)


def enter_in_textbox_ctrl(ctrl, value):
    ctrl.SetValue(value)


def assertEqualObjects(obj1, obj2):
    for attr in list(vars(obj1)):
        if getattr(obj1, attr) != getattr(obj2, attr):
            return False
    return True
