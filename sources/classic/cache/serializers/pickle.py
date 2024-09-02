from pickle import dumps, loads
from typing import Any

from ..serializer import Serializer
from ..typings import EncodedValueType


class PickleSerializer(Serializer):
    """
    Сериализация/десериализация объектов на основе стандартного модуля `pickle`
    """

    def serialize(self, element: Any) -> EncodedValueType:
        return dumps(element)

    def deserialize(self, element: EncodedValueType) -> Any:
        return loads(element)
