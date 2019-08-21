from contextlib import contextmanager
from pathlib import Path
import json
import os
import shutil
import tempfile
import unittest

from ..keys import KeyRegistry
from ..session import GEVERSession
from ..utils import singleton


PACKAGE_ROOT = (Path(__file__) / '..' / '..' / '..' / '..').resolve()
TESTS_DIR = (Path(__file__) / '..').resolve()
PLONE_URL = os.environ.get('TESTSERVER_PLONE_URL', 'http://localhost:55001/plone/')


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.plone_url = PLONE_URL

    def setUp(self):
        KeyRegistry.reset()
        GEVERSession.clear()

    @contextmanager
    def env(self, **env):
        original = os.environ.copy()
        os.environ.update(env)
        try:
            yield
        finally:
            os.environ.clear()
            os.environ.update(original)

    def assertDictContainsSubset(self, expected, got, msg=None):
        """Reimplementation of unittest.assertDictContainsSubset because it is
        deprecated and there is no other solution which provides a decent assertion
        message :-(
        """

        class Missing:
            def __repr__(self):
                return "<Missing value>"

        missing = Missing()
        prepared_got = {key: got.get(key, missing) for key in expected}
        self.assertEqual(expected, prepared_got, msg)


@singleton
class TestSuite:

    def setUp(self):
        self.create_temporary_keys_directory()

    def tearDown(self):
        self.remove_temporary_keys_directory()

    def create_temporary_keys_directory(self):
        self.keys_directory = tempfile.mkdtemp('keys')
        for source in (PACKAGE_ROOT / 'keys').glob('*.json'):
            with source.open('rb') as fio:
                key = json.load(fio)

            key['token_uri'] = key['token_uri'].replace(
                'http://localhost:55001/plone/', PLONE_URL)
            with (Path(self.keys_directory) / source.name).open('w+') as fio:
                json.dump(key, fio)

        os.environ.setdefault('OPENGEVER_APICLIENT_KEY_DIRS', self.keys_directory)

    def remove_temporary_keys_directory(self):
        shutil.rmtree(self.keys_directory)
