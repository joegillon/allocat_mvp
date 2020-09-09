from views.email_panel import EmailPanel

class EmailPresenter(object):

    def __init__(self, panel):
        self.model = None
        self.view = EmailPanel(panel)
        self.actor = None
