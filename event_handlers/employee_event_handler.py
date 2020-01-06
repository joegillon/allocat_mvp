import wx
from event_handlers.event_handler import EventHandler


class EmployeeEventHandler(EventHandler):

    def bind_form_events(self, view):
        view.fte_ctrl.Bind(wx.EVT_TEXT, self.OnDataFieldUpdated)
        view.investigator_ctrl.Bind(wx.EVT_TEXT, self.OnDataFieldUpdated)
