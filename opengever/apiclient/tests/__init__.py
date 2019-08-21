from contextlib import contextmanager
from pathlib import Path
import os
import unittest

from ..keys import KeyRegistry
from ..session import GEVERSession


PACKAGE_ROOT = (Path(__file__) / '..' / '..' / '..' / '..').resolve()
TESTS_DIR = (Path(__file__) / '..').resolve()


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.environ.setdefault('OPENGEVER_APICLIENT_KEY_DIRS', str(PACKAGE_ROOT / 'keys'))

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
