import lib.ui_lib as uil


class AllocatDataSet(object):

    def __init__(self, db_path):
        self.db_path = db_path

        self._prj_rex = []
        self._emp_rex = []
        self._asn_rex = []

        # These are to validate uniqueness
        self.prj_names = {}
        self.prj_full_names = {}
        self.emp_names = {}

        self._build_dataset()

        self._active_only = True

        self._observers = {
            'projects': [], 'employees': [], 'assignments': []
        }

    def _get_data(self):
        from dal.dao import Dao
        from models.project import Project
        from models.employee import Employee
        from models.assignment import Assignment

        dao = Dao(db_path=self.db_path, stateful=True)
        self._prj_rex = Project.get_all(dao)
        self._emp_rex = Employee.get_all(dao)
        self._asn_rex = Assignment.get_all(dao)
        dao.close()

    def _build_dataset(self):
        self._get_data()

        for prj in self._prj_rex:
            prj.asns = [asn for asn in self._asn_rex if asn.project_id == prj.id]
            self.prj_names[uil.set2compare(prj.name)] = prj.id
            self.prj_full_names[uil.set2compare(prj.full_name)] = prj.id

        for emp in self._emp_rex:
            emp.asns = [asn for asn in self._asn_rex if asn.employee_id == emp.id]
            self.emp_names[uil.set2compare(emp.name)] = emp.id

    def set_active_only(self, value):
        self._active_only = value

    def get_active_only(self):
        return self._active_only

    def get_prj_data(self):
        if self._active_only:
            return [rec for rec in self._prj_rex if rec.active]
        return self._prj_rex

    def get_prj_rec(self, id):
        return next((rec for rec in self._prj_rex if rec.id == id), None)
    
    def get_emp_data(self):
        if self._active_only:
            return [rec for rec in self._emp_rex if rec.active]
        return self._emp_rex

    def get_emp_rec(self, id):
        return next((rec for rec in self._emp_rex if rec.id == id), None)

    def get_emp_rec_by_name(self, name):
        return next((rec for rec in self._emp_rex if rec.name == name), None)

    def get_asn_data(self):
        if self._active_only:
            return [rec for rec in self._asn_rex if rec.active]
        return self._asn_rex

    def get_asn_rec(self, id):
        return next((rec for rec in self._asn_rex if rec.id == id), None)

    def bind_to(self, tbl, callback):
        self._observers[tbl].append(callback)

    def notify(self, tbl, idx=None):
        for callback in self._observers[tbl]:
            callback(idx) if idx else callback()

    def add_prj(self, new_prj):
        self._prj_rex.append(new_prj)
        self._prj_rex = sorted(self._prj_rex, key=lambda i: i.name.lower())
        idx = self._prj_rex.index(new_prj)
        if self._active_only:
            idx = [x for x in self._prj_rex if x.active].index(new_prj)
        self.prj_names[uil.set2compare(new_prj.name)] = new_prj.id
        self.prj_full_names[uil.set2compare(new_prj.full_name)] = new_prj.id
        self.notify('projects', idx)

    def update_prj(self, old_rec, new_rec):
        idx = self._prj_rex.index(new_rec)
        if old_rec.name != new_rec.name:
            del self.prj_names[uil.set2compare(old_rec.name)]
            self.prj_names[uil.set2compare(new_rec.name)] = new_rec.id
        if old_rec.full_name != new_rec.full_name:
            del self.prj_full_names[uil.set2compare(old_rec.full_name)]
            self.prj_full_names[uil.set2compare(new_rec.full_name)] = new_rec.id
        if self._active_only:
            idx = [x for x in self._prj_rex if x.active].index(new_rec)
        self.notify('projects', idx)

    def drop_prj(self, prj):
        del self.prj_names[uil.set2compare(prj.name)]
        del self.prj_full_names[uil.set2compare(prj.full_name)]
        idx = self._prj_rex.index(prj)
        del self._prj_rex[idx]
        self.notify('projects')

    def add_emp(self, new_emp):
        self._emp_rex.append(new_emp)
        self._emp_rex = sorted(self._emp_rex, key=lambda i: i.name.lower())
        idx = self._emp_rex.index(new_emp)
        if self._active_only:
            idx = [x for x in self._emp_rex if x.active].index(new_emp)
        self.emp_names[uil.set2compare(new_emp.name)] = new_emp.id
        self.notify('employees', idx)

    def update_emp(self, old_rec, new_rec):
        idx = self._emp_rex.index(new_rec)
        if old_rec.name != new_rec.name:
            del self.emp_names[uil.set2compare(old_rec.name)]
            self.emp_names[uil.set2compare(new_rec.name)] = new_rec.id
        if self._active_only:
            idx = [x for x in self._emp_rex if x.active].index(new_rec)
        self.notify('employees', idx)

    def drop_emp(self, emp):
        del self.emp_names[uil.set2compare(emp.name)]
        idx = self._emp_rex.index(emp)
        del self._emp_rex[idx]
        self.notify('employees')

    def add_asn(self, new_asn):
        prj = [rec for rec in self._prj_rex if rec.id == new_asn.project_id][0]
        prj.asns.append(new_asn)

        emp = [rec for rec in self._emp_rex if rec.id == new_asn.employee_id][0]
        emp.asns.append(new_asn)

        new_asn.employee = emp.name
        new_asn.project = prj.name
        self._asn_rex.append(new_asn)

        self.notify('assignments')

    def update_asn(self, asn):
        self.notify('assignments')

    def drop_asns(self, ids):
        # asn_id = ids[0]
        # asn = [rec for rec in self._asn_rex if rec.id == asn_id][0]
        asn = self.get_asn_rec(ids[0])
        # prj_id = asn.project_id
        # emp_id = asn.employee_id

        # prj = [rec for rec in self._prj_rex if rec.id == prj_id][0]
        prj = self.get_prj_rec(asn.project_id)
        prj.asns = [a for a in prj.asns if a.id not in ids]
        # for asn in prj.asns:
        #     if asn.id in ids:
        #         prj.asns.remove(asn)

        # emp = [rec for rec in self._emp_rex if rec.id == emp_id][0]
        emp = self.get_emp_rec(asn.employee_id)
        emp.asns = [a for a in emp.asns if a.id not in ids]
        # for asn in emp.asns:
        #     if asn.id in ids:
        #         emp.asns.remove(asn)

        self._asn_rex = [a for a in self._asn_rex if a.id not in ids]
        # for asn in [rec for rec in self._asn_rex if rec.id in ids]:
        #     self._asn_rex.remove(asn)

        self.notify('assignments')
