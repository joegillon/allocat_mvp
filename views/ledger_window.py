import wx
import globals as gbl
from presenters.import_presenter import ImportPresenter
from presenters.data_mgt_presenter import DataMgtPresenter
from presenters.ledger_presenter import LedgerPresenter


class LedgerWindow(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self, None, title='allocat ledger', size=(1500, 820))
        self.SetBackgroundColour(gbl.COLOR_SCHEME.pnlBg)

        notebook = wx.Notebook(self)

        self.ledger_presenter = LedgerPresenter(notebook)
        self.import_presenter = ImportPresenter(notebook)
        self.data_mgt_presenter = DataMgtPresenter(notebook)

        self.config_notebook(notebook)

    def config_notebook(self, notebook):
        icon_list = wx.ImageList(32, 32)
        icon_list.Add(wx.Bitmap('images/Billing.png', wx.BITMAP_TYPE_PNG))
        icon_list.Add(wx.Bitmap('images/Import.bmp', wx.BITMAP_TYPE_BMP))
        icon_list.Add(wx.Bitmap('images/Database.png', wx.BITMAP_TYPE_PNG))
        notebook.AssignImageList(icon_list)
        notebook.AddPage(self.ledger_presenter.view, 'Ledger', select=True, imageId=0)
        notebook.AddPage(self.import_presenter.view, 'Import Salaries', imageId=1)
        notebook.AddPage(self.data_mgt_presenter.view, 'Manage Data', imageId=2)
