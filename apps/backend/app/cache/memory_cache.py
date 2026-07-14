class MemoryCache:
    def __init__(self) -> None:
        self._cache: dict[str, object] = {}

    def get(
        self,
        key: str,
    ):
        return self._cache.get(key)

    def set(
        self,
        key: str,
        value,
    ) -> None:
        self._cache[key] = value

    def exists(
        self,
        key: str,
    ) -> bool:
        return key in self._cache

    def clear(
        self,
    ) -> None:
        self._cache.clear()