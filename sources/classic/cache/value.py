import time
from typing import Any
from dataclasses import dataclass, field


@dataclass
class CachedValue:
    """
    Хранимое значение в кэше с дополнительной метаинформацией
    """
    value: Any
    """Значение элемента из кэша"""

    ttl: int | None = None
    """Время "жизни" элемента в кэше (секунды), None - "живет" бесконечно"""

    created: int = field(default_factory=time.time)
    """Время создания элемента в формате timestamp"""
