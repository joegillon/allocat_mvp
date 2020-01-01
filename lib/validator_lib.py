import re
from collections import namedtuple
import lib.month_lib as ml
import lib.ui_lib as uil

MONTH_PATTERN = r"^[0-9]{2}(0[1-9]|1[0-2])$"
WHOLE_NAME_PATTERN = r"^[A-Z'\-]+,[\s]*[A-Z' \-]+$"
SCALE_100_PATTERN = r"^[0-9][0-9]?$|^100$"
SCALE_15_PATTERN = r"^[0-9]$|^1[0-5]$"


ProjectMatch = namedtuple('ProjectMatch', 'id values')
EmployeeMatch = namedtuple('EmployeeMatch', 'id names')


def validatePrjName(value, match=None):
    if value is None or value == '':
        return 'Project name required!'

    if match:
        target = uil.set2compare(value)
        if target in match.values:
            if match.values[target] != match.id:
                return 'Project name not unique!'

    return None


def validatePrjFullName(value, match=None):
    if value is None or value == '':
        return 'Project full name required!'

    if match:
        target = uil.set2compare(value)
        if target in match.values:
            if match.id == 0 or match.values[target] != match.id:
                return 'Project full name not unique!'

    return None


def validateTimeframe(frum, thru):
    if not re.match(MONTH_PATTERN, frum):
        return 'From date invalid!'

    if not re.match(MONTH_PATTERN, thru):
        return 'Thru date invalid!'

    if not ml.isValidSpan(frum, thru):
        return 'From date must precede thru date!'

    return None

def validateAsnTimeframe(frum, thru, prj=None):
    errMsg = validateTimeframe(frum, thru)
    if errMsg:
        return errMsg

    if prj:
        if not ml.isInPrjSpan(prj, frum, thru):
            return 'Timeframe outside project timeframe!'

    return None


def validateEmpName(value, match=None):
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


def validateFte(value):
    if value is None or value == '':
        return 'FTE required!'

    if not re.match(SCALE_100_PATTERN, value):
        return 'FTE must be number between 0-100!'
    return None


def validateEffort(value):
    if value is None or value == '':
        return 'Percent effort required!'

    if not re.match(SCALE_100_PATTERN, value):
        return 'Percent effort must be number between 0-100!'

    return None


def showErrMsg(ctl, msg):
    import wx

    ctl.SetFocus()
    wx.MessageBox(msg, 'Error!', wx.ICON_EXCLAMATION | wx.OK)
