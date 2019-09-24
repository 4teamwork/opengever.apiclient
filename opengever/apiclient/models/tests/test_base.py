from ... import GEVERClient
from ...tests import TestCase
from ..base import APIModel


class TestAPIModel(TestCase):

    def test_equality(self):
        document1 = GEVERClient(self.document_url, self.regular_user).fetch()
        document2 = GEVERClient(self.document_url, self.regular_user).fetch()
        self.assertEqual(document2, document1)

    def test_attribute_error_on_missing_properties(self):
        document = GEVERClient(self.document_url, self.regular_user).fetch()
        with self.assertRaises(AttributeError):
            document.not_existing_property

    def test_fetch_partial_item_to_upgrade_to_full_item(self):
        dossier = GEVERClient(self.document_url, self.regular_user).fetch().parent
        with self.assertRaises(AttributeError):
            dossier.created

        self.assertEqual(dossier, dossier.fetch())
        self.assertTrue(dossier.created)
        self.assertEqual(self.dossier_url, dossier.url)

    def test_parent(self):
        document = GEVERClient(self.document_url, self.regular_user).fetch()
        self.assertEqual(self.document_url, document.url)

        dossier = document.parent
        self.assertIsInstance(dossier, APIModel)
        self.assertEqual(self.dossier_url, dossier.url)

    def test_items(self):
        document = GEVERClient(self.document_url, self.regular_user).fetch()
        self.assertIn(document, document.parent.fetch().items)

    def test_has_addable_type(self):
        repository_folder = GEVERClient(self.repository_folder_url, self.regular_user).fetch()
        self.assertTrue(repository_folder.has_addable_type('opengever.dossier.businesscasedossier'))
        self.assertFalse(repository_folder.has_addable_type('opengever.repository.repositoryfolder'))

    def test_id_path(self):
        dossier = GEVERClient(self.document_url, self.regular_user).fetch()
        self.assertEqual(dossier.id_path, "/plone/ordnungssystem/fuehrung/vertraege-und-vereinbarungen/dossier-1/document-14")

    def test_sequence_number(self):
        dossier = GEVERClient(self.document_url, self.regular_user).fetch()
        self.assertEqual(dossier.sequence_number, 14)
