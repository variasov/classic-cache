"""
Модуль кэширования (заготовка к библиотеке evraz-cache)
"""
from . import caches, key_generators, serializers
from .cache import Cache
from .decorator import cache
from .key_generator import FuncKeyCreator
from .serializer import Serializer
from .value import CachedValue

__all__ = (
    caches, serializers, key_generators, Cache, CachedValue, Serializer, cache,
    FuncKeyCreator
)
