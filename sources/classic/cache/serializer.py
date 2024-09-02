from abc import ABC, abstractmethod
from typing import Any

from .typings import EncodedValueType


class Serializer(ABC):
    """
    Базовый интерфейс сериализации/десериализации объектов
    """

    @abstractmethod
    def serialize(self, element: Any) -> EncodedValueType:
        """
        Перевод элемента `value` в битовое представление
        :param element: элемент для кэширования
        :return: битовое представление элемента
        """
        ...

    @abstractmethod
    def deserialize(self, element: EncodedValueType) -> Any:
        """
        Перевод элемента кэша из битового в объектное представление
        :param element: битовое представление элемента
        :return: элемент из кэша
        """
        ...
