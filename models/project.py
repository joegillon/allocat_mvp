class Project(object):
    def __init__(self, d=None):
        self.id = None
        self.name = ''
        self.full_name = ''
        self.frum = ''
        self.thru = ''
        self.notes = ''
        self.investigator_id = None
        self.investigator = ''
        self.manager_id = None
        self.manager = ''
        self.active = 1
        self.asns = []
        if d:
            for attr in d:
                setattr(self, attr, d[attr])
            missing = self.get_missing_flds()
            if missing:
                raise AttributeError('Missing required fields ' + missing)

    def get_missing_flds(self):
        missing = []
        if not self.name:
            missing.append('name')
        if not self.full_name:
            missing.append('full name')
        if not self.frum:
            missing.append('from')
        if not self.thru:
            missing.append('thru')
        return ','.join(missing) if missing else None

    @staticmethod
    def get_all(dao):
        sql = ("SELECT p.*, i.name AS investigator, m.name AS manager "
               "FROM projects p "
               "LEFT JOIN employees i ON p.investigator_id=i.id "
               "LEFT JOIN employees m on p.manager_id=m.id "
               "ORDER BY name")
        rex = dao.execute(sql)
        return [Project(rec) for rec in rex] if rex else []

    def get_asns(self, dao):
        from models.assignment import Assignment

        sql = ("SELECT a.*, e.name AS employee, p.name AS project "
               "FROM assignments a "
               "LEFT JOIN employees e ON a.employee_id=e.id "
               "LEFT JOIN projects p ON a.project_id=p.id "
               "WHERE a.project_id=?")
        vals = (self.id,)
        rex = dao.execute(sql, vals)
        return [Assignment(rec) for rec in rex] if rex else []

    def add(self, dao):
        missing = self.get_missing_flds()
        if missing:
            s = ','.join(missing)
            raise AttributeError('Missing required fields ' + s)
        flds = 'name,full_name,frum,thru,investigator_id,manager_id,notes,active'
        sql = "INSERT INTO projects (%s) VALUES (%s)" % (
            flds, ('?,' * 8)[0:-1]
        )
        vals = [
            self.name, self.full_name, self.frum, self.thru,
            self.investigator_id, self.manager_id, self.notes, 1
        ]
        try:
            self.id = dao.execute(sql, vals)
            return self.id
        except Exception as e:
            s = str(e)
            if s.startswith('UNIQUE constraint failed'):
                raise Exception('Project %s is not unique!' % s.split('.')[1])
            else:
                raise

    def update(self, dao, new_values):
        new_values, investigator, manager = self.prep_update(new_values)
        nrex = self.do_update(dao, new_values)
        if nrex != 1:
            raise Exception('Unexpected update return value: %d' % nrex)
        self.post_update(new_values, investigator, manager)


    def prep_update(self, new_values):
        # Remove name and full_name if no change to avoid UNIQUE constraint
        if new_values['name'].upper() == self.name.upper():
            del new_values['name']
        if new_values['full_name'].upper() == self.full_name.upper():
            del new_values['full_name']

        # Replace Employee objects with Employee IDs
        if new_values['pi']:
            new_values['investigator_id'] = new_values['pi'].id
            investigator = new_values['pi'].name
        else:
            new_values['investigator_id'] = None
            investigator = None
        del new_values['pi']
        if new_values['pm']:
            new_values['manager_id'] = new_values['pm'].id
            manager = new_values['pm'].name
        else:
            new_values['manager_id'] = None
            manager = None
        del new_values['pm']

        return new_values, investigator, manager

    def do_update(self, dao, new_values):
        sql = ("UPDATE projects "
               "SET %s "
               "WHERE id=?;") % (
                  ','.join(f + '=?' for f in new_values.keys()))
        vals = list(new_values.values()) + [self.id]
        try:
            return dao.execute(sql, vals)
        except Exception as e:
            s = str(e)
            if s.startswith('UNIQUE constraint failed'):
                raise Exception('Project %s is not unique!' % s.split('.')[1])
            else:
                raise

    def post_update(self, new_values, investigator, manager):
        for attr in new_values:
            setattr(self, attr, new_values[attr])
        self.investigator = investigator
        self.manager = manager

    def drop(self, dao):
        expected = len(self.asns) + 1
        sql = "UPDATE projects SET active=0 WHERE id=?"
        result = dao.execute(sql, (self.id,))
        if result < 1 or result > expected:
            raise Exception('Expected %d records affected, got %d' % (expected, result))

    def undrop(self, dao):
        sql = "UPDATE projects SET active=1 WHERE id=?"
        dao.execute(sql, (self.id,))
