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


def is_in_prj_span(prj, first_month, last_month):
    if first_month < prj['first_month']:
        return False
    return last_month <= prj['last_month']

def get_timeframe_edges(list):
    min = '9999'
    max = '0000'
    for item in list:
        if item['first_month'] < min:
            min = item['first_month']
        if item['last_month'] > max:
            max = item['last_month']
    return min, max
