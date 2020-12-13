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
    # evt = wx.ListEvent(wx.EVT_LIST_ITEM_SELECTED.typeId)
    # evt.SetEventObject(ctrl)
    # evt.SetId(ctrl.GetId())
    # ctrl.GetEventHandler().ProcessEvent(evt)


def dbl_click_list_ctrl(ctrl, idx):
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
        val1 = getattr(obj1, attr)
        val2 = getattr(obj2, attr)
        if isinstance(val1, list):
            assertEqualListOfObjects(val1, val2)
        elif val1 != val2:
            msg = "%s: %s != %s" % (attr, str(val1), str(val2))
            assert False, msg

def assertEqualListOfObjects(lst1, lst2):
    if len(lst1) != len(lst2):
        assert False, 'Lists of different lengths!'
    for idx in range(0, len(lst1)):
        assertEqualObjects(lst1[idx], lst2[idx])


def get_grid_header(grid):
    result = []
    for col in range(0, grid.GetNumberCols()):
        result.append(grid.GetColLabelValue(col))
    return result


def get_grid_row(grid, rownum):
    result = []
    for colnum in range(0, grid.GetNumberCols()):
        result.append(grid.GetCellValue(rownum, colnum))
    return result


def grid_to_list(grid):
    hdr = get_grid_header(grid)
    rows = []
    for rownum in range(0, grid.GetNumberRows()):
        rows.append(get_grid_row(grid, rownum))
    return [hdr] + rows


def get_grid_colors(grid):
    rows = []
    for rownum in range(0, grid.GetNumberRows()):
        row = []
        for colnum in range(0, grid.GetNumberCols()):
            row.append(grid.GetCellTextColour(rownum, colnum).RGB)
        rows.append(row)
    return rows

def click_grid_cell(grid, rownum, colnum):
    evt = wx.CommandEvent(wx.grid.EVT_GRID_CELL_LEFT_CLICK.typeId)
    evt.Col = colnum
    evt.Row = rownum
    evt.SetEventObject(grid)
    evt.SetId(grid.GetId())
    grid.GetEventHandler().ProcessEvent(evt)


def get_list_items(lst):
    items = []
    for rownum in range(0, lst.GetItemCount()):
        row = []
        for colnum in range(0, lst.GetColumnCount()):
            row.append(lst.GetItem(rownum, colnum).GetText())
        items.append(row)
    return items
