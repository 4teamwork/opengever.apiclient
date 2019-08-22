from ... import GEVERClient
from ...tests import TestCase
from ..base import APIModel


class TestAPIModel(TestCase):

    def test_equality(self):
        document1 = GEVERClient(self.document_url, 'kathi.barfuss').retrieve()
        document2 = GEVERClient(self.document_url, 'kathi.barfuss').retrieve()
        self.assertEqual(document2, document1)

    def test_attribute_error_on_missing_properties(self):
        document = GEVERClient(self.document_url, 'kathi.barfuss').retrieve()
        with self.assertRaises(AttributeError):
            document.not_existing_property

    def test_parent(self):
        document = GEVERClient(self.document_url, 'kathi.barfuss').retrieve()
        self.assertEqual(self.document_url, document.url)

        dossier = document.parent
        self.assertIsInstance(dossier, APIModel)
        self.assertEqual(self.dossier_url, dossier.url)
