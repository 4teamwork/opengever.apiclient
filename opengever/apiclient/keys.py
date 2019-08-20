from opengever.apiclient.utils import singleton
from pathlib import Path
import json
import os


@singleton
class KeyRegistry:
    """The KeyRegistry stores loads the keys from the "keys" filesystem directory
    and stores them for later use.
    It loads all keys from directories configured in "OPENGEVER_APICLIENT_KEY_DIRS"
    on process boot time.
    """

    def __init__(self):
        self.reset()

    def get_base_url_for(self, url):
        """Returns the GEVER client base url according to the known keys.
        """
        for gever_base_url in sorted(self.keys.keys()):
            if url.startswith(gever_base_url):
                return gever_base_url

    def get_key_for(self, url):
        """Returns the GEVER service key matching the given URL.
        """
        for gever_base_url, key in sorted(self.keys.items()):
            if url.startswith(gever_base_url):
                return key

    def clear(self):
        """Clear all keys from the registry.
        """
        self.keys = {}

    def reset(self):
        """Clear the keys registry and load the keys from the configured directories.
        """
        self.clear()
        self.load_default_keys()

    def get_key_dirs(self):
        """Return the configured list of key directory paths.
        """
        return tuple(filter(bool, os.environ.get(
            'OPENGEVER_APICLIENT_KEY_DIRS', '').split(os.pathsep)))

    def load_default_keys(self):
        """Load keys of the configured key directories.
        """
        for directory in self.get_key_dirs():
            self.load_keys(directory)

    def load_keys(self, directory):
        """Load keys of a specific directory.
        """
        for key in self._iter_keys(directory):
            if "token_uri" not in key:
                continue

            gever_base_url = key["token_uri"].replace("@@oauth2-token", "")
            self.keys[gever_base_url] = key

    def _iter_keys(self, directory):
        for key_file in Path(directory).glob("*.json"):
            yield json.loads(key_file.read_text())
