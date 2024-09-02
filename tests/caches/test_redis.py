from dataclasses import dataclass
from datetime import datetime

import pytest
from fakeredis import FakeRedis
from freezegun import freeze_time

from classic.cache import Cache, CachedValue
from classic.cache.caches import RedisCache


@dataclass(frozen=True)
class FrozenDataclass:
    x: int
    y: int


# реализации кэширования (дополняем при необходимости)
@pytest.fixture(scope='function')
def redis_cache():
    return RedisCache(connection=FakeRedis())


# ссылки на экземпляров реализации кэшей (используем название фикстуры)
cache_instances = ('redis_cache', )


# параметизированный экземпляр кэша (request.param - фикстура с реализацией)
@pytest.fixture(scope='function')
def cache_instance(request) -> Cache:
    return request.getfixturevalue(request.param)


@pytest.fixture(scope='function')
def next_year():
    today = datetime.today()
    return datetime(year=today.year + 1, month=today.month, day=today.day)


# interface tests


@pytest.mark.parametrize('cache_instance', cache_instances, indirect=True)
def test_get_set_without_ttl(cache_instance, cached_value):
    key = 'test'

    cache_instance.set(key, cached_value.value)
    cache_result = cache_instance.get(key)

    assert (
        cache_result and cache_result.value == cached_value.value
        and cache_result.ttl is None
    )


@pytest.mark.parametrize('cache_instance', cache_instances, indirect=True)
def test_get_set_with_ttl(cache_instance, cached_value):
    key = 'test'

    cache_instance.set(key, cached_value.value, cached_value.ttl)
    cache_result = cache_instance.get(key)

    assert (
        cache_result and cache_result.value == cached_value.value
        and cache_result.ttl == cached_value.ttl
    )


@pytest.mark.parametrize('cache_instance', cache_instances, indirect=True)
def test_get_set_expired(cache_instance, cached_value, next_year):
    key = 'test'

    cache_instance.set(key, cached_value.value, cached_value.ttl)

    # make sure that the cached value is expired by using 1 year gap
    with freeze_time(next_year):
        assert cache_instance.get(key) is None


@pytest.mark.parametrize('cache_instance', cache_instances, indirect=True)
def test_get_set_many_without_ttl(cache_instance, cached_value):
    keys = [f'test_{index}' for index in range(5)]
    expected = {key: CachedValue(cached_value.value) for key in keys}

    cache_instance.set_many(
        {key: element.value
         for key, element in expected.items()}
    )

    result = cache_instance.get_many(keys)

    assert {*result.keys()} == {*expected.keys()}

    for key, element in result.items():
        expected_element: CachedValue = expected[key]
        assert (
            expected_element.value == element.value
            and expected_element.ttl == expected_element.ttl
        )


@pytest.mark.parametrize('cache_instance', cache_instances, indirect=True)
def test_get_set_many_with_ttl(cache_instance, cached_value):
    keys = [f'test_{index}' for index in range(5)]
    expected = {key: cached_value for key in keys}

    cache_instance.set_many(
        {key: element.value
         for key, element in expected.items()}, cached_value.ttl
    )

    result = cache_instance.get_many(keys)

    assert {*result.keys()} == {*expected.keys()}

    for key, element in result.items():
        expected_element: CachedValue = expected[key]
        assert (
            expected_element.value == element.value
            and expected_element.ttl == expected_element.ttl
        )


@pytest.mark.parametrize('cache_instance', cache_instances, indirect=True)
def test_get_set_many_expired(cache_instance, cached_value, next_year):
    keys = [f'test_{index}' for index in range(5)]

    cache_instance.set_many(
        {key: cached_value.value
         for key in keys}, cached_value.ttl
    )

    with freeze_time(next_year):
        assert not cache_instance.get_many(keys)


@pytest.mark.parametrize('cache_instance', cache_instances, indirect=True)
def test_get_set_many_partial(cache_instance, cached_value, next_year):
    non_expired_key = 'test_0'
    expired_keys = [f'test_{index}' for index in range(1, 55)]
    all_keys = [non_expired_key, *expired_keys]

    cache_instance.set(non_expired_key, CachedValue(cached_value.value))
    cache_instance.set_many(
        {key: cached_value.value
         for key in expired_keys}, cached_value.ttl
    )

    with freeze_time(next_year):
        result = cache_instance.get_many(all_keys)
        assert len(result) == 1


@pytest.mark.parametrize('cache_instance', cache_instances, indirect=True)
def test_invalidate(cache_instance, cached_value):
    key = 'test'

    cache_instance.set(key, cached_value.value)
    cache_instance.invalidate(key)

    assert cache_instance.get(key) is None


@pytest.mark.parametrize('cache_instance', cache_instances, indirect=True)
def test_invalidate_all(cache_instance, cached_value):
    keys = [f'test_{index}' for index in range(5)]
    expected = {key: cached_value.value for key in keys}

    cache_instance.set_many(expected, cached_value.ttl)
    cache_instance.invalidate_all()

    assert not cache_instance.get_many(keys)


@pytest.mark.parametrize(
    'key,expected', [
        (1, bytes), ('str', bytes), (datetime(2023, 12, 31), bytes),
        (FrozenDataclass(1, 2), bytes)
    ]
)
def test_serialize_key(request, key, expected):
    # пример с множественными параметрами теста
    for cache in cache_instances:
        instance = request.getfixturevalue(cache)

        encoded_key = instance._serialize_key(key)
        assert isinstance(encoded_key, expected)
