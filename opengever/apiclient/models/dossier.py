from .base import APIModel
from .registry import ModelRegistry


@ModelRegistry.register
class Dossier(APIModel):
    portal_type = 'opengever.dossier.businesscasedossier'
