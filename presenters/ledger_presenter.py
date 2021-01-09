from views.ledger_panel import LedgerPanel
import globals as gbl
import lib.excel_lib as xl
from models.deposit import Deposit
from event_handlers.ledger_event_handler import LedgerEventHandler


MTH_PATTERN = r"^[A-Z][a-z]+ FY[0-9]{2}$"
QTR_PATTERN = r"^[A-Z][a-z]+ FY[0-9]{2}$"


class LedgerPresenter(object):

    def __init__(self, panel=None):
        from tests.ledger_data.test_data import invoices

        if panel:
            self.view = LedgerPanel(panel)
            self.model = gbl.dataset
            actor = LedgerEventHandler()
            actor.install(self, self.view)
            # self.invoices =(gbl.dataset.get_ledger_data())
            self.invoices = invoices
            self.full_total = 0.0
            self.init_view()

    def init_view(self):

        total = 0
        for invoice in self.invoices:
            total += invoice.amount
        self.full_total = total

        self.view.set_total(total)
        self.view.set_unpaid_list(self.invoices)

    def set_total(self, attr):
        if attr == 'All':
            self.view.set_total(self.full_total)
            return

        attr = attr.replace(' ', '_').lower()
        selection = self.view.get_unpaid_list_selection()
        if not selection:
            return
        fltr = getattr(selection, attr)
        total = 0
        for invoice in self.invoices:
            if getattr(invoice, attr) == fltr:
                total += invoice.amount

        self.view.set_total(total)

    def import_spreadsheet(self):
        file = xl.get_file(self.view)
        if not file:
            return

        inv_nums = [inv.invoice_num for inv in self.invoices]

        wb = xl.open_wb(file)
        sh = xl.get_latest_sheet(wb)

        rex = []
        nrows = sum(1 for _ in sh.get_rows())
        for rownum in range(0, nrows):
            if sh.cell_value(rownum, 1).startswith('506'):
                deposit = Deposit(sh.row_values(rownum))
                if deposit.invoice_num not in inv_nums:
                    continue
                invoice = gbl.dataset.get_invoice_rec(deposit.invoice_num)
                s = str(invoice.quarter)
                deposit.fy = s[2:4]
                deposit.qtr = s[4]
                rex.append(deposit)

        self.view.set_deposits_list(rex)

    def update_ledger(self):
        from dal.dao import Dao
        from models.invoice import Invoice

        deposits = self.view.get_deposits_list()

        # dao = Dao(stateful=True)
        removals = []
        for deposit in deposits:
            invoice = gbl.dataset.get_invoice_rec(deposit.invoice_num)
            invoice.balance -= deposit.amount
            if invoice.balance == 0:
                invoice.paid = True
                removals.append(invoice.invoice_num)
        gbl.dataset.remove_invoices(removals)
        self.view.refresh_invoices()
        # dao.close()
