from ..utils import singleton


@singleton
class ModelRegistry:

    def __init__(self):
        self.models = {}

    def register(self, model_class):
        if model_class.portal_type in self.models:
            raise ValueError(
                'Duplicate model registration for {model_class.portal_type!r} '
                '({model_class!r} and {self.models[model_class.portal_type!r]')

        self.models[model_class.portal_type] = model_class
        return model_class

    def get(self, portal_type, *args, **kwargs):
        """Returns the model for an @type.
        """
        return self.models.get(portal_type, *args, **kwargs)

    def wrap(self, item, client):
        """Wrap an item (dict from GEVER) into an object based on our models.
        """
        if not isinstance(item, dict):
            raise ValueError(f'Expected dict, got {type(item).__name__}')
        if not item.get('@type'):
            raise ValueError(f'Missing @type in item.')

        model = self.get(item.get('@type')) or self.get('_unknown_')
        return model(item, client)
