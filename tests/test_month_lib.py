import unittest
from lib.month_lib import *


class TestMonthLib(unittest.TestCase):

    def testPrettify(self):

        with self.assertRaises(ValueError) as ex:
            prettify('0000')       # month 00
        self.assertEqual('Invalid ugly month!', str(ex.exception))

        with self.assertRaises(ValueError) as ex:
            prettify('0013')       # month 00
        self.assertEqual('Invalid ugly month!', str(ex.exception))

        self.assertEqual(prettify('0001'), '01/00')
