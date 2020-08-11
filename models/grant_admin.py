class GrantAdmin(object):

    def __init__(self, d=None):
        self.id = None
        self.name = ''
        self.email = ''
        if d:
            self.id = d['id']
            self.name = d['name']
            self.email = d['email']

    @staticmethod
    def get_all(dao):
        sql = "SELECT * FROM grant_admins ORDER BY name"
        rex = dao.execute(sql)
        return [GrantAdmin(rec) for rec in rex] if rex else []
