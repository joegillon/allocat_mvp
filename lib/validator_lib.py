import re
from collections import namedtuple
import lib.month_lib as ml
import lib.ui_lib as uil

MONTH_PATTERN = r"^[0-9]{2}(0[1-9]|1[0-2])$"
WHOLE_NAME_PATTERN = r"^[A-Z'\-]+,[\s]*[A-Z' \-]+$"
SCALE_100_PATTERN = r"^[0-9][0-9]?$|^100$"
SCALE_15_PATTERN = r"^[0-9]$|^1[0-5]$"
EMAIL_PATTERN = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"

ProjectMatch = namedtuple('ProjectMatch', 'id values')
EmployeeMatch = namedtuple('EmployeeMatch', 'id names')


def validate_prj_name(value, match=None):
    if value is None or value == '':
        return 'Project name required!'

    if match:
        target = uil.set2compare(value)
        if target in match.values:
            if match.values[target] != match.id:
                return 'Project name not unique!'

    return None


def validate_prj_full_name(value, match=None):
    if value is None or value == '':
        return 'Project full name required!'

    if match:
        target = uil.set2compare(value)
        if target in match.values:
            if match.id == 0 or match.values[target] != match.id:
                return 'Project full name not unique!'

    return None


def validate_timeframe(frum, thru):
    if not re.match(MONTH_PATTERN, frum):
        return 'From date invalid!'

    if not re.match(MONTH_PATTERN, thru):
        return 'Thru date invalid!'

    if not ml.is_valid_span(frum, thru):
        return 'From date must precede thru date!'

    return None

def validate_asn_timeframe(frum, thru, prj=None):
    errMsg = validate_timeframe(frum, thru)
    if errMsg:
        return errMsg

    if prj:
        if not ml.is_in_prj_span(prj, frum, thru):
            return 'Timeframe outside project timeframe!'

    return None


def validate_emp_name(value, match=None):
    if value is None or value == '':
        return 'Employee name required!'

    if match:
        if not re.match(WHOLE_NAME_PATTERN, value.upper()):
            return 'Employee name invalid!'

        target = uil.set2compare(value)
        if target in match.names:
            if match.names[target] != match.id:
                return 'Employee name not unique!'

    return None


def validate_fte(value):
    if value is None or value == '':
        return 'FTE required!'

    value = int(value)
    if value < 0 or value > 100:
        return 'FTE must be number between 0-100!'
    return None


def validate_email(value):
    if value and (not re.search(EMAIL_PATTERN, value)):
        return 'Invalid non-VA email!'


def validate_va_email(value):
    if not value:
        return None

    if not re.search(EMAIL_PATTERN, value):
        return 'Invalid VA email'

    parts = value.split('@')
    if parts[1].lower() != 'va.gov':
        return 'Invalid VA email!'


def validate_effort(value):
    if value is None or value == '':
        return 'Percent effort required!'

    if not re.match(SCALE_100_PATTERN, value):
        return 'Percent effort must be number between 0-100!'

    return None


def showErrMsg(ctl, msg):
    import wx

    if ctl:
        ctl.SetFocus()
    wx.MessageBox(msg, 'Error!', wx.ICON_EXCLAMATION | wx.OK)
