from .registry import ModelRegistry


class APIModel:

    def __init__(self, raw):
        if not isinstance(raw, dict):
            raise ValueError(f'Expected dict, got {type(raw).__name__}')
        if not raw.get('@type'):
            raise ValueError(f'Missing @type in raw.')
        if self.portal_type not in (raw['@type'], '_unknown_'):
            raise ValueError(f'Invalid portal_type {raw["@type"]} for {type(self)!r}')
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
        return ModelRegistry.wrap(self.raw['parent'])


@ModelRegistry.register
class BaseModel(APIModel):
    portal_type = '_unknown_'
