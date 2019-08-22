from . import TestCase
from .. import GEVERClient
from ..exceptions import APIRequestException


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
        self.assertTrue(client.fetch())

    def test_failure_when_retrieving_unknown_url(self):
        client = GEVERClient(f'{self.plone_url}ordnungssystem/bad-url', self.regular_user)
        with self.assertRaises(APIRequestException) as cm:
            client.fetch()

        self.assertEqual(
            f'404 Client Error: Not Found for url: {self.plone_url}ordnungssystem/bad-url',
            str(cm.exception))
