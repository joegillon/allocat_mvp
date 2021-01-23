import copy


class Invoice(object):

    def __init__(self, d=None):
        self.id = None
        self.quarter = 0
        self.dept = ''
        self.admin_approved = False
        self.va_approved = False
        self.invoice_num = ''
        self.asn_id = None
        self.project = '',
        self.employee = '',
        self.salary = 0.0
        self.fringe = 0.0
        self.total_day = 0.0
        self.frum = '',
        self.thru = '',
        self.effort = 0,
        self.days = 0
        self.amount = 0.0
        self.paid = False
        self.balance = 0.0
        self.short_code = ''
        self.grant_admin = ''
        self.grant_admin_email = ''
        if d:
            for attr in d:
                if attr in ['admin_approved', 'va_approved', 'paid']:
                    setattr(self, attr, True if d[attr] else False)
                else:
                    setattr(self, attr, d[attr])

    def __eq__(self, other):
        for attr in self.__dict__.keys():
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True
    
    # @staticmethod
    # def get_rex(dao, quarter):
    #     sql = ("SELECT ledger.*, "
    #            "projects.name AS project, "
    #            "employees.name AS employee, "
    #            "assignments.id AS asn_id, "
    #            "assignments.frum AS frum, "
    #            "assignments.thru AS thru, "
    #            "assignments.effort AS effort "
    #            "FROM ledger "
    #            "INNER JOIN assignments ON ledger.asn_id=assignments.id "
    #            "INNER JOIN projects ON assignments.project_id=projects.id "
    #            "INNER JOIN employees ON assignments.employee_id=employees.id "
    #            "WHERE quarter=?")
    #     return dao.execute(sql, (quarter,))

    @staticmethod
    def get_rex(dao):
        sql = "SELECT * FROM ledger WHERE paid=0"
        # sql = ("SELECT * FROM ledger "
        #        "WHERE quarter=? AND paid=?")
        # sql = ("SELECT ledger.*, "
        #        "projects.name AS project, "
        #        "employees.name AS employee, "
        #        "employees.salary AS salary, "
        #        "employees.fringe AS fringe, "
        #        "employees.va_email AS va_email, "
        #        "employees.nonva_email AS nonva_email, "
        #        "assignments.id AS asn_id, "
        #        "assignments.frum AS frum, "
        #        "assignments.thru AS thru, "
        #        "assignments.effort AS effort "
        #        "FROM ledger "
        #        "INNER JOIN assignments ON ledger.asn_id=assignments.id "
        #        "INNER JOIN projects ON assignments.project_id=projects.id "
        #        "INNER JOIN employees ON assignments.employee_id=employees.id "
        #        "WHERE quarter=? AND paid=?")
        rex = dao.execute(sql)
        return [Invoice(rec) for rec in rex] if rex else []

    def add(self, dao):
        self_copy = copy.copy(self)
        my_items = self.stringify_values(vars(self_copy))
        del my_items['id']
        keys = my_items.keys()
        vals = my_items.values()

        sql = ("INSERT INTO ledger "
               "(%s) "
               "VALUES (%s)" % (','.join(keys), ('?,' * len(vals))[0:-1]))
        self.id = dao.execute(sql, list(vals))
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
        for fld in [
            'id', 'quarter', 'asn_id',
            'project', 'employee', 'salary', 'fringe', 'total_day', 'effort', 'frum', 'thru',
            'days', 'paid'
        ]:
            delattr(self_copy, fld)
        return vars(self_copy)

    def stringify_values(self, vals):
        for k, v in vals.items():
            if isinstance(v, bool):
                vals[k] = '1' if v else '0'
            elif isinstance(v, (int, float)):
                vals[k] = str(v)
        return vals

    @staticmethod
    def get_by_invoice(dao, invoice_num):
        sql = "SELECT * FROM ledger WHERE invoice_num=?"
        rex = dao.execute(sql, (invoice_num,))
        return Invoice(rex[0]) if rex else None

    def update_balance(self, dao, amount):
        self.balance = round(self.balance - amount, 2)
        if self.balance == 0.0:
            self.paid = True
        sql = "UPDATE ledger SET balance=?, paid=? WHERE id=?"
        dao.execute(sql, (self.balance, self.paid, self.id))
