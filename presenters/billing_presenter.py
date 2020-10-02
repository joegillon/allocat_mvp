from views.billing_panel import BillingPanel
import globals as gbl
import lib.excel_lib as xl
from models.billing_record import BillingRecord
from event_handlers.billing_event_handler import BillingInteractor


MTH_PATTERN = r"^[A-Z][a-z]+ FY[0-9]{2}$"
QTR_PATTERN = r"^[A-Z][a-z]+ FY[0-9]{2}$"


class BillingPresenter(object):

    def __init__(self, panel=None):
        # No panel is for testing
        if panel:
            self.view = BillingPanel(panel)
            self.model = gbl.dataset
            actor = BillingInteractor()
            actor.install(self, self.view)
            self.init_view()

    def init_view(self):
        pass

    def import_spreadsheet(self):
        file = xl.get_file(self.view)
        if not file:
            return

        wb = xl.open_wb(file)
        sh = xl.get_latest_sheet(wb)

        rex = []
        nrows = sum(1 for _ in sh.get_rows())
        for rownum in range(0, nrows):
            if sh.cell_value(rownum, 1).startswith('506'):
                rex.append(BillingRecord(sh.row_values(rownum)))

        self.update_ledger(rex)

    def update_ledger(self, new_rex):
        from dal.dao import Dao
        from models.ledger import Ledger

        dao = Dao(stateful=True)
        for new_rec in new_rex:
            old_rec = Ledger.get_rec_by_invoice(dao, new_rec.invoice_num)
            old_rec.balance = old_rec.balance - new_rec.balance
            if old_rec.balance == 0.0:
                old_rec.paid = True
            old_rec.update(dao)

        dao.close()

        self.view.update()
