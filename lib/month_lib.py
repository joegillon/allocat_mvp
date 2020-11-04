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


def get_months(frum, thru):
    from dateutil.relativedelta import relativedelta as rd

    start_date = month2d(frum)
    thru_date = month2d(thru)
    months = []
    while start_date <= thru_date:
        months.append(d2month(start_date))
        start_date = start_date + rd(months=1)
    return months


def date_plus(d, nmonths):
    return d + dt.timedelta(nmonths * 365 / 12)


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


def get_timeframe_edges(lst):
    mn = '9999'
    mx = '0000'
    for item in lst:
        if not item.active:
            continue
        if item.frum < mn:
            mn = item.frum
        if item.thru > mx:
            mx = item.thru
    return mn, mx


def get_quarter(month):
    if month in [10, 12]:
        return 1
    if month in [1, 3]:
        return 2
    if month in [4, 6]:
        return 3
    if month in [7, 9]:
        return 4
    return None


def get_quarter_interval(yr, qtr):
    y = int(str(yr)[2:])

    if qtr == 1:
        m1 = '10'
        m2 = '12'
        y -= 1
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


def frum2str(frum):
    return frum2dt(frum).strftime('%#m/%#d/%y')


def thru2dt(thru):
    m = int(thru[2:])
    y = int(thru[0:2]) + 2000
    d = 31
    if m in [4, 6, 9, 11]:
        d = 30
    elif m == 2:
        d = 29 if is_leap_year(y) else 28
    return dt.datetime(y, m, d)


def thru2str(thru):
    return thru2dt(thru).strftime('%#m/%#d/%y')


def is_leap_year(year):
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return True
            else:
                return False
    else:
        return False


def get_total_days(frum, thru):
    f_date = month2d(frum)
    t_date = month2d(thru)
    t_date = get_last_day_of_month(t_date)
    delta = t_date - f_date
    return delta.days + 1


def get_last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + dt.timedelta(days=4)
    return next_month - dt.timedelta(days=next_month.day)

def is_in_span(frum, thru, span_frum, span_thru):
    if frum < span_frum or thru > span_thru:
        return False
    return True

