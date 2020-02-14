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
            for attr in d:
                setattr(self, attr, d[attr])

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
        return dao.execute(sql, ids)

    @staticmethod
    def get_for_timeframe(dao, frum, thru):
        sql = ("SELECT a.*, e.name, p.name "
               "FROM assignments a "
               "JOIN employees e ON a.employee_id=e.id "
               "JOIN projects p ON a.project_id=p.id "
               "WHERE a.frum >= ? AND a.thru <= ?")
        vals = (frum, thru)
        return dao.execute(sql, vals)
