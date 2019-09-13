from .base import APIModel
from .registry import ModelRegistry


@ModelRegistry.register
class Document(APIModel):
    portal_type = 'opengever.document.document'

    @property
    def reference_number(self):
        return self.raw['reference_number']
