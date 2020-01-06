class AllocatDataSet(object):

    def __init__(self, db_path):
        self.db_path = db_path

        self.prj_rex = {}
        self.emp_rex = {}
        self.asn_rex = {}

        # These are to validate uniqueness
        self.prj_names = {}
        self.prj_full_names = {}
        self.emp_names = {}

        self.build_dataset()

    def get_data(self):
        from dal.dao import Dao
        from models.project import Project
        from models.employee import Employee
        from models.assignment import Assignment

        dao = Dao(db_path=self.db_path, stateful=True)
        self.prj_rex = Project.get_all(dao)
        self.emp_rex = Employee.get_all(dao)
        self.asn_rex = Assignment.get_all(dao)
        dao.close()

    def build_dataset(self):
        import lib.ui_lib as uil

        self.get_data()

        for prj in self.prj_rex:
            prj.asns = [asn for asn in self.asn_rex if asn.project_id == prj.id]
            self.prj_names[uil.set2compare(prj.name)] = prj.id
            self.prj_full_names[uil.set2compare(prj.full_name)] = prj.id

        for emp in self.emp_rex:
            emp.asns = [asn for asn in self.asn_rex if asn.employee_id == emp.id]
            self.emp_names[uil.set2compare(emp.name)] = emp.id


