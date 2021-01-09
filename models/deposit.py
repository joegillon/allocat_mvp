class Deposit(object):

    def __init__(self, t=None):
        self.id = None
        self._invoice_num = None
        self._date = None
        self._deposit_num = None
        self.amount = None
        self.ledger_id = None
        self.fy = None
        self.qtr = None
        if t:
            self.invoice_num = t[1]
            self.date = t[2]
            self.deposit_num = t[3]
            self.amount = t[6]

    @property
    def invoice_num(self):
        return self._invoice_num

    @invoice_num.setter
    def invoice_num(self, value):
        if value.startswith('506'):
            value = value[3:]
        self._invoice_num = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        import lib.excel_lib as xl

        self._date = xl.to_date(value)

    @property
    def deposit_num(self):
        return self._deposit_num

    @deposit_num.setter
    def deposit_num(self, value):
        if value.startswith('506'):
            value = value[3:]
        self._deposit_num = value

    @staticmethod
    def get_by_invoice_num(dao, invoice_num):
        sql = "SELECT * FROM deposits WHERE invoice_num=?"
        vals = (invoice_num,)
        rex = dao.execute(sql, vals)
        if len(rex) > 1:
            raise Exception('Multiple deposit records for invoice ' + invoice_num)
        if len(rex) == 0:
            return None
        return Deposit(rex[0])

    def add(self, dao):
        sql = ("INSERT INTO deposits "
               "(invoice_num, deposit_num, date, amount) "
               "VALUES(?,?,?,?)")
        vals = (
            self.invoice_num, self.deposit_num, self.date, self.amount
        )
        return dao.execute(sql, vals)
