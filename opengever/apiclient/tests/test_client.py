from .. import GEVERClient
from ..exceptions import APIRequestException
from ..models.base import APIModel
from . import TestCase


class TestClient(TestCase):

    def test_adopt_changes_url(self):
        document_client = GEVERClient(self.document_url, self.regular_user)
        self.assertEqual(self.document_url, document_client.url)
        self.assertEqual(self.regular_user, document_client.username)

        dossier_client = document_client.adopt(self.dossier_url)
        self.assertEqual(self.dossier_url, dossier_client.url)
        self.assertEqual(self.regular_user, dossier_client.username)

    def test_fetch_document(self):
        client = GEVERClient(self.document_url, self.regular_user)
        document = client.fetch()
        self.assertIsInstance(document, APIModel)
        self.assertEqual('Verträgsentwurf', document.title)

    def test_fetch_raw_document(self):
        client = GEVERClient(self.document_url, self.regular_user)
        document = client.fetch(raw=True)
        self.assertIsInstance(document, dict)
        self.assertEqual('Verträgsentwurf', document['title'])

    def test_failure_when_retrieving_unknown_url(self):
        client = GEVERClient(f'{self.plone_url}ordnungssystem/bad-url', self.regular_user)
        with self.assertRaises(APIRequestException) as cm:
            client.fetch()

        self.assertEqual(
            f'404 Client Error: Not Found for url: {self.plone_url}ordnungssystem/bad-url',
            str(cm.exception))

    def test_create_dossier(self):
        client = GEVERClient(self.repository_folder_url, self.regular_user)
        dossier = client.create_dossier('Wichtige Unterlagen',
                                        description='Richtig Wichtig')
        self.assertIsInstance(dossier, APIModel)
        self.assertEqual('Wichtige Unterlagen', dossier.title)
        self.assertEqual('Richtig Wichtig', dossier.description)
        self.assertEqual(self.regular_user, dossier.responsible)

    def test_create_dossier_raw(self):
        client = GEVERClient(self.repository_folder_url, self.regular_user)
        dossier = client.create_dossier('Kleines Dossier', raw=True)
        self.assertIsInstance(dossier, dict)
        self.assertEqual('Kleines Dossier', dossier['title'])

    def test_get_navigation(self):
        client = GEVERClient(self.root_url, self.regular_user)
        with self.assertRaisesRegex(NotImplementedError, 'use raw=True'):
            client.get_navigation()

        navigation = client.get_navigation(raw=True)
        self.assertEqual({
            '@id': f'{self.plone_url}ordnungssystem/@navigation',
            'tree': [
                {
                    '@type': 'opengever.repository.repositoryfolder',
                    'active': True,
                    'current': False,
                    'current_tree': False,
                    'description': 'Alles zum Thema Führung.',
                    'nodes': [
                        {
                            '@type': 'opengever.repository.repositoryfolder',
                            'active': True,
                            'current': False,
                            'current_tree': False,
                            'description': '',
                            'nodes': [],
                            'text': '1.1. Verträge und Vereinbarungen',
                            'uid': 'createrepositorytree000000000003',
                            'url': f'{self.plone_url}ordnungssystem/fuehrung/vertraege-und-vereinbarungen',
                        }
                    ],
                    'text': '1. Führung',
                    'uid': 'createrepositorytree000000000002',
                    'url': f'{self.plone_url}ordnungssystem/fuehrung',
                },
                {
                    '@type': 'opengever.repository.repositoryfolder',
                    'active': True,
                    'current': False,
                    'current_tree': False,
                    'description': '',
                    'nodes': [],
                    'text': '2. Rechnungsprüfungskommission',
                    'uid': 'createrepositorytree000000000004',
                    'url': f'{self.plone_url}ordnungssystem/rechnungspruefungskommission',
                },
                {
                    '@type': 'opengever.repository.repositoryfolder',
                    'active': False,
                    'current': False,
                    'current_tree': False,
                    'description': '',
                    'nodes': [],
                    'text': '3. Spinnännetzregistrar',
                    'uid': 'createrepositorytree000000000005',
                    'url': f'{self.plone_url}ordnungssystem/spinnaennetzregistrar',
                },
            ],
        }, navigation)

    def test_update_dossier(self):
        dossier = GEVERClient(self.repository_folder_url, self.regular_user).create_dossier('Ein Tossier')
        update = GEVERClient(dossier.url, self.regular_user).update_object(title='Ein Dossier')
        self.assertTrue(update)
