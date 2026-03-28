# coding=utf-8
"""
供 YAML 模板 ${函数名} 使用的白名单注册，避免整模块反射注册导致误注册类/常量。
"""
from __future__ import annotations

from typing import Any, Dict


def _build_registry() -> Dict[str, Any]:
    from AccountUtils.generators import common, contact, finance, id_card, tax

    return {
        "RandomIDCards": id_card.RandomIDCards,
        "RandomEmail": contact.RandomEmail,
        "generate_random_phone_number": contact.generate_random_phone_number,
        "random_param": contact.random_param,
        "random_param_ZZbank": finance.random_param_ZZbank,
        "calendar_time": common.calendar_time,
        "finance_info_number": finance.finance_info_number,
        "generate_tax_id": tax.generate_tax_id,
        "generate_random_tax_id": tax.generate_random_tax_id,
    }


def register_template_generators() -> None:
    """将白名单函数注册到 TemplateParser（应在进程内只调用一次）。"""
    from util.template_parser import TemplateParser

    reg = _build_registry()
    TemplateParser.register_functions(reg)


def get_whitelist_names() -> tuple:
    """便于测试或文档列出允许的占位符函数名。"""
    return tuple(sorted(_build_registry().keys()))
