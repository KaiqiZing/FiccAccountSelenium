# coding=utf-8
"""
向后兼容：DataManager 为 DataFactory 的别名。
新代码请优先使用 util.data_factory.DataFactory。
"""
from util.data_factory import DataFactory

DataManager = DataFactory

if __name__ == "__main__":
    all_data = DataManager().get_yaml("test_data.yaml")
    page1 = all_data.get("page1_basic_info")
    page2 = all_data.get("page2_department_role")
    print(page1)
    print(page2)
