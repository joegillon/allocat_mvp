import xlrd


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
    import datetime

    t = xlrd.xldate_as_tuple(xl_date, 0)
    return datetime.datetime(t[0], t[1], t[2])


def get_nrows(xl_sheet):
    return sum(1 for _ in xl_sheet.get_rows())
