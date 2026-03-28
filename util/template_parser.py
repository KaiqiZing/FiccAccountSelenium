# util/template_parser.py
import re
from AccountUtils.AccountInfoSet import AccountInfoSet  # 引入你现有的工具
from util.context_manager import GlobalContext


class TemplateParser:
    @staticmethod
    def parse_value(value):
        """解析字符串中的占位符"""
        if not isinstance(value, str):
            return value

        # 1. 处理动态函数，如 ${generate_random_phone_number}
        # 匹配 ${func_name}
        func_match = re.findall(r'\$\{(.*?)\}', value)
        for func_name in func_match:
            # 如果函数存在于 AccountInfoSet 中，则调用它
            if hasattr(AccountInfoSet, func_name):
                real_val = getattr(AccountInfoSet, func_name)()
                value = value.replace(f'${{{func_name}}}', str(real_val))

            # 2. 处理上下文变量，如 ${ctx.user_id}
            elif func_name.startswith("ctx."):
                ctx_key = func_name.split(".")[1]
                real_val = GlobalContext.get(ctx_key)
                value = value.replace(f'${{{func_name}}}', str(real_val))

        return value

    @classmethod
    def parse_data(cls, data):
        """递归解析整个数据结构（列表或字典）"""
        if isinstance(data, dict):
            return {k: cls.parse_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [cls.parse_data(i) for i in data]
        else:
            return cls.parse_value(data)