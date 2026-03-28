# coding=utf-8
import os
from util.read_yaml import ReadYaml
from util.template_parser import TemplateParser
# 仅在 DataManager 中关联业务模块，实现 Engine 与业务的解耦
from AccountUtils import AccountInfoSet


class DataManager:
    _instance = None
    _initialized = False
    _cache = {"yaml": {}, "ini": {}, "excel": {}}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DataManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not DataManager._initialized:
            # 核心：将业务工具类的方法“注入”到解析引擎中
            TemplateParser.register_module(AccountInfoSet)
            DataManager._initialized = True

    def get_yaml(self, file_name, is_parse=True):
        """
        获取 YAML 数据（非列表格式字典）
        由于 YAML 不是 - 开头，返回的是一个嵌套字典
        """
        if file_name not in self._cache["yaml"]:
            # 修正：直接获取原始数据存入缓存
            reader = ReadYaml(file_name)
            self._cache["yaml"][file_name] = reader.get_raw_data()

        raw_data = self._cache["yaml"][file_name]
        return TemplateParser.parse_data(raw_data) if is_parse else raw_data


if __name__ == "__main__":
    all_data = DataManager().get_yaml("test_data.yaml")
    # 2. 按页面获取数据块
    page1 = all_data.get("page1_basic_info")
    page2 = all_data.get("page2_department_role")

    # 3. 此时 page1['username'] 已经是经过解析的真实随机值了
    print(page1)