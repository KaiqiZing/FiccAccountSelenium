# coding=utf-8
from abc import ABC, abstractmethod
from typing import Any


class BaseLoader(ABC):
    """数据源加载器抽象基类。"""

    CACHE_STRATEGY: str = "static"  # static | template | volatile
    CACHE_TTL: float | None = None  # 仅 volatile 使用，单位：秒

    @property
    @abstractmethod
    def source_type(self) -> str:
        """数据源类型标识，如 yaml / ini / excel / db。"""

    @abstractmethod
    def load(self, source_id: Any, **kwargs: Any) -> Any:
        """从数据源加载原始数据。"""

    def cache_key(self, source_id: Any, **kwargs: Any) -> str:
        """生成缓存键，子类可覆写。"""
        return f"{self.source_type}::{source_id}"
