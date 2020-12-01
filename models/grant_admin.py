class GrantAdmin(object):

    def __init__(self, d=None):
        self.id = None
        self.name = ''
        self.email = ''
        if d:
            self.id = d['id']
            self.name = d['name']
            self.email = d['email']

    def __eq__(self, other):
        for attr in self.__dict__.keys():
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True
    
    @staticmethod
    def get_all(dao):
        sql = "SELECT * FROM grant_admins ORDER BY name"
        rex = dao.execute(sql)
        return [GrantAdmin(rec) for rec in rex] if rex else []

    @staticmethod
    def get_names(dao):
        sql = "SELECT name FROM grant_admins ORDER BY name"
        rex = dao.execute(sql)
        return [rec['name'] for rec in rex] if rex else []

    @staticmethod
    def add_admin(dao, name, email):
        sql = "INSERT INTO grant_admins (name, email) VALUES (?,?)"
        return dao.execute(sql, (name, email))

    def add(self, dao):
        sql = "INSERT INTO grant_admins (name, email) VALUES (?,?)"
        return dao.execute(sql, (self.name, self.email))

    def update(self, dao):
        sql = ("UPDATE grant_admins "
               "SET name=?, email=? "
               "WHERE id=?")
        return dao.execute(sql, (self.name, self.email, self.id))

    def drop(self, dao):
        sql = "DELETE FROM grant_admins WHERE id=?"
        return dao.execute(sql, (self.id,))
