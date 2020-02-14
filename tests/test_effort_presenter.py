import unittest
from unittest.mock import patch
from datetime import date
from tests.helpers import *
import globals as gbl
from models.dataset import AllocatDataSet
from presenters.effort_presenter import EffortPresenter


class TestEffortPresenter(unittest.TestCase):

    def setUp(self):
        gbl.dataset = AllocatDataSet(db_path='c:/bench/allocat/tests/allocat.db')
        self.app = wx.App()
        self.frame = wx.Frame(None)

        self.presenter = EffortPresenter(self.frame)
        self.presenter.init_view()

    def tearDown(self):
        self.frame.Destroy()
        self.app.Destroy()

    def get_vars(self):
        return self.presenter.view, self.presenter.model, self.presenter.view.grid_ctrl

    @patch('presenters.effort_presenter.get_init_dates', return_value=('2001', '2012'))
    def testViewLoaded(self):
        view, model, grid_ctrl = self.get_vars()

        # No grid clicks made
        # assert view.get_selected_idx() == 0

        assert view.get_frum() == '2001'
        assert view.frum_ctrl.GetValue() == '01/20'

