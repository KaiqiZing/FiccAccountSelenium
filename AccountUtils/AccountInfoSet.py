# -*- coding: utf-8 -*-
"""
项目数据生成集合（兼容层）。

实现已拆分：
- 行政区划数据：AccountUtils.data.area_info
- 生成器：AccountUtils.generators.*
- YAML 模板白名单注册：AccountUtils.template_generators
"""
from AccountUtils.data.area_info import AREA_INFO
from AccountUtils.generators.common import calendar_time
from AccountUtils.generators.contact import (
    RandomEmail,
    generate_random_phone_number,
    random_param,
)
from AccountUtils.generators.finance import finance_info_number, random_param_ZZbank
from AccountUtils.generators.id_card import (
    ID_NUMBER_15_REGEX,
    ID_NUMBER_18_REGEX,
    IdCardNumber,
    RandomIDCards,
)
from AccountUtils.generators.tax import generate_random_tax_id, generate_tax_id

__all__ = [
    "AREA_INFO",
    "ID_NUMBER_15_REGEX",
    "ID_NUMBER_18_REGEX",
    "IdCardNumber",
    "RandomIDCards",
    "RandomEmail",
    "generate_random_phone_number",
    "random_param",
    "random_param_ZZbank",
    "calendar_time",
    "finance_info_number",
    "generate_tax_id",
    "generate_random_tax_id",
]