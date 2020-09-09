import unittest
from presenters.ledger_presenter import LedgerPresenter


class TestLedgerPresenter(unittest.TestCase):

    def setUp(self):
        self.presenter = LedgerPresenter(None)

    def testCalculateCost(self):
        salary = 123554
        fringe = .41
        effort = 10
        ndays = 91
        cost = self.presenter.calculate_cost(salary, fringe, effort, ndays)
        self.assertEquals(cost, 6076.94)
