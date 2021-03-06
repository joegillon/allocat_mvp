import globals as gbl


class Employee(object):
    def __init__(self, d=None):
        self.id = None
        self.name = None
        self.fte = None
        self.investigator = False
        self.intern = False
        self.pm = False
        self.org = None
        self.va_email = None
        self.nonva_email = None
        self.salary = None
        self.fringe = None
        self.notes = None
        self.active = 1
        self.asns = []
        if d:
            for attr in d:
                setattr(self, attr, d[attr].strip() if isinstance(d[attr], str) else d[attr])
            missing = self.get_missing_flds()
            if missing:
                raise AttributeError('Missing required fields ' + missing)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        for attr in self.__dict__.keys():
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True
    
    def get_missing_flds(self):
        missing = []
        if not self.name:
            missing.append('name')
        return ','.join(missing) if missing else None

    @staticmethod
    def get_all(dao):
        sql = ("SELECT * "
               "FROM employees "
               "ORDER BY name")
        rex = dao.execute(sql)
        return [Employee(rec) for rec in rex] if rex else []

    def get_asns(self, dao):
        from models.assignment import Assignment

        sql = ("SELECT a.*, e.name AS employee, p.name AS project "
               "FROM assignments a "
               "LEFT JOIN employees e ON a.employee_id=e.id "
               "LEFT JOIN projects p ON a.project_id=p.id "
               "WHERE a.employee_id=?")
        vals = (self.id,)
        rex = dao.execute(sql, vals)
        return [Assignment(rec) for rec in rex] if rex else []

    def add(self, dao):
        missing = self.get_missing_flds()
        if missing:
            s = ','.join(missing)
            raise AttributeError('Missing required fields ' + s)
        flds = 'name,fte,investigator,intern,pm,org,notes,active'
        vals = [
            self.name.replace(', ', ','), self.fte, self.investigator, self.intern, self.pm,
            self.org, self.notes, 1
        ]
        sql = "INSERT INTO employees (%s) VALUES (%s)" % (
            flds, ('?,' * len(vals))[0:-1]
        )
        try:
            self.id = dao.execute(sql, vals)
            gbl.dataset.add_emp(self)
            return self.id
        except Exception as e:
            s = str(e)
            if s.startswith('UNIQUE constraint failed'):
                raise Exception('Employee %s is not unique!' % s.split('.')[1])
            else:
                raise

    def update(self, dao, new_values):
        import copy

        old_self = copy.copy(self)
        nrex = self.do_update(dao, new_values)
        if nrex != 1:
            raise Exception('Unexpected update return value: %d' % nrex)
        self.after_update(new_values)
        gbl.dataset.update_emp(old_self, self)

    def do_update(self, dao, new_values):
        new_values['name'] = new_values['name'].replace(', ', ',')
        sql = ("UPDATE employees "
               "SET %s "
               "WHERE id=?;") % (
                  ','.join(f + '=?' for f in new_values.keys()))
        vals = list(new_values.values()) + [self.id]
        try:
            return dao.execute(sql, vals)
        except Exception as e:
            s = str(e)
            if s.startswith('UNIQUE constraint failed'):
                raise Exception('Employee %s is not unique!' % s.split('.')[1])
            else:
                raise

    def after_update(self, new_values):
        for attr in new_values:
            setattr(self, attr, new_values[attr])

    def drop(self, dao):
        expected = len(self.asns) + 1
        sql = "UPDATE employees SET active=0 WHERE id=?"
        result = dao.execute(sql, (self.id,))
        if result < 1 or result > expected:
            raise Exception('Expected %d records affected, got %d' % (expected, result))
        gbl.dataset.drop_emp(self)

    def undrop(self, dao):
        sql = "UPDATE employees SET active=1 WHERE id=?"
        dao.execute(sql, (self.id,))

    @staticmethod
    def update_name(dao, old_name, new_name):
        sql = "UPDATE employees SET name=? WHERE name=?"
        try:
            return dao.execute(sql, (new_name, old_name))
        except Exception as e:
            s = str(e)
            if s.startswith('UNIQUE constraint failed'):
                raise Exception('Employee %s is not unique!' % s.split('.')[1])
            else:
                raise

    @staticmethod
    def add_name(dao, name):
        sql = "INSERT INTO employees (name, active) VALUES (?, ?)"
        try:
            return dao.execute(sql, (name, 1))
        except Exception as e:
            s = str(e)
            if s.startswith('UNIQUE constraint failed'):
                raise Exception('Employee %s is not unique!' % s.split('.')[1])
            else:
                raise

    @staticmethod
    def update_salaries(dao, rex):
        sql = ("UPDATE employees "
               "SET salary=?, fringe=? "
               "WHERE id=?")
        for rec in rex:
            vals = (int(rec['salary']), rec['fringe'], rec['id'])
            try:
                dao.txn_write(sql, vals)
            except Exception as e:
                dao.rollback()
                raise

        dao.commit()

    def update_pm(self, dao):
        sql = ("UPDATE employees "
               "SET pm=?, va_email=?, nonva_email=? "
               "WHERE id=?")
        vals = [self.pm, self.va_email, self.nonva_email, self.id]
        return dao.execute(sql, vals)
