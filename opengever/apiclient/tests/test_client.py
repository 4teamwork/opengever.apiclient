from . import TestCase
from .. import GEVERClient
from ..exceptions import APIRequestException


class TestClient(TestCase):

    def test_retrieve_document(self):
        client = GEVERClient(
            f'{self.plone_url}ordnungssystem/fuehrung/vertraege-und-vereinbarungen/dossier-1/proposal-2/document-19',
            'kathi.barfuss')

        document = client.retrieve()
        self.assertTrue(document)

    def test_failure_when_retrieving_unknown_url(self):
        client = GEVERClient(f'{self.plone_url}ordnungssystem/bad-url', 'kathi.barfuss')
        with self.assertRaises(APIRequestException) as cm:
            client.retrieve()

        self.assertEqual(
            f'404 Client Error: Not Found for url: {self.plone_url}ordnungssystem/bad-url',
            str(cm.exception))
