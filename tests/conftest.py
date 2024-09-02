import pytest

from classic.cache import CachedValue


@pytest.fixture(scope='function')
def cached_value():
    return CachedValue(1.0, ttl=120)
