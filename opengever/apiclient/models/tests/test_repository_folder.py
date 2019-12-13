from .. import RepositoryFolder
from ... import GEVERClient
from ...tests import TestCase


class TestRepositoryFolderModel(TestCase):

    def test_properties(self):
        repository_folder = GEVERClient(self.repository_folder_url, self.regular_user).fetch()
        self.assertIsInstance(repository_folder, RepositoryFolder)
        self.assertEqual(12, repository_folder.items_total)
        self.assertEqual('2016-08-31T07:07:33+00:00', repository_folder.created)
        self.assertEqual('Verträge mit der kantonalen Finanzverwaltung', repository_folder.items[0].title)

    def test_raw(self):
        repository_folder = GEVERClient(self.repository_folder_url, self.regular_user).fetch()
        self.maxDiff = None
        self.assertDictContainsSubset(
            {
                'UID': 'createrepositorytree000000000003',
                'allow_discussion': False,
                'changed': '2016-08-31T07:07:33+00:00',
                'classification': 'unprotected',
                'created': '2016-08-31T07:07:33+00:00',
                'description': '',
                'id': 'vertraege-und-vereinbarungen',
                'is_folderish': True,
                'layout': 'tabbed_view',
                'modified': '2016-08-31T19:05:33+00:00',
                'privacy_layer': 'privacy_layer_no',
                'public_trial': 'unchecked',
                'public_trial_statement': None,
                'reference_number': 'Client1 1.1',
                'relative_path': 'ordnungssystem/fuehrung/vertraege-und-vereinbarungen',
                'review_state': 'repositoryfolder-state-active',
                'title_de': 'Verträge und Vereinbarungen',
                'title_fr': 'Contrats et accords',
            },
            repository_folder.raw)

    def test_url(self):
        repository_folder = GEVERClient(self.repository_folder_url, self.regular_user).fetch()
        self.assertEqual(self.repository_folder_url, repository_folder.url)
