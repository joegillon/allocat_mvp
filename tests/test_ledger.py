import unittest
from models.ledger import Ledger


class TestLedger(unittest.TestCase):

    def setUp(self):
        pass

    def testAdd(self):
        obj = Ledger()
        obj.add(None)
        pass
