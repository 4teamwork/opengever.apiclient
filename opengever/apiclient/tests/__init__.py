from contextlib import contextmanager
import os
import unittest


class TestCase(unittest.TestCase):

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
