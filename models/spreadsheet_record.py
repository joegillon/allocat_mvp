class SpreadsheetRecord(object):

    def __init__(self, d=None):
        self.name = ''
        self.salary = 0.0
        self.fringe = 0.0
        self.step_date = None
        self.matched = False
        if d:
            self.name = d['name']
            self.salary = d['salary']
            self.fringe = d['fringe']
            self.step_date = d['step_date']
            self.matched = d['matched'] if 'matched' in d else False
