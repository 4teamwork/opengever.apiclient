import requests_mock

from . import TestCase
from ..exceptions import AuthorizationFailed
from ..exceptions import ServiceKeyMissing
from ..keys import KeyRegistry
from ..session import GEVERSession


class TestGeverSessionManager(TestCase):

    def test_returns_prepared_session_when_called(self):
        manager = GEVERSession(f'{self.plone_url}ordnungssystem/', 'john.doe')
        self.assertTrue(manager().get)
        self.assertTrue(manager().post)
        self.assertTrue(manager().headers.get("Authorization"))

    def test_error_when_no_key_configured(self):
        with self.assertRaises(ServiceKeyMissing) as cm:
            GEVERSession("http://gever.example.com/fd/", "john.doe")

        self.maxDiff = None
        self.assertEqual(
            f"No GEVER service key found for URL http://gever.example.com/fd/.\n"
            f"Found keys ('{self.plone_url}',) "
            f"in paths {KeyRegistry.get_key_dirs()!r}",
            str(cm.exception))

    def test_error_when_key_invalid(self):
        with requests_mock.Mocker() as mocker:
            mocker.post(f'{self.plone_url}@@oauth2-token', status_code=500)
            with self.assertRaises(AuthorizationFailed) as cm:
                GEVERSession(f'{self.plone_url}ordnungssystem/', 'john.doe')

        self.maxDiff = None
        self.assertEqual(
            f'500 Server Error: None for url: {self.plone_url}@@oauth2-token',
            str(cm.exception))

    def test_user_agent(self):
        manager = GEVERSession(f'{self.plone_url}ordnungssystem/', '')
        self.assertRegex(
            manager().headers.get('User-Agent'),
            r'^opengever.apiclient/[0-9.]+.dev0')

    def test_user_agent_is_configurable(self):
        with self.env(OPENGEVER_APICLIENT_USER_AGENT='Baumverwaltung/7.0'):
            manager = GEVERSession(f'{self.plone_url}ordnungssystem/', '')
            self.assertRegex(
                manager().headers.get('User-Agent'),
                r'^opengever.apiclient/[0-9.]+.dev0 Baumverwaltung/7.0')
