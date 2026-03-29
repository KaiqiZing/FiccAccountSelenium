# coding=utf-8
"""通用小工具。"""
import random
import string
import time


def calendar_time():
    """当前日期字符串 YYYY-MM-DD"""
    return time.strftime("%Y-%m-%d", time.localtime())


def generate_random_password(length: int = 12) -> str:
    """
    生成随机密码：至少包含大写、小写、数字、特殊字符各一个，其余随机填充。
    """
    if length < 4:
        length = 4

    upper = random.choice(string.ascii_uppercase)
    lower = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    special = random.choice("!@#$%&*")

    remaining = "".join(
        random.choices(string.ascii_letters + string.digits + "!@#$%&*", k=length - 4)
    )

    password = list(upper + lower + digit + special + remaining)
    random.shuffle(password)
    return "".join(password)
