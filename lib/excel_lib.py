import xlrd
import datetime


def get_file(parent):
    import wx

    folder = 'c:/bench/allocat/data'
    dlg = wx.FileDialog(parent, 'Open', folder, '',
                        'Excel files (*.xls;*.xlsx)|*.xls;*.xlsx',
                        wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
    dlg.ShowModal()
    file = dlg.GetPath()
    dlg.Destroy()
    return file


def open_wb(file):
    return xlrd.open_workbook(file)


def get_sheet_names(wb):
    return wb.sheet_names()


def get_latest_sheet(wb):
    return wb.sheets()[0]


def to_date(xl_date):

    try:
        t = xlrd.xldate_as_tuple(xl_date, 0)
    except Exception:
        return None
    return datetime.date(t[0], t[1], t[2])


def to_xl_date(m, d, y):
    temp = datetime.datetime(1899, 12, 30)
    py_date = datetime.datetime(y, m, d)
    delta = py_date - temp
    return float(delta.days) + (float(delta.seconds) / 86400)


def get_nrows(xl_sheet):
    return sum(1 for _ in xl_sheet.get_rows())


def get_sheet_data(sheet):
    rows = []
    flds = sheet.row_values(0)
    for idx in range(1, sheet.nrows):
        rows.append(dict(zip(flds, sheet.row_values(idx))))
    return rows
