from dataclasses import dataclass, field
from datetime import datetime

from .typings import ValueType


@dataclass
class CachedValue:
    """
    Хранимое значение в кэше с дополнительной метаинформацией
    """
    value: ValueType
    """Значение элемента из кэша"""

    ttl: int | None = None
    """Время "жизни" элемента в кэше (секунды), None - "живет" бесконечно"""

    created: datetime = field(default_factory=datetime.utcnow)
    """Время создания элемента"""
