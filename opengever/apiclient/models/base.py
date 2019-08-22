from .registry import ModelRegistry


class APIModel:

    def __init__(self, item):
        if not isinstance(item, dict):
            raise ValueError(f'Expected dict, got {type(item).__name__}')
        if not item.get('@type'):
            raise ValueError(f'Missing @type in item.')
        if self.portal_type not in (item['@type'], '_unknown_'):
            raise ValueError(f'Invalid portal_type {item["@type"]} for {type(self)!r}')
        self.update_item(item)

    def update_item(self, item):
        self.item = item

    def __getattr__(self, *args, **kwargs):
        return self.item.get(*args, **kwargs)

    @property
    def url(self):
        return self.item['@id']

    @property
    def parent(self):
        """Parent object.
        """
        return ModelRegistry.wrap(self.item['parent'])


@ModelRegistry.register
class BaseModel(APIModel):
    portal_type = '_unknown_'
