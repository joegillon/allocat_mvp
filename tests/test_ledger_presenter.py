import unittest
import unittest.mock
from unittest.mock import patch
from tests.helpers import *
import globals as gbl
from models.ledger_dataset import LedgerDataSet
from models.invoice import Invoice
from presenters.ledger_presenter import LedgerPresenter
import tests.ledger_data.test_data as test_data


class TestLedgerPresenter(unittest.TestCase):

    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None)

        gbl.COLOR_SCHEME = gbl.SKINS[gbl.pick_scheme()]

        gbl.dataset = LedgerDataSet(None)

    def tearDown(self):
        self.frame.Destroy()
        self.app.Destroy()

    def testInitView(self):
        # verify global dataset set populated
        self.assertEqual(gbl.dataset.get_ledger_data(), test_data.ledger_objs)

    # def testImportSpreadsheet(self):
    #
    #     with patch('lib.excel_lib.get_file') as mock_get_file_dlg:
    #         mock_get_file_dlg.return_value = 'c:/bench/allocat/data/test_vista_billing.xls'
    #         with patch('presenters.ledger_presenter.LedgerPresenter.get_billing_month') as mock_popup:
    #             mock_popup.return_value = 'April FY20'
    #             click_button(self.view.update_entries_btn)
    #
    #     mock_get_file_dlg.assert_called_once_with(self.presenter.view)
    #
    #     sheet_names = [
    #         'May FY20', 'April FY20', 'March FY20', 'February FY20', 'January FY20',
    #         'December FY20', 'November FY20', 'October FY20', '4th QTR FY19', '3rd QTR FY19',
    #         '2nd QTR FY19', '1st QTR FY19', '4th QTR FY18', '3rd QTR FY18', '2nd QTR FY18',
    #         '1st QTR FY18'
    #     ]
    #     mock_popup.assert_called_once_with(sheet_names)
    #
    # def testImportSS(self):
    #     self.presenter.import_spreadsheet()
    #     pass
