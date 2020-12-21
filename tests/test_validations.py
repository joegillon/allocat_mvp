import unittest
from lib.validator_lib import *


class ValidationTestSuite(unittest.TestCase):

    def setUp(self):
        self.prj_names = {
            'TESTNAME1': 41,
            'TESTNAME2': 23,
            'TESTNAME3': 18
        }
        self.prj_full_names = {
            'TESTFULLNAME1': 41,
            'TESTFULLNAME2': 23,
            'TESTFULLNAME3': 18
        }
        self.emp_names = {
            'MARX,GROUCHO': 1,
            'MARX,CHICO': 2,
            'MARX,HARPO': 3,
            'NAME-HYPHENATED,BOZO': 99
        }

    def testName(self):
        # Set current project to ID 18 (Test Name 3)
        prj_match = ProjectMatch(18, self.prj_names)

        # Project name cannot be None
        result = validate_prj_name(None, prj_match)
        self.assertEqual(result, 'Project name required!')

        # Project name cannot be ''
        result = validate_prj_name('', prj_match)
        self.assertEqual(result, 'Project name required!')

        # Project name must be unique
        result = validate_prj_name('test  name 2', prj_match)
        self.assertEqual(result, 'Project name not unique!')

        # Now we have a match but it's the current project
        result = validate_prj_name('test  name 3', prj_match)
        self.assertIsNone(result)

        result = validate_prj_name('Unused project name', prj_match)
        self.assertIsNone(result)

    def testFullName(self):
        # Set current project to ID 18 (Test Name 3)
        prj_match = ProjectMatch(18, self.prj_full_names)

        result = validate_prj_full_name(None, prj_match)
        self.assertEqual(result, 'Project full name required!')

        result = validate_prj_full_name('', prj_match)
        self.assertEqual(result, 'Project full name required!')

        result = validate_prj_full_name('test  fullname 1', prj_match)
        self.assertEqual(result, 'Project full name not unique!')

        result = validate_prj_full_name('test  fullname 3', prj_match)
        self.assertIsNone(result)

        result = validate_prj_full_name('Unused project full name', prj_match)
        self.assertIsNone(result)

    def testTimeframe(self):
        from models.project import Project

        result = validate_timeframe('', '')
        self.assertEqual(result, 'From, Thru dates required!')

        result = validate_timeframe('00', '')
        self.assertEqual(result, 'From, Thru dates required!')

        result = validate_timeframe('01', '')
        self.assertEqual(result, 'From, Thru dates required!')

        result = validate_timeframe('010', '')
        self.assertEqual(result, 'From, Thru dates required!')

        result = validate_timeframe('0000', '')
        self.assertEqual(result, 'From, Thru dates required!')

        result = validate_timeframe('0013', '')
        self.assertEqual(result, 'From, Thru dates required!')

        result = validate_timeframe('0001', '')
        self.assertEqual(result, 'From, Thru dates required!')

        result = validate_timeframe('0001', '00')
        self.assertEqual(result, 'Thru date invalid!')

        result = validate_timeframe('0001', '010')
        self.assertEqual(result, 'Thru date invalid!')

        result = validate_timeframe('0001', '0000')
        self.assertEqual(result, 'Thru date invalid!')

        result = validate_timeframe('0001', '0013')
        self.assertEqual(result, 'Thru date invalid!')

        result = validate_timeframe('0001', '00131')
        self.assertEqual(result, 'Thru date invalid!')

        result = validate_timeframe('1902', '1901')
        self.assertEqual(result, 'From date must precede thru date!')

        result = validate_timeframe('1901', '1812')
        self.assertEqual(result, 'From date must precede thru date!')

        result = validate_timeframe('1912', '2001')
        self.assertIsNone(result)

        prj = Project({
            'name': 'Any name',
            'full_name': 'Any full name',
            'frum': '1407',
            'thru': '1906'
        })
        result = validate_asn_timeframe('1406', '1906', prj)
        self.assertEqual(result, 'Timeframe outside project timeframe!')

        prj.frum = '1407'
        result = validate_asn_timeframe('1407', '1907', prj)
        self.assertEqual(result, 'Timeframe outside project timeframe!')

        prj.thru = '1906'
        result = validate_asn_timeframe('1407', '1906', prj)
        self.assertIsNone(result)

    def testEmpName(self):
        emp_match = EmployeeMatch(1, self.emp_names)

        result = validate_emp_name(None)
        self.assertEqual(result, 'Employee name required!')

        result = validate_emp_name('')
        self.assertEqual(result, 'Employee name required!')

        result = validate_emp_name('groucho marx', emp_match)
        self.assertEqual(result, 'Employee name invalid!')

        result = validate_emp_name('marx', emp_match)
        self.assertEqual(result, 'Employee name invalid!')

        result = validate_emp_name('_marx,groucho', emp_match)
        self.assertEqual(result, 'Employee name invalid!')

        result = validate_emp_name('marx,groucho:', emp_match)
        self.assertEqual(result, 'Employee name invalid!')

        result = validate_emp_name('marx,  groucho', emp_match)
        self.assertIsNone(result)

        result = validate_emp_name('marx,harpo', emp_match)
        self.assertEqual(result, 'Employee name not unique!')

        result = validate_emp_name('name-hyphenated,bozo', emp_match)
        self.assertEqual(result, 'Employee name not unique!')

        result = validate_emp_name('marx, zeppo', emp_match)
        self.assertIsNone(result)

        result = validate_emp_name("o'marx, groucho", emp_match)
        self.assertIsNone(result)

        result = validate_emp_name("marx, o'groucho", emp_match)
        self.assertIsNone(result)

        result = validate_emp_name('marx-karl, groucho', emp_match)
        self.assertIsNone(result)

        result = validate_emp_name('marx, karl-groucho', emp_match)
        self.assertIsNone(result)

    def testFte(self):
        result = validate_fte("")
        self.assertEqual(result, 'FTE required!')

        # result = validate_fte('x2')
        # self.assertEqual(result, 'FTE must be number between 0-100!')
        #
        result = validate_fte('-1')
        self.assertEqual(result, 'FTE must be number between 0-100!')

        result = validate_fte('101')
        self.assertEqual(result, 'FTE must be number between 0-100!')

        result = validate_fte('0')
        self.assertIsNone(result)

        result = validate_fte('100')
        self.assertIsNone(result)

        result = validate_fte('22')
        self.assertIsNone(result)

    def testEffort(self):
        result = validate_effort(None)
        self.assertEqual(result, 'Percent effort required!')

        result = validate_effort("")
        self.assertEqual(result, 'Percent effort required!')

        result = validate_effort('x2')
        self.assertEqual(result, 'Percent effort must be number between 0-100!')

        result = validate_effort('-1')
        self.assertEqual(result, 'Percent effort must be number between 0-100!')

        result = validate_effort('101')
        self.assertEqual(result, 'Percent effort must be number between 0-100!')

        result = validate_effort('0')
        self.assertIsNone(result)

        result = validate_effort('100')
        self.assertIsNone(result)

        result = validate_effort('22')
        self.assertIsNone(result)
