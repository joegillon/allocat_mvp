import wx
from event_handlers.event_handler import EventHandler


class ProjectEventHandler(EventHandler):

    def bind_form_events(self, view):
        view.full_name_ctrl.Bind(wx.EVT_TEXT, self.OnDataFieldUpdated)
        view.frum_ctrl.Bind(wx.EVT_TEXT, self.OnDataFieldUpdated)
        view.thru_ctrl.Bind(wx.EVT_TEXT, self.OnDataFieldUpdated)
