class LedgerDataSet(object):

    def __init__(self, db_path):
        self.db_path = db_path

        self._prj_rex = []
        self._emp_rex = []
        self._asn_rex = []
        self._dept_rex = []
        self._grant_admin_rex = []

        self._build_dataset()

        self._active_only = True

    def _get_data(self):
        from dal.dao import Dao
        from models.project import Project
        from models.employee import Employee
        from models.department import Department
        from models.grant_admin import GrantAdmin

        dao = Dao(db_path=self.db_path, stateful=True)
        self._prj_rex = Project.get_names(dao)
        self._emp_rex = Employee.get_names(dao)
        self._dept_rex = Department.get_names(dao)
        self._grant_admin_rex = GrantAdmin.get_names(dao)
        dao.close()

    def _build_dataset(self):
        self._get_data()

    def set_active_only(self, value):
        self._active_only = value

    def get_active_only(self):
        return self._active_only

    def get_prj_data(self):
        if self._active_only:
            return [rec for rec in self._prj_rex if rec.active]
        return self._prj_rex

    def get_emp_data(self):
        if self._active_only:
            return [rec for rec in self._emp_rex if rec.active]
        return self._emp_rex

    def get_dept_data(self):
        return self._dept_rex

    def get_grant_admin_data(self):
        return self._grant_admin_rex
