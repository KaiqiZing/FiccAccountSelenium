# coding=utf-8
"""
统一数据工厂：YAML / INI / Excel / DB 按需加载与分策略缓存。
"""
from typing import Any, Optional

from log.user_log import get_logger
from util.cache_manager import CacheManager
from util.template_parser import TemplateParser

logger = get_logger()


class DataFactory:
    """单例入口，兼容原 DataManager.get_yaml 等用法。"""

    _instance: Optional["DataFactory"] = None
    _initialized = False

    def __new__(cls, *args: Any, **kwargs: Any) -> "DataFactory":
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if DataFactory._initialized:
            return
        self._cache = CacheManager()
        self._loaders: dict[str, Any] = {}
        self._register_default_loaders()
        from AccountUtils.template_generators import register_template_generators

        register_template_generators()
        DataFactory._initialized = True

    def _register_default_loaders(self) -> None:
        from util.loaders.excel_loader import ExcelLoader
        from util.loaders.ini_loader import IniLoader
        from util.loaders.yaml_loader import YamlLoader

        self.register_loader(YamlLoader())
        self.register_loader(IniLoader())
        self.register_loader(ExcelLoader())

    def register_loader(self, loader: Any) -> None:
        """注册或替换某类数据源的 Loader（如 DbLoader）。"""
        self._loaders[loader.source_type] = loader

    def get(self, source_type: str, source_id: Any, parse: bool = True, **kwargs: Any) -> Any:
        """
        统一数据获取入口。
        :param source_type: yaml / ini / excel / db
        :param source_id: 文件名或 SQL
        :param parse: 是否对结果走 TemplateParser（YAML 模板解析）
        """
        loader = self._loaders.get(source_type)
        if not loader:
            raise ValueError(f"未注册的数据源类型: {source_type}")

        key = loader.cache_key(source_id, **kwargs)
        strategy = loader.CACHE_STRATEGY

        if strategy == "static":
            cached = self._cache.get(key)
            if cached is not None:
                return cached
            data = loader.load(source_id, **kwargs)
            if parse and isinstance(data, (dict, list)):
                data = TemplateParser.parse_data(data)
            self._cache.set(key, data)
            return data

        if strategy == "template":
            cached_raw = self._cache.get(key)
            if cached_raw is None:
                cached_raw = loader.load(source_id, **kwargs)
                self._cache.set(key, cached_raw)
            return TemplateParser.parse_data(cached_raw) if parse else cached_raw

        if strategy == "volatile":
            cached = self._cache.get(key)
            if cached is not None:
                return cached
            data = loader.load(source_id, **kwargs)
            if parse and isinstance(data, (dict, list)):
                data = TemplateParser.parse_data(data)
            ttl = getattr(loader, "CACHE_TTL", None)
            self._cache.set(key, data, ttl=ttl)
            return data

        raise ValueError(f"未知的缓存策略: {strategy}")

    def get_yaml(self, file_name: str, is_parse: bool = True) -> Any:
        """获取 YAML 测试数据（与原 DataManager 签名一致）。"""
        return self.get("yaml", file_name, parse=is_parse)

    def get_ini(self, file_name: str) -> Any:
        """获取 INI 读取器实例（已缓存）。"""
        return self.get("ini", file_name, parse=False)

    def get_excel(self, file_name: str, sheet_index: int = 0) -> Any:
        """获取 Excel 二维数据（已缓存）。"""
        return self.get("excel", file_name, parse=False, sheet_index=sheet_index)

    def get_db(self, sql: str, params: Optional[tuple] = None) -> Any:
        """执行 SQL 并返回字典行列表（需先 register_loader(DbLoader(...))）。"""
        return self.get("db", sql, parse=False, params=params or ())

    def clear_cache(self, source_type: Optional[str] = None) -> None:
        if source_type:
            self._cache.clear(prefix=f"{source_type}::")
            logger.info("缓存已清除: %s", source_type)
        else:
            self._cache.clear()
            logger.info("缓存已清除: 全部")

    @property
    def cache_stats(self) -> dict:
        return self._cache.stats

