from io import BytesIO

import requests_mock

from .. import GEVERClient
from ..exceptions import APIRequestException
from ..models import Document
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

    def test_exception_includes_response_from_gever(self):
        client = GEVERClient(f'{self.plone_url}ordnungssystem/nope', self.regular_user)
        with requests_mock.Mocker() as mocker:
            mocker.get(f'{self.plone_url}ordnungssystem/nope', text='GEVER says no', status_code=500)
            with self.assertLogs(level='ERROR') as cm, self.assertRaises(APIRequestException):
                client.fetch()

        # The last error should include the original response from GEVER.
        error = cm.output[-1]
        self.assertIn('Response from GEVER: GEVER says no', error)

    def test_create_dossier(self):
        client = GEVERClient(self.repository_folder_url, self.regular_user)
        dossier = client.create_dossier('Wichtige Unterlagen',
                                        description='Richtig Wichtig')
        self.assertIsInstance(dossier, APIModel)
        self.assertEqual('Wichtige Unterlagen', dossier.title)
        self.assertEqual('Richtig Wichtig', dossier.description)
        self.assertEqual(self.regular_user, dossier.responsible['token'])

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
        self.maxDiff = None
        self.assertEqual({
            '@id': f'{self.plone_url}ordnungssystem/@navigation',
            'tree': [
                {
                    '@type': 'opengever.repository.repositoryfolder',
                    'active': True,
                    'current': False,
                    'current_tree': False,
                    'description': 'Alles zum Thema Führung.',
                    'is_leafnode': False,
                    'nodes': [
                        {
                            '@type': 'opengever.repository.repositoryfolder',
                            'active': True,
                            'current': False,
                            'current_tree': False,
                            'description': '',
                            'is_leafnode': True,
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
                    'is_leafnode': True,
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
                    'is_leafnode': True,
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

    def test_listing(self):
        listing = GEVERClient(url=self.dossier_url, username=self.regular_user).listing(name='documents')
        # All listing elements are returned
        self.assertEqual(listing['items_total'], 12)
        # Results are wrapped as 'Documents'
        self.assertIsInstance(listing['items'][0], Document)
        self.assertEqual(
            listing['items'][0].url,
            f'{self.plone_url}ordnungssystem/fuehrung/vertraege-und-vereinbarungen/dossier-1/task-1/document-35'
        )

    def test_documents_listing(self):
        listing = GEVERClient(url=self.dossier_url, username=self.regular_user).listing(
            name='documents',
            columns=[
                'title',
                'created',
                'modified',
                'filename',
                'checked_out',
                'bumblebee_checksum',
                'file_extension',
                'document_type',
            ]
        )
        first_document = listing['items'][0]
        self.assertEqual(first_document.title, 'Feedback zum Vertragsentwurf')
        self.assertEqual(first_document.created, '2016-08-31T16:05:33+00:00')
        self.assertEqual(first_document.modified, '2016-08-31T16:05:33+00:00')
        self.assertEqual(first_document.filename, 'Feedback zum Vertragsentwurf.docx')
        self.assertEqual(first_document.checked_out, '')
        self.assertEqual(first_document.bumblebee_checksum, '5ed3f5959a83418cb26e0ae4f54319695f0c5faac0833616bdba8d4d856f659c')
        self.assertEqual(first_document.file_extension, '.docx')
        self.assertEqual(first_document.document_type, None)

    def test_listing_passes_optional_params(self):
        listing = GEVERClient(url=self.dossier_url, username=self.regular_user).listing(name='documents', b_size=700)
        self.assertEqual(700, listing['b_size'])

    def test_office_connector_url(self):
        response = GEVERClient(url=self.document_url, username=self.regular_user).get_office_connector_url()

        # The Office Connector is a string starting with 'oc:', followed by a JWT. The value of
        # the JWT is based on secreted generated by Plone durin boot time, so we cannot predict
        # it. It is though sufficient to test for the return value to start with 'oc:'.
        self.assertTrue(
            response.startswith('oc:')
        )

    def test_create_document(self):
        document = GEVERClient(url=self.dossier_url, username=self.regular_user).create_document(
            title='Ein Dokument',
            file=BytesIO(b'content of the document'),
            content_type='text/plain',
            filename='Ein Dokument.txt',
            size=23,
        )

        self.assertIsInstance(document, Document)
        self.assertEqual('Ein Dokument', document.title)
        self.assertEqual({
            'content-type': 'text/plain',
            'download': f'{self.plone_url}ordnungssystem/fuehrung/vertraege-und-vereinbarungen/dossier-1/document-41/@@download/file',
            'filename': 'Ein Dokument.txt',
            'size': 23
        }, document.file)

    def test_accepts_headers(self):
        client = GEVERClient(url=self.dossier_url, username=self.regular_user, headers={'Accept-Language': 'fr-CH'})
        self.assertDictContainsSubset({'Accept-Language': 'fr-CH'}, client.session.headers)

    def test_get_sharing(self):
        sharing = GEVERClient(url=self.dossier_url, username='nicole.kohler').sharing()
        # Asserting the structure of the content and that it is non-empty should be good enough.
        self.assertEqual(list(sharing.keys()), ['available_roles', 'entries', 'inherit'])

    def test_set_sharing(self):
        sharing = GEVERClient(url=self.dossier_url, username='nicole.kohler').sharing()
        self.assertNotIn('rk_users', [entry['id'] for entry in sharing['entries']])
        ok = GEVERClient(url=self.dossier_url, username='nicole.kohler').set_group_roles('rk_users', {'Reader': True})
        self.assertTrue(ok)
        sharing = GEVERClient(url=self.dossier_url, username='nicole.kohler').sharing()
        self.assertIn('rk_users', [entry['id'] for entry in sharing['entries']])

    # def test_get_group(self):
    #     This would require a new fixture, as the Administrator does not have permissions to access this endpoint.
    #     group = GEVERClient(url=self.root_url, username='nicole.kohler').get_group('rk_users')
