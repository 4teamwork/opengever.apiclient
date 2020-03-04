from requests import HTTPError
import jwt
import os
import pkg_resources
import requests
import threading
import time

from .exceptions import APIRequestException
from .exceptions import AuthorizationFailed
from .exceptions import ServiceKeyMissing
from .keys import KeyRegistry


GEVER_SESSION_STORAGE = threading.local()
GRANT_TYPE = "urn:ietf:params:oauth:grant-type:jwt-bearer"
API_CLIENT_VERSION = pkg_resources.get_distribution('opengever.apiclient').version


class GEVERSession:
    """The GEVER session provides requests sessions which are preconfigured for a
    GEVER client.

    The requests session is reused for multiple requests so that we have a smaller
    footprint regarding oauth authentication requests. The session is cached in memory.

    The GeverSession is instantiated with a GEVER url (to any ressource)
    and the operating user. Whenever a request to GEVER is initiated, the session
    must be called, returning a prepared requests object.
    """

    min_seconds_to_expiration = 60
    session_expiration_seconds = 60 * 60

    def __init__(self, url, username, headers={}):
        self.gever_base_url = KeyRegistry.get_base_url_for(url)
        if not self.gever_base_url:
            raise ServiceKeyMissing(url)

        self.username = username
        self.headers = headers
        self._session = self._get_session()

    def __call__(self):
        """Returns a requests session which is prepared for making a request to the
        GEVER client.
        By "prepared" we mean that session has a valid authorization header which will
        be valid in the near future ("near future" is defined by
        min_seconds_to_expiration).
        This method is meant to be called right before making a request, for each
        request.
        """
        token_expiration = self._session.gever_token_expiration
        if unfrozen_time() > (token_expiration - self.min_seconds_to_expiration):
            self._acquire_authorization_token(self._session)
        return self._session

    @staticmethod
    def clear():
        """Clear all caches.
        """
        GEVER_SESSION_STORAGE.sessions = None

    def _get_session(self):
        """Returns a ``requests`` session for the GEVER client with the given url.
        The session may be outdated.
        The session is reused over multiple requests by the same person.
        """
        if getattr(GEVER_SESSION_STORAGE, "sessions", None) is None:
            GEVER_SESSION_STORAGE.sessions = {}

        unique_session_key = (self.gever_base_url, self.username)
        if unique_session_key not in GEVER_SESSION_STORAGE.sessions:
            GEVER_SESSION_STORAGE.sessions[unique_session_key] = self._make_session()

        return GEVER_SESSION_STORAGE.sessions[unique_session_key]

    def _make_session(self):
        """Create a fresh requests session and return it.
        """
        session = requests.Session()
        session.hooks["response"].append(self._raise_for_status_hook)
        session.headers.update(
            {
                "User-Agent": self._user_agent,
                "Accept": "application/json",
                **self.headers,
            }
        )
        self._acquire_authorization_token(session)
        return session

    def _raise_for_status_hook(self, response, *args, **kwargs):
        try:
            response.raise_for_status()
        except HTTPError as exception:
            raise APIRequestException(exception)

    @property
    def _user_agent(self):
        """
        Use the version defined in setup.py. The commit hash could be included,
        but this is good enough for now.
        """
        custom_user_agent = os.environ.get('OPENGEVER_APICLIENT_USER_AGENT', '')
        return f'opengever.apiclient/{API_CLIENT_VERSION} {custom_user_agent}'.strip()

    def _acquire_authorization_token(self, session):
        """Acquires a fresh authorization token from GEVER and sets it in the
        current session.
        """
        service_key = KeyRegistry.get_key_for(self.gever_base_url)
        if service_key is None:
            raise ServiceKeyMissing(self.gever_base_url)

        claim_set = {
            "iss": service_key["client_id"],
            "sub": self.username,
            "aud": service_key["token_uri"],
            "iat": int(unfrozen_time()),
            "exp": int(unfrozen_time() + self.session_expiration_seconds),
        }

        grant = jwt.encode(claim_set, service_key["private_key"], algorithm="RS256")
        payload = {"grant_type": GRANT_TYPE, "assertion": grant}
        try:
            response = requests.post(service_key["token_uri"], data=payload)
            response.raise_for_status()
        except HTTPError as exception:
            raise AuthorizationFailed(exception)

        bearer_token = response.json()["access_token"]
        session.headers.update({"Authorization": f"Bearer {bearer_token}"})
        session.gever_token_expiration = claim_set["exp"]


def unfrozen_time(*args, **kwargs):
    """In testing, we want to be able to freeze the time. But we never want to freeze
    the time when generating JWT access tokens for accessing other systems.
    The unfrozen_time function makes sure to always return a real time, no matter
    whether the time is frozen or the freezegun is even installed.
    """
    try:
        from freezegun.api import real_time
    except ImportError:
        return time.time(*args, **kwargs)
    else:
        return real_time(*args, **kwargs)
