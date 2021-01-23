class LedgerDataSet(object):

    def __init__(self, db_path):
        self.db_path = db_path

        self._emp_rex = []
        self._asn_rex = []
        self._dept_rex = []
        self._grant_admin_rex = []
        self._invoices_sent = []
        self._invoices_unsent = []

        self.build_dataset()

    def _get_data(self):
        from dal.dao import Dao
        # from tests.ledger_data.test_data import invoices

        from models.employee import Employee
        from models.department import Department
        from models.grant_admin import GrantAdmin
        from models.invoice import Invoice
        from models.assignment import Assignment

        dao = Dao(db_path=self.db_path, stateful=True)
        self._emp_rex = Employee.get_all(dao)
        self._dept_rex = Department.get_all(dao)
        self._grant_admin_rex = GrantAdmin.get_all(dao)
        invoices_unpaid = Invoice.get_rex(dao)
        self._invoices_sent = [invoice for invoice in invoices_unpaid if invoice.sent]
        self._invoices_unsent = [invoice for invoice in invoices_unpaid if not invoice.sent]
        self._asn_rex = Assignment.get_billables(dao)
        dao.close()

    def build_dataset(self):
        self._get_data()

    def get_emp_data(self):
        return self._emp_rex

    def get_emp_rec(self, id):
        return next((rec for rec in self._emp_rex if rec.id == id), None)

    def get_emp_rec_by_name(self, name):
        return next((rec for rec in self._emp_rex if rec.name == name), None)

    def get_asn_rec(self, id):
        return next((rec for rec in self._asn_rex if rec.id == id), None)
        
    def get_dept_data(self):
        return self._dept_rex

    def get_grant_admin_data(self):
        return self._grant_admin_rex

    def get_sent_invoices(self, quarter=None):
        if quarter:
            return [rec for rec in self._invoices_sent if rec.quarter == quarter]
        return self._invoices_sent

    def get_sent_invoice(self, inv_num):
        return next((rec for rec in self._invoices_sent if rec.invoice_num == inv_num), None)

    def remove_sent_invoices(self, inv_nums):
        self._invoices_sent = [rec for rec in self._invoices_sent if rec.invoice_num not in inv_nums]

    def set_unsent_invoices(self, invoices):
        self._invoices_unsent = invoices

    def get_unsent_invoices(self, quarter=None):
        if quarter:
            return [rec for rec in self._invoices_unsent if rec.quarter == quarter]
        return self._invoices_unsent

    def get_unsent_invoice(self, inv_num):
        return next((rec for rec in self._invoices_unsent if rec.invoice_num == inv_num), None)

    def send_invoice(self, inv_num):
        invoice = self.get_unsent_invoice(inv_num)
        self._invoices_sent.append(invoice)
        self._invoices_unsent = [rec for rec in self._invoices_unsent if rec.invoice_num != inv_num]

    def set_asn_data(self, asns):
        self._asn_rex = asns

    def get_asn_data(self, quarter=None):
        import lib.month_lib as ml

        if quarter:
            s_qtr = str(quarter)
            yr = int(s_qtr[0:4])
            qtr = int(s_qtr[4])
            frum, thru = ml.get_quarter_interval(yr, qtr)
            return [a for a in self._asn_rex if ml.is_in_span(a.frum, a.thru, frum, thru)]
        return self._asn_rex

