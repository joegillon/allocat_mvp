class LedgerDataSet(object):

    def __init__(self, db_path):
        self.db_path = db_path

        self._prj_rex = []
        self._emp_rex = []
        self._asn_rex = []
        self._dept_rex = []
        self._grant_admin_rex = []

        self.build_dataset()

    def _get_data(self):
        from dal.dao import Dao
        from models.project import Project
        from models.ledger_employee import LedgerEmployee
        from models.department import Department
        from models.grant_admin import GrantAdmin

        dao = Dao(db_path=self.db_path, stateful=True)
        self._prj_rex = Project.get_names(dao)
        self._emp_rex = LedgerEmployee.get_all(dao)
        self._dept_rex = Department.get_names(dao)
        self._grant_admin_rex = GrantAdmin.get_all(dao)
        self._ledger_rex = []
        dao.close()

    def build_dataset(self):
        self._get_data()

    def get_prj_data(self):
        return self._prj_rex

    def get_emp_data(self):
        return self._emp_rex

    def get_emp_rec(self, name):
        return next((rec for rec in self._emp_rex if rec.name == name), None)

    def get_dept_data(self):
        return self._dept_rex

    def get_grant_admin_data(self):
        return self._grant_admin_rex

    def set_ledger_data(self, rex):
        self._ledger_rex = rex
