from views.script_panel import ScriptPanel


class ScriptPresenter(object):

    def __init__(self, panel):
        self.model = None
        self.view = ScriptPanel(panel)
        self.actor = None
