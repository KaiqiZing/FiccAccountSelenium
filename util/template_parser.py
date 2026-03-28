# util/template_parser.py
import re
import random  # 引入 Python 自带的随机库
from util.context_manager import GlobalContext


class TemplateParser:
    _func_registry = {}

    @classmethod
    def register_module(cls, module_obj):
        for attr_name in dir(module_obj):
            if not attr_name.startswith("_"):
                attr = getattr(module_obj, attr_name)
                if callable(attr):
                    cls._func_registry[attr_name] = attr

    @classmethod
    def register_functions(cls, mapping):
        """显式注册占位符名 -> 可调用对象（推荐，避免整模块扫描）。"""
        for name, fn in mapping.items():
            cls._func_registry[name] = fn

    @classmethod
    def parse_value(cls, value):
        if not isinstance(value, str):
            return value

        # ==========================================
        # 👉 新增补丁：原生支持 YAML 中的 {random} 快捷语法
        # ==========================================
        if "{random}" in value:
            # 自动生成 4 位随机数字（对应你 yaml 全局配置里的 random_length: 4）
            rand_num = str(random.randint(1000, 9999))
            # 将字符串中的 {random} 全部替换为这个随机数字
            value = value.replace("{random}", rand_num)

        # ==========================================
        # 下面保留原有的标准高级语法 ${func_name} 解析逻辑
        # ==========================================
        pattern = r'\$\{(.*?)\}'
        matches = re.findall(pattern, value)

        for placeholder in matches:
            real_val = None
            if placeholder.startswith("ctx."):
                ctx_key = placeholder.split(".", 1)[1]
                real_val = GlobalContext.get(ctx_key)
            elif placeholder in cls._func_registry:
                real_val = cls._func_registry[placeholder]()

            if real_val is not None:
                if value == f"${{{placeholder}}}":
                    return real_val
                value = value.replace(f"${{{placeholder}}}", str(real_val))

        return value

    @classmethod
    def parse_data(cls, data):
        """递归解析字典和列表"""
        if isinstance(data, dict):
            return {k: cls.parse_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [cls.parse_data(i) for i in data]
        return cls.parse_value(data)