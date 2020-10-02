import wx
import globals as gbl
from presenters.ledger_presenter import LedgerPresenter
from presenters.import_presenter import ImportPresenter
from presenters.email_presenter import EmailPresenter
from presenters.script_presenter import ScriptPresenter
from presenters.data_mgt_presenter import DataMgtPresenter
from presenters.billing_presenter import BillingPresenter


class LedgerWindow(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self, None, title='allocat ledger', size=(1400, 800))
        self.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)

        notebook = wx.Notebook(self)

        self.ledger_presenter = LedgerPresenter(notebook)
        self.import_presenter = ImportPresenter(notebook)
        # self.billing_presenter = BillingPresenter(notebook)
        self.email_presenter = EmailPresenter(notebook)
        self.script_presenter = ScriptPresenter(notebook)
        self.data_mgt_presenter = DataMgtPresenter(notebook)

        self.config_notebook(notebook)

    def config_notebook(self, notebook):
        icon_list = wx.ImageList(32, 32)
        icon_list.Add(wx.Bitmap('images/Edit page.bmp', wx.BITMAP_TYPE_BMP))
        icon_list.Add(wx.Bitmap('images/Import.bmp', wx.BITMAP_TYPE_BMP))
        icon_list.Add(wx.Bitmap('images/E-mail.bmp', wx.BITMAP_TYPE_BMP))
        icon_list.Add(wx.Bitmap('images/Script.bmp', wx.BITMAP_TYPE_BMP))
        icon_list.Add(wx.Bitmap('images/Database.png', wx.BITMAP_TYPE_PNG))
        # icon_list.Add(wx.Bitmap('images/Billing.png', wx.BITMAP_TYPE_PNG))
        notebook.AssignImageList(icon_list)
        notebook.AddPage(self.ledger_presenter.view, 'Ledger', select=True, imageId=0)
        notebook.AddPage(self.import_presenter.view, 'Import Salaries', imageId=1)
        # notebook.AddPage(self.billing_presenter.view, 'Billing Report', imageId=5)
        notebook.AddPage(self.email_presenter.view, 'Email Approvals', imageId=2)
        notebook.AddPage(self.script_presenter.view, 'Write Script', imageId=3)
        notebook.AddPage(self.data_mgt_presenter.view, 'Manage Data', imageId=4)
