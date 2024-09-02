from abc import ABC, abstractmethod
from typing import Mapping, Optional, Sequence

from .key_generator import FuncKeyCreator
from .typings import KeyType, ValueType
from .value import CachedValue


class Cache(ABC):
    """
    Базовый интерфейс кэширования элементов (ключ-значение + поддержка TTL)
    """

    key_function: FuncKeyCreator
    """
    Реализация хэширования функции и ее аргументов
    """

    @abstractmethod
    def set(
        self,
        key: KeyType,
        value: ValueType,
        ttl: Optional[int] = None
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
        elements: Mapping[KeyType, ValueType],
        ttl: Optional[int] = None
    ) -> None:
        """
        Сохранение множества элементов `elements` в кэше
        :param elements: ключи доступа и значения элементов
        :param ttl: время "жизни"
            (как долго элемент может находиться в кэше)
        """

    @abstractmethod
    def get(self, key: KeyType) -> Optional[CachedValue]:
        """
        Получение сохраненного элемента из кэша
        :param key: ключ доступа к элементу
        :return: Элемент, если он существует и не просрочен, иначе `None`
        """
        ...

    @abstractmethod
    def get_many(self, keys: Sequence[KeyType]) -> Mapping[KeyType, ValueType]:
        """
        Получение множества сохраненных элементов из кэша
        :param keys: ключи доступа к элементам
        :return: Словарь ключей и элементов,
            которые существуют в кэше и не являются просроченными
        """

    @abstractmethod
    def invalidate(self, key: KeyType) -> None:
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
