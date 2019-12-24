import unittest
from unittest.mock import MagicMock
import tests.mock_objects as mock_objects
from models.project import Project
from presenters.project_presenter import ProjectPresenter

db_rex = [
    {
        'id': 1,
        'name': 'Test Project One',
        'nickname': 'Test Prj 1',
        'frum': '1911',
        'thru': '2004'
     },
    {
        'id': 2,
        'name': 'Test Project Two',
        'nickname': 'Test Prj 2',
        'frum': '1910',
        'thru': '1912'
     },
    {
        'id': 3,
        'name': 'Test Project Three',
        'nickname': 'Test Prj 3',
        'frum': '1810',
        'thru': '2010'
     },
    {
        'id': 4,
        'name': 'Test Project Four',
        'nickname': 'Test Prj 4',
        'frum': '1911',
        'thru': '2011'
     },
]


class TestProjectPresenter(unittest.TestCase):

    def setUp(self):
        self.view = mock_objects.MockProjectFrame()
        self.model = [Project(p) for p in db_rex]
        self.interactor = mock_objects.MockProjectInteractor()
        self.presenter = ProjectPresenter(self.model, self.view, self.interactor)

    def testAddSavesDataToModelAndReloadsView(self):
        formValues = {
            'name': 'Test Project Five',
            'nickname': 'Test Prj 5',
            'frum': '1911',
            'thru': '2004'
        }
        self.presenter.loadView = MagicMock(
            side_effect=self.presenter.loadView)
        self.presenter.addProject(formValues)
        assert self.view.name == 'Test Project Five'
        assert self.view.nickname == 'Test Prj 5'
        assert self.view.frum == '1911'
        assert self.view.thru == '2004'

        # noinspection PyUnresolvedReferences
        assert self.presenter.loadView.called

    def testUpdateSavesDataToModelAndReloadsView(self):
        formValues = db_rex[1]
        formValues['nickname'] = 'New nickname'
        self.presenter.loadView = MagicMock(
            side_effect=self.presenter.loadView
        )
        self.presenter.updateProject(formValues)
        assert self.view.name == 'Test Project Two'
        assert self.view.nickname == 'New nickname'
        assert self.view.frum == '1910'
        assert self.view.thru == '1912'

        # noinspection PyUnresolvedReferences
        assert self.presenter.loadView.called

    def testSaveAddsNewDataToModelAndReloadsView(self):
        self.view.setName('Test Project Five')
        self.view.setNickname('Test Prj 5')
        self.view.setFrum('1911')
        self.view.setThru('2004')
        self.view.setSelectedIdx(-1)
        self.presenter.loadView = MagicMock(
            side_effect=self.presenter.loadView
        )
        self.presenter.save()
        assert self.view.name == 'Test Project Five'
        assert self.view.nickname == 'Test Prj 5'
        assert self.view.frum == '1911'
        assert self.view.thru == '2004'

        # noinspection PyUnresolvedReferences
        assert self.presenter.loadView.called

    def testSaveUpdatesChangeToModelAndReloadsView(self):
        self.view.setName('Test Project Two')
        self.view.setNickname('New nickname')
        self.view.setFrum('1910')
        self.view.setThru('1912')
        self.view.setSelectedIdx(1)
        self.presenter.loadView = MagicMock(
            side_effect=self.presenter.loadView
        )
        self.presenter.save()
        assert self.view.name == 'Test Project Two'
        assert self.view.nickname == 'New nickname'
        assert self.view.frum == '1910'
        assert self.view.thru == '1912'

        # noinspection PyUnresolvedReferences
        assert self.presenter.loadView.called

    def testDropRestoresDataFromModelAndReloadsView(self):
        self.view.setSelectedIdx(2)
        assert self.model[self.view.getSelectedIdx()].id == 3
        assert len(self.model) == 4
        self.presenter.loadView = MagicMock(
            side_effect=self.presenter.loadView
        )
        self.presenter.drop()
        assert len(self.model) == 3
        assert self.model[1].id == 2
        assert self.model[2].id == 4

        # noinspection PyUnresolvedReferences
        assert self.presenter.loadView.called

    def testDropLastRestoresDataFromModelAndReloadsView(self):
        self.view.setSelectedIdx(3)
        assert self.model[self.view.getSelectedIdx()].id == 4
        assert len(self.model) == 4
        self.presenter.loadView = MagicMock(
            side_effect=self.presenter.loadView
        )
        self.presenter.drop()
        assert len(self.model) == 3
        assert self.model[1].id == 2
        assert self.model[2].id == 3

        # noinspection PyUnresolvedReferences
        assert self.presenter.loadView.called

    def testAddNewProject(self):
        projectCount = len(self.presenter.model)
        self.presenter.addProject({
            'name': 'Test Project Five',
            'nickname': 'Test Prj 5',
            'frum': '1911',
            'thru': '2011'
        })
        assert len(self.presenter.model) is projectCount + 1

if __name__ == '__main__':
    unittest.main()
