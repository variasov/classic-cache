import pytest
import time
import msgspec

from classic.cache import CachedValue


@pytest.fixture(scope='function')
def cached_value():
    return CachedValue(1.0, ttl=120)


@pytest.fixture(scope='function')
def cached_value_type():
    return msgspec.defstruct(
        'CachedValue',
        [
            ('value', float),
            ('ttl', int | None, None),
            ('created', float, msgspec.field(default_factory=time.monotonic)),
        ]
    )
