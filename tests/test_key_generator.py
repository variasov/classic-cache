from typing import Optional

import pytest

from classic.cache import key_generators


def empty_args_function():
    return 'test'


def optional_kwargs_function(
    optional_arg: Optional[int] = None
) -> Optional[int]:
    return optional_arg


def args_function(a: int, b: int) -> int:
    return a + b


def kwargs_function(**kwargs):
    return kwargs


class A:

    def args_function(self, a: int, b: int) -> int:
        return a + b

    @classmethod
    def classmethod_function(cls, a: Optional[int] = None) -> Optional[int]:
        return a


# пример наследования
class B(A):
    ...


# экземпляры генераторов ключей функций+аргументов
generators = [
    key_generators.PureHash(),
    key_generators.Blake2b(),
    key_generators.OrJson()
]


@pytest.mark.parametrize('generator', generators)
def test_empty_args_function(generator):
    key = generator(empty_args_function)

    assert isinstance(key, str)
    assert generator.MODULE_SEP in key and generator.ARGS_SEP not in key


@pytest.mark.parametrize(
    'kwargs,expected_token', [({}, False), ({
        'optional_arg': 1
    }, True)]
)
def test_optional_kwargs_function(kwargs, expected_token):
    for generator in generators:

        key = generator(optional_kwargs_function, **kwargs)
        if not expected_token:
            assert generator.ARGS_SEP not in key
        else:
            assert generator.ARGS_SEP in key


@pytest.mark.parametrize('generator', generators)
def test_function_hashing_args(generator):
    key_a = generator(args_function, 0, 1)
    key_b = generator(args_function, 1, 0)

    assert key_a != key_b


@pytest.mark.parametrize('generator', generators)
def test_function_hashing_kwargs(generator):
    # Порядок аргументов в kwargs не должен влиять на итоговый ключ

    key_a = generator(kwargs_function, a=1, b=2)
    key_b = generator(kwargs_function, b=2, a=1)

    assert key_a == key_b


@pytest.mark.parametrize('generator', generators)
def test_class_function(generator):
    key = generator(A().args_function, 0, 1)

    assert A.__name__ in key


@pytest.mark.parametrize('generator', generators)
def test_same_function_different_scopes(generator):
    key_a = generator(A().args_function, 0, 1)
    key_b = generator(args_function, 0, 1)

    assert key_a != key_b


@pytest.mark.parametrize('generator', generators)
def test_same_function_different_classes(generator):
    key_a = generator(A().args_function, 0, 1)
    key_b = generator(B().args_function, 0, 1)

    assert key_a != key_b


@pytest.mark.parametrize('generator', generators)
def test_classmethods(generator):
    key_a = generator(A.classmethod_function)
    key_b = generator(B.classmethod_function)

    assert key_a != key_b


# specific key generators
@pytest.mark.parametrize('generator', [key_generators.PureHash()])
def test_non_hashable_structures(generator):
    with pytest.raises(AssertionError):
        generator(optional_kwargs_function, {'optional_arg': {'a': 1, 'b': 2}})
