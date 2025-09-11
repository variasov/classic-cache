# Classic Cache

Classic Cache - предоставляет функциональность кеширования.
Предоставляет утилиты для пометки кеша, бекенд для кеширования в RAM
и бекенд для кешироавния в Redis.

## Установка

Для установки Classic-Cache вы можете использовать pip:

```bash
pip install classic-cache
```

Для установки Classic-Cache с поддержкой Redis:

```bash
pip install classic-cache[redis]
```

## Использование

```python
from classic.cache import cached, InMemoryCache, RedisCache
from classic.components import component

@component
class SomeClass:

    # Кэширование результата метода some_method на 60 секунд
    @cached(ttl=60)
    def some_method(self, arg1: int, arg2: int) -> int:
        return arg1 + arg2

# кеширование в памяти
cache = InMemoryCache()
# ИЛИ
# кеширование в Redis
cache = RedisCache(connection=Redis())

some_instance = SomeClass(cache=cache)

# ручная инвалидация кэша
some_instance.some_method.invalidate(1, 2)
# ручное обновление кэша
some_instance.some_method.refresh(1, 2)
```
