class LedgerDataSet(object):

    def __init__(self, db_path):
        self.db_path = db_path

        self._emp_rex = []
        self._asn_rex = []
        self._dept_rex = []
        self._grant_admin_rex = []
        self._ledger_rex = []
        self._ledger_entries = []

        self.build_dataset()

    def _get_data(self):
        from dal.dao import Dao

        from models.employee import Employee
        from models.department import Department
        from models.grant_admin import GrantAdmin
        from models.ledger import Ledger
        from models.assignment import Assignment

        dao = Dao(db_path=self.db_path, stateful=True)
        self._emp_rex = Employee.get_all(dao)
        self._dept_rex = Department.get_all(dao)
        self._grant_admin_rex = GrantAdmin.get_all(dao)
        self._ledger_rex = Ledger.get_rex(dao)
        # self._asn_rex = Assignment.get_billables(dao)
        dao.close()

    def build_dataset(self):
        self._get_data()

    def get_emp_data(self):
        return self._emp_rex

    def get_emp_rec(self, id):
        return next((rec for rec in self._emp_rex if rec.id == id), None)

    def get_emp_rec_by_name(self, name):
        return next((rec for rec in self._emp_rex if rec.name == name), None)

    def get_dept_data(self):
        return self._dept_rex

    def get_grant_admin_data(self):
        return self._grant_admin_rex

    def get_ledger_data(self, quarter=None):
        if quarter:
            return [rec for rec in self._ledger_rex if rec.quarter == quarter]
        return self._ledger_rex

    def set_ledger_entries(self, entries):
        self._ledger_entries = entries

    def get_ledger_entries(self):
        return self._ledger_entries

    def set_asn_data(self, asns):
        self._asn_rex = asns

    def get_asn_data(self, quarter=None):
        import lib.month_lib as ml

        if quarter:
            yr = int(quarter[0:4])
            qtr = int(quarter[4])
            frum, thru = ml.get_quarter_interval(yr, qtr)
            return [a for a in self._asn_rex if ml.is_in_span(a.frum, a.thru, frum, thru)]
        return self._asn_rex
