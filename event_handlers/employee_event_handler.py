import wx
from event_handlers.event_handler import EventHandler


class EmployeeEventHandler(EventHandler):

    def bind_form_events(self, view):
        view.fteCtrl.Bind(wx.EVT_TEXT, self.OnDataFieldUpdated)
        view.investigatorCtrl.Bind(wx.EVT_TEXT, self.OnDataFieldUpdated)
