class Ledger(object):

    def __init__(self, d=None):
        self.id = None
        self.quarter = None
        self.project_id = None
        self.department_id = None
        self.admin_approved = False
        self.va_approved = False
        self.invoice_num = ''
        self.staff_id = None
        self.pct_effort = None
        self.salary = None
        self.fringe = None
        self.total_day = None
        self.days = None
        self.amount = None
        self.frum = None
        self.thru = None
        self.paid = None
        self.balance = None
        self.short_code = ''
        self.grand_admin = None
        self.grant_admin_email = None
        if d:
            for attr in d:
                setattr(self, attr, d[attr])

    @staticmethod
    def get_rex(dao, quarter):
        sql = ("SELECT * FROM ledger "
               "WHERE quarter=?")
        return dao.execute(sql, (quarter,))

    @staticmethod
    def update_salary_fringe(dao, salary, fringe, id):
        sql = ("UPDATE ledger "
               "SET salary=?, fringe=? "
               "WHERE id=?")
        vals = (salary, fringe, id)
        return dao.execute(sql, vals)
