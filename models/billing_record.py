class BillingRecord(object):

    def __init__(self, t=None):
        self._invoice_num = ''
        self._date = None
        self._deposit_num = ''
        self.amount = 0.0
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
        self._invoice_num = value[3:]

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
        self._deposit_num = value[3:]
