class AllocatDataSet(object):

    def __init__(self, db_path):
        self.db_path = db_path

        self.prjRex = {}
        self.empRex = {}
        self.asnRex = {}

        # These are to validate uniqueness
        self.prjNames = {}
        self.prjFullNames = {}
        self.empNames = {}

        self.buildDataSet()

    def getData(self):
        from dal.dao import Dao
        from models.project import Project
        from models.employee import Employee
        from models.assignment import Assignment

        dao = Dao(db_path=self.db_path, stateful=True)
        self.prjRex = Project.get_all(dao)
        self.empRex = Employee.get_all(dao)
        self.asnRex = Assignment.get_all(dao)
        dao.close()

    def buildDataSet(self):
        import lib.ui_lib as uil

        self.getData()

        for prj in self.prjRex:
            prj.asns = [asn for asn in self.asnRex if asn.project_id==prj.id]
            self.prjNames[uil.set2compare(prj.name)] = prj.id
            self.prjFullNames[uil.set2compare(prj.full_name)] = prj.id

        for emp in self.empRex:
            emp.asns = [asn for asn in self.asnRex if asn.employee_id==emp.id]
            self.empNames[uil.set2compare(emp.name)] = emp.id


