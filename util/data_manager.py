# coding=utf-8
import os
from util.read_ini import ReadIni
from util.read_yaml import ReadYaml
from AccountUtils.AccountExcelUtil import ExcelUtil
from util.template_parser import TemplateParser
from log.user_log import get_logger

logger = get_logger()


class DataManager:
    """
    统一数据管理中心（单例缓存仓库）
    支持：INI、YAML、Excel 文件的缓存加载与动态解析
    """
    _instance = None
    _cache = {
        "ini": {},  # 存储 ReadIni 实例
        "yaml": {},  # 存储 原始 YAML 数据
        "excel": {}  # 存储 原始 Excel 数据列表
    }

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DataManager, cls).__new__(cls)
        return cls._instance

    def get_ini(self, file_path):
        """缓存加载 INI 配置"""
        if file_path not in self._cache["ini"]:
            logger.info(f"💾 磁盘读取 INI 文件: {file_path}")
            self._cache["ini"][file_path] = ReadIni(file_path)
        return self._cache["ini"][file_path]

    def get_yaml(self, file_path, is_parse=True):
        """缓存加载并动态解析 YAML 数据"""
        if file_path not in self._cache["yaml"]:
            logger.info(f"💾 磁盘读取 YAML 文件: {file_path}")
            # 这里调用之前的 ReadYaml 工具
            reader = ReadYaml(file_path)
            self._cache["yaml"][file_path] = reader.get_raw_data()

        data = self._cache["yaml"][file_path]
        return TemplateParser.parse_data(data) if is_parse else data

    def get_excel(self, file_path, is_parse=True):
        """缓存加载并动态解析 Excel 数据"""
        if file_path not in self._cache["excel"]:
            logger.info(f"💾 磁盘读取 Excel 文件: {file_path}")
            excel_util = ExcelUtil(file_path)
            self._cache["excel"][file_path] = excel_util.get_data()

        data = self._cache["excel"][file_path]
        return TemplateParser.parse_data(data) if is_parse else data

    def clear_all_cache(self):
        """清理所有缓存（用于内存回收）"""
        for key in self._cache:
            self._cache[key].clear()
        logger.info("🧹 全局文件缓存已清理")