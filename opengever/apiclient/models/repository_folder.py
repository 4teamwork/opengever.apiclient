from .base import APIModel
from .registry import ModelRegistry


@ModelRegistry.register
class RepositoryFolder(APIModel):
    portal_type = 'opengever.repository.repositoryfolder'
