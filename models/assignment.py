import globals as gbl


class Assignment(object):
    def __init__(self, d=None):
        self.id = None
        self.employee_id = None
        self.employee = ''
        self.project_id = None
        self.project = ''
        self.frum = ''
        self.thru = ''
        self.effort = None
        self.notes = ''
        self.active = 1
        if d:
            self.from_dict(d)

    def from_dict(self, d):
        for attr in d:
            setattr(self, attr, d[attr])
        self.effort = int(self.effort)

    @staticmethod
    def get_all(dao):
        sql = ("SELECT a.*, p.name AS project, e.name AS employee "
               "FROM assignments a "
               "JOIN projects p ON a.project_id=p.id "
               "JOIN employees e ON a.employee_id=e.id")
        rex = dao.execute(sql)
        return [Assignment(rec) for rec in rex] if rex else []

    @staticmethod
    def drop_many(dao, ids):
        sql = "UPDATE assignments SET active=0 WHERE id IN (%s)" % (
                  dao.get_param_str(ids))
        nrex = dao.execute(sql, ids)
        gbl.dataset.drop_asns(ids)
        return nrex

    @staticmethod
    def get_for_timeframe(dao, frum, thru):
        sql = ("SELECT a.*, e.name AS employee, p.name AS project "
               "FROM assignments a "
               "JOIN employees e ON a.employee_id=e.id "
               "JOIN projects p ON a.project_id=p.id "
               "WHERE a.frum >= ? AND a.thru <= ?")
        vals = (frum, thru)
        return dao.execute(sql, vals)

    def add(self, dao):
        sql = ("INSERT INTO assignments "
               "(employee_id, project_id, frum, thru, effort, notes, active) "
               "VALUES(%s)" % (('?,' * 7)[0:-1],))
        vals = [
            self.employee_id, self.project_id,
            self.frum, self.thru, self.effort,
            self.notes, 1
        ]
        self.id = dao.execute(sql, vals)
        gbl.dataset.add_asn(self)
        return self.id

    def update(self, dao):
        sql = ("UPDATE assignments "
               "SET employee_id=?, project_id=?, "
               "frum=?, thru=?, effort=?, notes=?, active=? "
               "WHERE id=?")
        vals = [
            self.employee_id, self.project_id,
            self.frum, self.thru, self.effort,
            self.notes, 1, self.id
        ]
        nrex = dao.execute(sql, vals)
        gbl.dataset.update_asn(self)
        return nrex
