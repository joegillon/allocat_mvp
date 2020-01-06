class Employee(object):
    def __init__(self, d=None):
        self.id = None
        self.name = ''
        self.grade = ''
        self.step = ''
        self.fte = ''
        self.notes = ''
        self.investigator = False
        self.active = 1
        if d:
            for attr in d:
                setattr(self, attr, d[attr].strip() if isinstance(d[attr], str) else d[attr])

    @staticmethod
    def get_all(dao):
        sql = ("SELECT * "
               "FROM employees "
               "WHERE active "
               "ORDER BY name")
        rex = dao.execute(sql)
        return [Employee(rec) for rec in rex] if rex else []

    @staticmethod
    def get_inactives(dao):
        sql = ("SELECT p.*, i.name AS investigator, m.name AS manager "
               "FROM projects p "
               "LEFT JOIN employees i ON p.investigator_id=i.id "
               "LEFT JOIN employees m on p.manager_id=m.id "
               "WHERE NOT p.active "
               "ORDER BY nickname")
        rex = dao.execute(sql)
        return [Employee(rec) for rec in rex] if rex else []

    def get_asns(self, dao):
        from models.assignment import Assignment

        sql = ("SELECT a.*, e.name AS employee, p.name AS project "
               "FROM assignments a "
               "LEFT JOIN employees e ON a.employee_id=e.id "
               "LEFT JOIN projects p ON a.project_id=p.id "
               "WHERE a.active AND a.employee_id=?")
        vals = (self.id,)
        rex = dao.execute(sql, vals)
        return [Assignment(rec) for rec in rex] if rex else []
