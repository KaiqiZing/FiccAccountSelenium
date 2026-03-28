# coding=utf-8
import hashlib
from typing import Any, Callable, Optional

from util.loaders.base_loader import BaseLoader


class DbLoader(BaseLoader):
    """
    数据库查询：带 TTL 的易失缓存。
    需在注册时传入 connection_factory: () -> 数据库连接。
    """

    CACHE_STRATEGY = "volatile"
    CACHE_TTL = 300.0

    def __init__(self, connection_factory: Optional[Callable[[], Any]] = None) -> None:
        self._get_conn = connection_factory

    @property
    def source_type(self) -> str:
        return "db"

    def load(self, source_id: Any, **kwargs: Any) -> Any:
        if self._get_conn is None:
            raise RuntimeError(
                "DbLoader 未配置：请使用 register_loader(DbLoader(connection_factory=...)) 注入连接工厂"
            )
        sql = source_id
        params = kwargs.get("params") or ()
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            if cursor.description is None:
                return []
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def cache_key(self, source_id: Any, **kwargs: Any) -> str:
        sql = source_id if isinstance(source_id, str) else str(source_id)
        params = kwargs.get("params") or ()
        raw = sql.encode("utf-8") + repr(params).encode("utf-8")
        sql_hash = hashlib.md5(raw).hexdigest()[:16]
        return f"{self.source_type}::{sql_hash}"
