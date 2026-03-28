# coding=utf-8
"""金融类随机编号。"""
import random


def random_param_ZZbank():
    """生成随机理财号码"""
    param = random.randint(100000, 999999)
    return "Z7000924" + str(param)


def finance_info_number():
    """生成金融账号"""
    Bstr = "B2128S"
    param = random.randint(200000000, 999999999)
    return Bstr + str(param)
