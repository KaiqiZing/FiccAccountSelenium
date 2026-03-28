# coding=utf-8
"""手机、邮箱等联系方式类随机数据。"""
import random
import string


def RandomEmail(emailtype=None, rang=None):
    """
    随机生成指定长度的邮箱
    :param emailtype: 可选 @qq.com, @163.com, @126.com, @sina.com, @189.com
    :param rang: 邮箱本地部分长度，默认 6-10
    """
    __emailtype = ["@qq.com", "@163.com", "@126.com", "@sina.com", "@189.com"]
    if emailtype is None:
        __randomemailtype = random.choice(__emailtype)
    else:
        __randomemailtype = emailtype
    if rang is None:
        __rangnum = random.randint(6, 10)
    else:
        __rangnum = int(rang)

    __mutiple_param = string.ascii_letters + string.digits
    __firstemail = "".join(random.choice(__mutiple_param) for i in range(__rangnum))
    return __firstemail + __randomemailtype


def generate_random_phone_number():
    """生成随机手机号码"""
    phone_prefixes = [
        "134",
        "135",
        "136",
        "137",
        "138",
        "139",
        "147",
        "150",
        "151",
        "152",
        "157",
        "158",
        "159",
        "172",
        "178",
        "182",
        "183",
        "184",
        "187",
        "188",
    ]
    prefix = random.choice(phone_prefixes)
    second_part = f"{random.randint(10000000, 99999999)}"
    return f"{prefix}{second_part}"


def random_param():
    """生成随机整数（历史命名，用于部分模板）"""
    return random.randint(1000000, 99999999)
