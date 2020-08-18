import datetime as dt

MONTH_FORMAT = '%y%m'


def prettify(month):
    if len(month) != 4:
        return month
    return month[2:] + '/' + month[0:2]


def uglify(month):
    if len(month) != 5:
        return month
    return (month[3:] + month[0:2]).strip()


def get_months(startMonth, thruMonth):
    from dateutil.relativedelta import relativedelta as rd

    start_date = month2d(startMonth)
    thru_date = month2d(thruMonth)
    months = []
    while start_date <= thru_date:
        months.append(d2month(start_date))
        start_date = start_date + rd(months=1)
    return months


def date_plus(d, nmonths):
    return (d + dt.timedelta(nmonths * 365 / 12))


def d2month(d):
    return d.strftime(MONTH_FORMAT)


def month2d(month):
    return dt.datetime.strptime(month, MONTH_FORMAT)


def is_valid_span(first, last):
    return last >= first


def is_in_prj_span(prj, frum, thru):
    if frum < prj.frum:
        return False
    return thru <= prj.thru


def get_timeframe_edges(list):
    min = '9999'
    max = '0000'
    for item in list:
        if not item.active:
            continue
        if item.frum < min:
            min = item.frum
        if item.thru > max:
            max = item.thru
    return min, max

def get_quarter_interval(yr, qtr):
    y = int(yr[0:2])

    if qtr == 1:
        m1 = '10'
        m2 = '12'
        y = y - 1
    elif qtr == 2:
        m1 = '01'
        m2 = '03'
    elif qtr == 3:
        m1 = '04'
        m2 = '06'
    else:
        m1 = '07'
        m2 = '09'

    yr = str(y)
    if len(yr) == 1:
        yr = '0' + yr

    frum = yr + m1
    thru = yr + m2

    return frum, thru


def frum2dt(frum):
    m = int(frum[2:])
    y = int(frum[0:2]) + 2000
    return dt.datetime(y, m, 1)


def thru2dt(thru):
    m = int(thru[2:])
    y = int(thru[0:2]) + 2000
    d = 31
    if m in [4, 6, 9, 11]:
        d = 30
    elif m == 2:
        d = 29 if is_leap_year(y) else 28
    return dt.datetime(y, m, d)


def is_leap_year(year):
    if (year % 4) == 0:
       if (year % 100) == 0:
           if (year % 400) == 0:
               return True
           else:
               return False
       else:
           return True
    else:
       return False


def get_total_days(frum, thru):
    return (thru2dt(thru) - frum2dt(frum)).days + 1
