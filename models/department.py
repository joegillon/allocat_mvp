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

    @staticmethod
    def add_rec(dao, name):
        sql = "INSERT INTO departments (name) VALUES (?)"
        return dao.execute(sql, (name,))

    def add(self, dao):
        sql = "INSERT INTO departments (name) VALUES (?)"
        return dao.execute(sql, (self.name,))

    def update(self, dao):
        sql = "UPDATE departments SET name=? WHERE id=?"
        return dao.execute(sql, (self.name, self.id))

    def drop(self, dao):
        sql = 'DELETE FROM departments WHERE id=?'
        return dao.execute(sql, (self.id,))
