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
                setattr(self, attr, d[attr])

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
        return [Project(rec) for rec in rex] if rex else []
