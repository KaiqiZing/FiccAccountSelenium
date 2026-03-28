# coding=utf-8
"""统一缓存层：支持 TTL 与按前缀清除。"""
import time
from typing import Any, Optional

from log.user_log import get_logger

logger = get_logger()


class CacheEntry:
    __slots__ = ("data", "created_at", "ttl")

    def __init__(self, data: Any, ttl: Optional[float] = None):
        self.data = data
        self.created_at = time.time()
        self.ttl = ttl  # None 表示永不过期

    @property
    def is_expired(self) -> bool:
        if self.ttl is None:
            return False
        return (time.time() - self.created_at) > self.ttl


class CacheManager:
    def __init__(self) -> None:
        self._store: dict[str, CacheEntry] = {}

    def get(self, key: str) -> Any:
        entry = self._store.get(key)
        if entry is None:
            return None
        if entry.is_expired:
            del self._store[key]
            logger.info("缓存已过期，自动清除: %s", key)
            return None
        return entry.data

    def set(self, key: str, data: Any, ttl: Optional[float] = None) -> None:
        self._store[key] = CacheEntry(data, ttl)
        logger.debug("缓存写入: %s (TTL=%s)", key, ttl)

    def clear(self, prefix: Optional[str] = None) -> None:
        if prefix is None:
            self._store.clear()
            return
        keys_to_delete = [k for k in self._store if k.startswith(prefix)]
        for k in keys_to_delete:
            del self._store[k]

    @property
    def stats(self) -> dict:
        total = len(self._store)
        expired = sum(1 for e in self._store.values() if e.is_expired)
        return {"total": total, "active": total - expired, "expired": expired}
