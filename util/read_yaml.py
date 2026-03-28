# util/read_yaml.py
import yaml
from util.template_parser import TemplateParser

class ReadYaml:
    def __init__(self, file_path):
        self.file_path = file_path # 路径逻辑参考之前

    def get_decoded_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            raw_data = yaml.safe_load(f)
            # 核心：返回前进行动态解析
            return TemplateParser.parse_data(raw_data)