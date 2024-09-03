"""
Модуль кэширования (заготовка к библиотеке evraz-cache)
"""
from . import caches, key_generators
from .cache import Cache
from .decorator import cache
from .key_generator import FuncKeyCreator
from .value import CachedValue

__all__ = (
    caches, key_generators, Cache, CachedValue, cache,
    FuncKeyCreator
)
