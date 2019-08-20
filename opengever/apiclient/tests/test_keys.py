from . import TestCase
from opengever.apiclient.keys import KeyRegistry
from pathlib import Path


class TestKeyRegistry(TestCase):

    def tearDown(self):
        super().tearDown()
        KeyRegistry.reset()

    def test_key_dirs_are_configurable_through_env_variable(self):
        with self.env(OPENGEVER_APICLIENT_KEY_DIRS=''):
            self.assertEqual((), KeyRegistry.get_key_dirs())

        with self.env(OPENGEVER_APICLIENT_KEY_DIRS='/tmp/foo:/tmp/bar'):
            self.assertEqual(('/tmp/foo', '/tmp/bar'), KeyRegistry.get_key_dirs())

    def test_loads_keys_from_environment_variable(self):
        with self.env(OPENGEVER_APICLIENT_KEY_DIRS=str(Path(__file__).parent / 'keys')):
            KeyRegistry.reset()
            self.assertEqual(('http://gever.test/mandant/',), tuple(KeyRegistry.keys))

    def test_loads_keys_of_one_directory(self):
        directory = str(Path(__file__).parent / 'keys')
        with self.env(OPENGEVER_APICLIENT_KEY_DIRS=''):
            KeyRegistry.clear()
            self.assertEqual((), tuple(KeyRegistry.keys))
            KeyRegistry.load_keys(directory)
            self.assertEqual(('http://gever.test/mandant/',), tuple(KeyRegistry.keys))

    def test_get_base_url_for(self):
        with self.env(OPENGEVER_APICLIENT_KEY_DIRS=str(Path(__file__).parent / 'keys')):
            KeyRegistry.reset()
            self.assertEqual(
                None,
                KeyRegistry.get_base_url_for('http://unknown/url'))
            self.assertEqual(
                'http://gever.test/mandant/',
                KeyRegistry.get_base_url_for('http://gever.test/mandant/foo/bar/baz'))

    def test_get_key_for(self):
        with self.env(OPENGEVER_APICLIENT_KEY_DIRS=str(Path(__file__).parent / 'keys')):
            KeyRegistry.reset()
            self.assertEqual(None, KeyRegistry.get_key_for('http://unknown/url'))
            self.assertDictContainsSubset(
                {
                    'client_id': '4321',
                    'issued': '2018-05-23T00:00:00',
                    'key_id': '1234',
                    'token_uri': 'http://gever.test/mandant/@@oauth2-token',
                    'user_id': 'ris.app',
                },
                KeyRegistry.get_key_for('http://gever.test/mandant/foo/bar/baz'))
