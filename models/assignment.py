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
