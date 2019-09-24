from urllib.parse import urljoin
from urllib.parse import urlparse

from .registry import ModelRegistry


class APIModel:

    def __init__(self, raw, client):
        if not isinstance(raw, dict):
            raise ValueError(f'Expected dict, got {type(raw).__name__}')
        if not raw.get('@type'):
            raise ValueError(f'Missing @type in raw.')
        if self.portal_type not in (raw['@type'], '_unknown_'):
            raise ValueError(f'Invalid portal_type {raw["@type"]} for {type(self)!r}')
        self.client = client.adopt(raw['@id'])
        self.update_item(raw)

    def update_item(self, raw):
        self.raw = raw

    def __getattr__(self, name):
        if name in self.raw:
            return self.raw.get(name)
        elif hasattr(super(), name):
            return getattr(super(), name)
        else:
            raise AttributeError(
                f'{type(self).__name__} object has no attribute {name}')

    def __eq__(self, other):
        return self.url == other.url

    @property
    def url(self):
        return self.raw['@id']

    @property
    def parent(self):
        """Parent object.
        """
        return self.client.wrap(self.raw['parent'])

    @property
    def items(self):
        """The children of the object.
        """
        return list(map(self.client.wrap, self.raw['items']))

    @property
    def id_path(self):
        return urlparse(self.raw['@id']).path

    @property
    def sequence_number(self):
        return int(self.id_path.split("-")[-1])

    def fetch(self):
        """Fetch this item from GEVER and update self.
        """
        self.update_item(self.client.fetch(raw=True))
        return self

    def has_addable_type(self, content_type):
        # Why the trailing slash?
        # https://stackoverflow.com/a/10893427/3906189
        types = self.client.session().get(urljoin(f'{self.url}/', '@types')).json()
        for gever_content_type in types:
            if gever_content_type['@id'].endswith(content_type):
                return gever_content_type['addable']
        return False


@ModelRegistry.register
class BaseModel(APIModel):
    portal_type = '_unknown_'
