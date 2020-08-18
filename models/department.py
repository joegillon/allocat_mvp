class Department(object):

    def __init__(self, d=None):
        self.id = None
        self.name = ''
        if d:
            self.id = d['id']
            self.name = d['name']

    @staticmethod
    def get_all(dao):
        sql = "SELECT * FROM departments ORDER BY name"
        rex = dao.execute(sql)
        return [Department(rec) for rec in rex] if rex else []

    @staticmethod
    def get_names(dao):
        sql = "SELECT name FROM departments ORDER BY name"
        rex = dao.execute(sql)
        return [rec['name'] for rec in rex] if rex else []
