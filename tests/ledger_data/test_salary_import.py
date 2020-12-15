import datetime as dt
from models.spreadsheet_record import SpreadsheetRecord


ss_rex = [
    SpreadsheetRecord({
        'name': 'AARON,HENRY',
        'salary': 74971,
        'fringe': .46,
        'step_date': dt.date(2020, 12, 10),
        'matched': True
    }),
    SpreadsheetRecord({
        'name': 'FORD,EDWARD C',
        'salary': 70286,
        'fringe': .261,
        'step_date': None,
        'matched': False
    }),
    SpreadsheetRecord({
        'name': 'KOUFAX,SANFORD',
        'salary': 50657,
        'fringe': .229,
        'step_date': dt.date(2021, 7, 8),
        'matched': True
    }),
    SpreadsheetRecord({
        'name': 'WILLIAMS,THEODORE',
        'salary': 117082,
        'fringe': .352,
        'step_date': dt.date(2019, 12, 1),
        'matched': True
    }),
    SpreadsheetRecord({
        'name': 'MAYS,WILLIE HOWARD JR',
        'salary': 142052,
        'fringe': .317,
        'step_date': None,
        'matched': True
    }),
    SpreadsheetRecord({
        'name': 'BERRA,LAWRENCE P',
        'salary': 53822,
        'fringe': .077,
        'step_date': None,
        'matched': False
    }),
    SpreadsheetRecord({
        'name': 'RUTH,GEORGE HERMAN',
        'salary': 61965,
        'fringe': .357,
        'step_date': dt.date(2021, 6, 10),
        'matched': False
    }),
    SpreadsheetRecord({
        'name': 'JETER,DEREK',
        'salary': 52239,
        'fringe': .388,
        'step_date': dt.date(2020, 1, 2),
        'matched': True
    }),
    SpreadsheetRecord({
        'name': 'KALINE,ALBERT W',
        'salary': 67834,
        'fringe': .243,
        'step_date': None,
        'matched': True
    }),
    SpreadsheetRecord({
        'name': 'BANKS,ERNEST',
        'salary': 44444,
        'fringe': .044,
        'step_date': None,
        'matched': True
    }),
    SpreadsheetRecord({
        'name': 'GEHRIG,HENRY LOUIS',
        'salary': 107070,
        'fringe': .335,
        'step_date': dt.date(2019, 10, 1),
        'matched': True
    }),
    SpreadsheetRecord({
        'name': 'MANTLE,MICKEY',
        'salary': 37122,
        'fringe': .189,
        'step_date': None,
        'matched': True
    }),
    SpreadsheetRecord({
        'name': 'DIMAGGIO,JOSEPH P',
        'salary': 76470,
        'fringe': .422,
        'step_date': dt.date(2019, 11, 1),
        'matched': True
    })
]
