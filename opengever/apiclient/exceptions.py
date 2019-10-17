from . import LOG
from .keys import KeyRegistry


class APIException(Exception):
    """Base class for all GEVER API exceptions.
    """


class ServiceKeyMissing(APIException):

    def __init__(self, url):
        try:
            known_key_urls = repr(tuple(KeyRegistry.keys.keys()))
        except Exception as exc:
            LOG.exception(exc)
            known_key_urls = '????'

        try:
            key_dirs = KeyRegistry.get_key_dirs()
        except Exception as exc:
            LOG.exception(exc)
            key_dirs = '????'

        super().__init__(f'No GEVER service key found for URL {url}.\n'
                         f'Found keys {known_key_urls} in paths {key_dirs}')


class APIRequestException(APIException):
    """Base class for exceptions when making a request to gever.

    This base class can be used to build custom exception classes which will then
    be raised by the GEVER API client when something bad happens in the communication
    with the GEVER system.

    A log message is emitted automatically when one of the custom exceptions
    is instantiated.
    """

    default_message = "Request to GEVER failed."

    def __init__(self, original_exception=None, message=None):
        """
        :param original_exception: An instance of an exception. Will be logged too.
        :param message: A custom message to be logged. Useful for debugging.
        """
        self.original_exception = original_exception
        self.message = message or self.default_message
        self._emit_log(original_exception)

    def _emit_log(self, original_exception):
        LOG.exception(original_exception)
        msgs = [__class__.__name__]

        if self.message:
            msgs.append(self.message)

        if self.original_exception:
            msgs.append(f"Original exception: {self.original_exception}.")

            if hasattr(self.original_exception, "response") and self.original_exception.response.text:
                msgs.append(f"Response from GEVER: {self.original_exception.response.text}")

        LOG.exception("\n".join(msgs))

    @classmethod
    def emit_log(cls, exception):
        cls(exception)


class AuthorizationFailed(APIRequestException):
    default_message = (
        "An error occurred while acquiring the GEVER token. "
        "Maybe your API key is corrupt or invalid."
    )
