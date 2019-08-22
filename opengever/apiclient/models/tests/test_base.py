from ... import GEVERClient
from ...tests import TestCase
from ..base import APIModel


class TestAPIModel(TestCase):

    def test_parent(self):
        document = GEVERClient(self.document_url, 'kathi.barfuss').retrieve()
        self.assertEqual(self.document_url, document.url)

        dossier = document.parent
        self.assertIsInstance(dossier, APIModel)
        self.assertEqual(self.dossier_url, dossier.url)
