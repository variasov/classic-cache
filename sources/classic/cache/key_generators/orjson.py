from typing import Any, Callable, Optional, Union

from orjson import dumps

from ..key_generator import FuncKeyCreator


class OrJson(FuncKeyCreator):
    """
    Персистентное хэширование функции и аргументов при помощи orjson
    """

    def __init__(
        self,
        options: Optional[int] = None,
        default: Optional[Callable[[Any], Any]] = None
    ):
        """
        Инициализация опций orjson (см. https://github.com/ijl/orjson)
        :param options: опции поведения сериализатора с помощью флагов
        :param default: callable для серилазации нестандартных типов данных
        """
        self.options = options
        self.default = default

    def hash_arguments(self, *args,
                       **kwargs) -> Union[Optional[int], Optional[str]]:
        if not (args or kwargs):
            return None

        kwargs = {key: kwargs[key] for key in sorted(kwargs.keys())}
        arguments = [*args, *[(key, value) for key, value in kwargs.items()]]

        return dumps(arguments, self.default, self.options).decode('utf8')
