class Assignment(object):
    def __init__(self, d=None):
        self.id = None
        self.employee_id = None
        self.employee = ''
        self.project_id = None
        self.project = ''
        self.frum = ''
        self.thru = ''
        self.effort = None
        self.notes = ''
        self.active = 1
        if d:
            for attr in d:
                setattr(self, attr, d[attr])
