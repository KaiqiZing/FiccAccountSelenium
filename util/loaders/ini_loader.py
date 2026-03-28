# coding=utf-8
import os
from typing import Any

from util.loaders.base_loader import BaseLoader
from util.read_ini import BASE_DIR, ReadIni


def _resolve_ini_path(file_name: str) -> str:
    """与 ReadIni.__init__ 中 self.file_name 规则一致，用于稳定 cache_key。"""
    if file_name.startswith("../"):
        return os.path.join(BASE_DIR, file_name.replace("../", ""))
    return file_name


class IniLoader(BaseLoader):
    """INI 配置：静态缓存，元素定位运行期不变。"""

    CACHE_STRATEGY = "static"

    @property
    def source_type(self) -> str:
        return "ini"

    def load(self, source_id: Any, **kwargs: Any) -> Any:
        return ReadIni(source_id)

    def cache_key(self, source_id: Any, **kwargs: Any) -> str:
        if not isinstance(source_id, str):
            return f"{self.source_type}::{source_id}"
        return f"{self.source_type}::{_resolve_ini_path(source_id)}"
