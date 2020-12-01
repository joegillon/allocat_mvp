import wx
import wx.lib.newevent
from collections import namedtuple
import globals as gbl
from lib.custom_button import CustomButton

ColDef = namedtuple('ColDef', 'hdr just width fldName stringConverter')
TabDef = namedtuple('TabDef', 'tblName srchFld colDefs dal dlg')


def get_toolbar_label(panel, text):
    font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                   wx.FONTWEIGHT_BOLD)

    lbl = wx.StaticText(panel, wx.ID_ANY, text)
    lbl.SetFont(font)
    lbl.SetForegroundColour('white')
    return lbl


def toolbar_button(panel, label):
    btn = CustomButton(panel, wx.ID_ANY, label)
    font_normal = wx.Font(10,
                          wx.FONTFAMILY_DEFAULT,
                          wx.FONTSTYLE_NORMAL,
                          wx.FONTWEIGHT_BOLD)
    font_hover = wx.Font(10,
                         wx.FONTFAMILY_DEFAULT,
                         wx.FONTSTYLE_NORMAL,
                         wx.FONTWEIGHT_NORMAL)
    btn.set_font(font_normal, hover=font_hover)
    btn.set_foreground_color('#ffffff')
    btn.set_bg_color(gbl.COLOR_SCHEME.btnBg)
    btn.set_cursor(wx.Cursor(wx.CURSOR_HAND))
    if gbl.COLOR_SCHEME.btnGrd:
        btn.set_bg_gradient(gbl.COLOR_SCHEME.btnGrd)
    btn.set_border((1, 'white', 1))
    btn.set_padding((5, 10, 5, 10))

    return btn


def get_month_ctrl(panel, value):
    import wx.lib.masked as masked

    ctl = masked.TextCtrl(panel, -1, mask='##/##',
                          size=(50, -1),
                          formatcodes='0>')
    ctl.SetFont(wx.Font(9, 70, 90, 90))
    return ctl


def get_help_btn(parent):
    bmp = wx.Bitmap('images/question.png', wx.BITMAP_TYPE_ANY)
    return wx.BitmapButton(parent, wx.ID_ANY, bitmap=bmp,
                           size=(bmp.GetWidth() + 5,
                                 bmp.GetHeight() + 5))


def show_list_help():
    msg = ("Left click to select item.\n"
           "Ctrl-left click to select multiple separate items.\n"
           "Shift-left click to select multiple contiguous items.\n"
           "Right click to see Notes.\n"
           "Double click to edit.")
    wx.MessageBox(msg, 'Help', wx.OK | wx.ICON_INFORMATION)


def show_error(msg):
    wx.MessageBox(msg, 'Oops!', wx.OK | wx.ICON_ERROR)


def show_msg(msg, caption):
    wx.MessageBox(msg, caption, wx.OK)


def confirm(parent, msg):
    dlg = wx.MessageDialog(parent, msg, 'Just making sure...',
                           wx.YES_NO | wx.ICON_QUESTION)
    reply = dlg.ShowModal()
    dlg.Destroy()
    return reply == wx.ID_YES


class ObjComboBox(wx.ComboBox):
    def __init__(self, parent, choices, display_fld, name, style=None):
        wx.ComboBox.__init__(self, parent, wx.ID_ANY, style=style, name=name)

        self.set_choices(choices, display_fld)
        self.SetLabelText(name + ': ')

    def set_choices(self, choices, display_fld):
        self.Clear()
        self.Append('')     # Without this can't SetValue to ''
        i = 1
        for choice in choices:
            self.Append(getattr(choice, display_fld))
            self.SetClientObject(i, choice)
            i += 1

    def get_selection_id(self):
        selection = self.get_selection()
        if selection:
            return selection.id
        else:
            return None

    def set_selection(self, text):
        if self.Count == 1:
            return
        x = text if text else ''
        self.Select(self.GetItems().index(x))
        self.SetValue(x)

    def get_selection(self):
        if self.CurrentSelection == -1:
            return None
        return self.GetClientData(self.GetSelection())


def display_value(obj, attr):
    if not obj or not obj[attr]:
        return ''
    return obj[attr]


def toYN(value):
    return 'Y' if value else 'N'


def set2compare(s):
    import string

    return s.translate({ord(c): None for c in string.whitespace}).upper()


class UpperTextCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        super(UpperTextCtrl, self).__init__(*args, **kwargs)
        self.Bind(wx.EVT_TEXT, self.on_text)

    def on_text(self, event):
        event.Skip()
        selection = self.GetSelection()
        value = self.GetValue().upper()
        self.ChangeValue(value)
        self.SetSelection(*selection)


class RadioGroup(wx.BoxSizer):
    def __init__(self, parent, lbl_text, options):
        super(RadioGroup, self).__init__()
        self.SetOrientation(wx.HORIZONTAL)

        lbl = get_toolbar_label(parent, lbl_text)
        self.Add(lbl, 0, wx.ALL, 5)

        self.buttons = []
        for option in options:
            lbl = get_toolbar_label(parent, option)
            lbl.SetForegroundColour(wx.Colour(gbl.COLOR_SCHEME.tbFg))
            lbl.SetFont(lbl.GetFont().MakeBold())
            btn = wx.RadioButton(parent, wx.ID_ANY, style=wx.RB_GROUP,
                                 name=option)
            btn.SetValue(False)
            btn.Bind(wx.EVT_RADIOBUTTON, self.on_button_select)
            self.Add(lbl, 0, wx.ALL, 5)
            self.Add(btn, 0, wx.ALL, 5)
            self.buttons.append(btn)

    def on_button_select(self, evt):
        self.clear()
        btn_name = evt.EventObject.GetName()
        selected_button = next((b for b in self.buttons if b.GetName() == btn_name), None)
        selected_button.SetValue(True)

    def get_selection(self):
        for button in self.buttons:
            if button.GetValue():
                return self.buttons.index(button)
        return -1

    def clear(self):
        for button in self.buttons:
            button.SetValue(False)

    def set_selection(self, idx, value):
        self.clear()
        self.buttons[idx].SetValue(value)


def to_money(value):
    if type(value) == int:
        return format(value, ',d')
    return format(float(value), ',.2f')


def frum_money(value):
    return value.replace(',', '')


def clear_panel(panel):
    from wx._core import TextCtrl
    import ObjectListView as olv

    for ctrl in list(panel.Children):
        if isinstance(ctrl, TextCtrl):
            ctrl.SetValue('')
        elif isinstance(ctrl, ObjComboBox):
            ctrl.Select(0)
        elif isinstance(ctrl, olv.ObjectListView):
            ctrl.DeleteAllItems()
