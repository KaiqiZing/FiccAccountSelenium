# coding=utf-8
from typing import Any

from util.loaders.base_loader import BaseLoader
from util.read_yaml import ReadYaml


class YamlLoader(BaseLoader):
    """YAML 测试数据：缓存原始模板，每次解析生成新随机值。"""

    CACHE_STRATEGY = "template"

    @property
    def source_type(self) -> str:
        return "yaml"

    def load(self, source_id: Any, **kwargs: Any) -> Any:
        return ReadYaml(source_id).get_raw_data()

    def cache_key(self, source_id: Any, **kwargs: Any) -> str:
        return f"{self.source_type}::{source_id}"
