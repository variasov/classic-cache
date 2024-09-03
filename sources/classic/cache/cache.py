from abc import ABC, abstractmethod
from typing import Mapping, Sequence, Any, Hashable

import msgspec

from .key_generator import FuncKeyCreator
from .value import CachedValue


class Cache(ABC):
    """
    Базовый интерфейс кэширования элементов (ключ-значение + поддержка TTL)
    """

    key_function: FuncKeyCreator
    """
    Реализация хэширования функции и ее аргументов
    """

    def _serialize(self, element: Any) -> bytes:
        return msgspec.json.encode(element)

    def _deserialize(self, element: bytes, type_) -> Any:
        return msgspec.json.decode(element, type=type_)

    @abstractmethod
    def set(
        self,
        key: Hashable,
        value: Any,
        type_,
        ttl: int | None = None
    ) -> None:
        """
        Сохранение элемента `element` в кэше
        :param key: ключ доступа к элементу
        :param value: значение элемента
        :param ttl: время "жизни"
            (как долго элемент может находиться в кэше)
        """
        ...

    @abstractmethod
    def set_many(
        self,
        elements: Mapping[Hashable, Any],
        ttl: int | None = None
    ) -> None:
        """
        Сохранение множества элементов `elements` в кэше
        :param elements: ключи доступа и значения элементов
        :param ttl: время "жизни"
            (как долго элемент может находиться в кэше)
        """

    @abstractmethod
    def get(self, key: Hashable, type_) -> CachedValue | None:
        """
        Получение сохраненного элемента из кэша
        :param key: ключ доступа к элементу
        :return: Элемент, если он существует и не просрочен, иначе `None`
        """
        ...

    @abstractmethod
    def get_many(self, keys: Sequence[Hashable]) -> Mapping[Hashable, Any]:
        """
        Получение множества сохраненных элементов из кэша
        :param keys: ключи доступа к элементам
        :return: Словарь ключей и элементов,
            которые существуют в кэше и не являются просроченными
        """

    @abstractmethod
    def invalidate(self, key: Hashable) -> None:
        """
        Удаление элемента из кэша
        :param key: ключ доступа к элементу
        """
        ...

    @abstractmethod
    def invalidate_all(self) -> None:
        """
        Удаление всех элементов из кэша
        """
        ...
