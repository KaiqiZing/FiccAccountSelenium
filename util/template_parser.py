# util/template_parser.py
import re
import random
from util.context_manager import GlobalContext

_DEFAULT_RANDOM_LENGTH = 4


def _get_random_length() -> int:
    try:
        from util.data_factory import DataFactory
        cfg = DataFactory().get_yaml("base_config.yaml", is_parse=False)
        return int((cfg.get("global_config") or {}).get("random_length", _DEFAULT_RANDOM_LENGTH))
    except Exception:
        return _DEFAULT_RANDOM_LENGTH


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

        if "{random}" in value:
            n = _get_random_length()
            low = 10 ** (n - 1)
            high = 10 ** n - 1
            rand_num = str(random.randint(low, high))
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
