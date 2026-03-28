# util/read_yaml.py
import yaml
import os

class ReadYaml:
    def __init__(self, file_name):
        # 路径拼接逻辑建议参考你 read_ini.py 里的绝对路径实现
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = os.path.join(base_dir, "config", "test_data_yaml", file_name)

    def get_raw_data(self):
        """仅负责从磁盘读取原始 YAML 结构"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)



