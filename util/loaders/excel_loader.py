# coding=utf-8
import os
from typing import Any

from util.loaders.base_loader import BaseLoader
from AccountUtils.AccountExcelUtil import ExcelUtil


class ExcelLoader(BaseLoader):
    """Excel 测试数据：静态缓存。"""

    CACHE_STRATEGY = "static"

    @property
    def source_type(self) -> str:
        return "excel"

    def load(self, source_id: Any, **kwargs: Any) -> Any:
        sheet_index = kwargs.get("sheet_index", 0)
        return ExcelUtil(excel_path=source_id, index=sheet_index).get_data()

    def cache_key(self, source_id: Any, **kwargs: Any) -> str:
        sheet_index = kwargs.get("sheet_index", 0)
        path = os.path.abspath(source_id) if isinstance(source_id, str) else source_id
        return f"{self.source_type}::{path}::{sheet_index}"
