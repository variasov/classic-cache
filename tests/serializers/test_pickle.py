import pytest

from classic.cache import CachedValue, Serializer
from classic.cache.serializers import PickleSerializer


# реализации сериализатора (дополняем при необходимости)
@pytest.fixture(scope='function')
def pickle_serializer():
    return PickleSerializer()


# ссылки на экземпляров реализации кэшей (используем название фикстуры)
serializer_instances = ('pickle_serializer', )


# параметизированный экземпляр сериализатора
# (request.param - фикстура с реализацией)
@pytest.fixture(scope='function')
def serializer_instance(request) -> Serializer:
    return request.getfixturevalue(request.param)


@pytest.mark.parametrize(
    'serializer_instance', serializer_instances, indirect=True
)
def test_serialize_value(serializer_instance):
    value = CachedValue('tested_value', 200)
    encoded_value = serializer_instance.serialize(value)
    assert isinstance(encoded_value, bytes)


@pytest.mark.parametrize(
    'serializer_instance', serializer_instances, indirect=True
)
def test_deserialize_value(serializer_instance):
    value = CachedValue('tested_value', 200)
    encoded_value = serializer_instance.serialize(value)

    decoded_value = serializer_instance.deserialize(encoded_value)

    assert value == decoded_value
