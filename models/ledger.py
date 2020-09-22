import copy


class Ledger(object):

    def __init__(self, d=None):
        self.id = None
        self.quarter = 0
        self.dept = ''
        self.admin_approved = False
        self.va_approved = False
        self.invoice_num = ''
        self.asn_id = None
        self.salary = 0.0
        self.fringe = 0.0
        self.total_day = 0.0
        self.days = 0
        self.amount = 0.0
        self.paid = False
        self.balance = 0.0
        self.short_code = ''
        self.grant_admin = ''
        self.grant_admin_email = ''
        if d:
            for attr in d:
                setattr(self, attr, d[attr])

    @staticmethod
    def get_rex(dao, quarter):
        sql = ("SELECT ledger.*, "
               "projects.name AS project, "
               "employees.name AS employee, "
               "assignments.id AS asn_id, "
               "assignments.frum AS frum, "
               "assignments.thru AS thru, "
               "assignments.effort AS effort "
               "FROM ledger "
               "INNER JOIN assignments ON ledger.asn_id=assignments.id "
               "INNER JOIN projects ON assignments.project_id=projects.id "
               "INNER JOIN employees ON assignments.employee_id=employees.id "
               "WHERE quarter=?")
        return dao.execute(sql, (quarter,))

    def add(self, dao):
        vals = self.get_updatable_values()
        del vals['id']
        vals = self.stringify_values(vals)
        sql = ("INSERT INTO ledger "
               "(%s) "
               "VALUES (%s)" % (','.join(vals.keys()), ('?,' * len(vals))[0:-1]))
        self.id = dao.execute(sql, list(vals.values()))
        return self.id

    def update(self, dao):
        vals = self.get_updatable_values()
        vals = self.stringify_values(vals)
        sql = ("UPDATE ledger "
               "SET %s "
               "WHERE id=?;") % (
            ','.join(f + '=?' for f in vals.keys())
        )
        vals = list(vals.values()) + [self.id]
        return dao.execute(sql, vals)

    def get_updatable_values(self):
        self_copy = copy.copy(self)
        for fld in ['project', 'employee', 'effort', 'frum', 'thru']:
            delattr(self_copy, fld)
        return vars(self_copy)

    def stringify_values(self, vals):
        for k, v in vals.items():
            vals[k] = str(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else v
        return vals
