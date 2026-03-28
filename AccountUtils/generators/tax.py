# coding=utf-8
"""税务相关随机编号。"""
import random


def _calculate_check_digit(tax_id):
    weights = [3, 7, 9, 10, 5, 8, 4, 2]
    total = sum(int(digit) * weight for digit, weight in zip(tax_id, weights))
    check_digit = str((11 - total % 11) % 11)
    return check_digit if check_digit != "10" else "X"


def generate_tax_id(birth_date):
    """国税证号示例生成（birth_date 为历史参数名）"""
    prefix = "1" + "".join(str(random.randint(0, 9)) for _ in range(16))

    def calc_check_digit(pfx):
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        checksum = sum(int(d) * w for d, w in zip(pfx, weights))
        return str((12 - checksum % 11) % 11)

    check_digit = calc_check_digit(prefix)
    return prefix + check_digit


def generate_random_tax_id():
    """地税证号风格随机编号"""
    prefix = "".join(str(random.randint(0, 9)) for _ in range(6))
    birthday = "".join(str(random.randint(0, 9)) for _ in range(8))
    suffix = "".join(str(random.randint(0, 9)) for _ in range(3))
    check_digit = _calculate_check_digit(prefix + birthday + suffix)
    return prefix + birthday + suffix + check_digit
