from .. import ModelRegistry
from ... import GEVERClient
from ...tests import TestCase
from ..base import BaseModel


class TestModelRegistry(TestCase):

    def setUp(self):
        super().setUp()
        self.client = GEVERClient(self.root_url, 'kathi.barfuss')

    def test_wrap_requires_dict(self):
        with self.assertRaises(ValueError) as cm:
            ModelRegistry.wrap('foo', self.client)

        self.assertEqual('Expected dict, got str', str(cm.exception))

    def test_wrap_requires_type(self):
        with self.assertRaises(ValueError) as cm:
            ModelRegistry.wrap({}, self.client)

        self.assertEqual('Missing @type in item.', str(cm.exception))

    def test_unkown_portal_type_is_wrapped_in_base_model(self):
        obj = ModelRegistry.wrap(
            {'@type': 'foo',
             '@id': self.document_url},
            self.client)
        self.assertIsInstance(obj, BaseModel)

    def test_get_model(self):
        self.assertTrue(ModelRegistry.get('opengever.document.document'))
        self.assertFalse(ModelRegistry.get('opengever.document.foobar'))
