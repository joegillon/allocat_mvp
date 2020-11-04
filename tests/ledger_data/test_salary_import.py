import datetime as dt
from models.spreadsheet_record import SpreadsheetRecord


ss_rex = [
    SpreadsheetRecord({
        'name': 'EMP 107',
        'salary': 74971,
        'fringe': .46,
        'step_date': dt.date(2020, 12, 10),
        'matched': True
    }),
    SpreadsheetRecord({
        'name': 'EMP 264',
        'salary': 70286,
        'fringe': .261,
        'step_date': None,
        'matched': True
    }),
    SpreadsheetRecord({
        'name': 'EMP 211',
        'salary': 50657,
        'fringe': .229,
        'step_date': dt.date(2021, 7, 8),
        'matched': True
    }),
    SpreadsheetRecord({
        'name': 'VA EMP 73',
        'salary': 117082,
        'fringe': .352,
        'step_date': dt.date(2019, 12, 1),
        'matched': False
    }),
    SpreadsheetRecord({
        'name': 'EMP 76',
        'salary': 142052,
        'fringe': .317,
        'step_date': None,
        'matched': True
    }),
    SpreadsheetRecord({
        'name': 'EMP 62',
        'salary': 53822,
        'fringe': .077,
        'step_date': None,
        'matched': True
    }),
    SpreadsheetRecord({
        'name': 'EMP 20',
        'salary': 61965,
        'fringe': .357,
        'step_date': dt.date(2021, 6, 10),
        'matched': True
    }),
    SpreadsheetRecord({
        'name': 'EMP 15',
        'salary': 52239,
        'fringe': .388,
        'step_date': dt.date(2020, 1, 2),
        'matched': True
    }),
    SpreadsheetRecord({
        'name': 'EMP 106',
        'salary': 67834,
        'fringe': .243,
        'step_date': None,
        'matched': True
    }),
    SpreadsheetRecord({
        'name': 'EMP 282',
        'salary': 44444,
        'fringe': .044,
        'step_date': None,
        'matched': True
    }),
    SpreadsheetRecord({
        'name': 'EMP 52',
        'salary': 107070,
        'fringe': .335,
        'step_date': dt.date(2019, 10, 1),
        'matched': True
    }),
    SpreadsheetRecord({
        'name': 'EMPL 61',
        'salary': 37122,
        'fringe': .189,
        'step_date': None,
        'matched': False
    }),
    SpreadsheetRecord({
        'name': 'EMPL 56',
        'salary': 76470,
        'fringe': .422,
        'step_date': dt.date(2019, 11, 1),
        'matched': False
    })
]

matched_rec = SpreadsheetRecord({
        'name': 'VA EMP 73',
        'salary': 117082,
        'fringe': .352,
        'step_date': dt.date(2019, 12, 1),
        'matched': True
})
