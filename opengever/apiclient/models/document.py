from .base import APIModel
from .registry import ModelRegistry


@ModelRegistry.register
class Document(APIModel):
    portal_type = 'opengever.document.document'
