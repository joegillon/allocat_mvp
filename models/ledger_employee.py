class LedgerEmployee(object):
    def __init__(self, d=None):
        self.id = None
        self.emp_id = None
        self.name = ''
        self.va_email = ''
        self.nonva_email = ''
        self.salary = ''
        self.fringe = ''
        if d:
            for attr in d:
                setattr(self, attr, d[attr].strip() if isinstance(d[attr], str) else d[attr])

    @staticmethod
    def get_all(dao):
        sql = ("SELECT l.*, e.name AS name "
               "FROM employees e "
               "JOIN ledger_employees l ON l.emp_id=e.id "
               "ORDER BY e.name")
        rex = dao.execute(sql)
        return [LedgerEmployee(rec) for rec in rex] if rex else []

    @staticmethod
    def update_salaries(dao, rex):
        for rec in rex:
            sql = ("UPDATE ledger_employees "
                   "SET salary=?, fringe=? "
                   "WHERE emp_id=?")
            vals = (rec['salary'], rec['fringe'], rec['emp_id'])
            try:
                dao.txn_write(sql, vals)
            except Exception as e:
                dao.rollback()
                raise

        dao.commit()

