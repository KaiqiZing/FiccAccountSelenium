# coding=utf-8
"""身份证生成与校验。"""
import random
import re
from datetime import datetime, timedelta

from AccountUtils.data.area_info import AREA_INFO

# 十五位身份证号表达式
ID_NUMBER_15_REGEX = r"^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}$"

# 十八位身份证号表达式
ID_NUMBER_18_REGEX = (
    r"^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))"
    r"(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$"
)


class IdCardNumber:
    def __init__(self, id_number):
        self.id = id_number
        self.area_id = int(self.id[0:6])
        self.birth_year = int(self.id[6:10])
        self.birth_month = int(self.id[10:12])
        self.birth_day = int(self.id[12:14])

    def get_area_name(self):
        """根据区域编号取出区域名称"""
        return AREA_INFO[self.area_id]

    def get_birthday(self):
        """通过身份证号获取出生日期"""
        return "{0}-{1}-{2}".format(self.birth_year, self.birth_month, self.birth_day)

    def get_age(self):
        """通过身份证号获取年龄"""
        now = datetime.now() + timedelta(days=1)
        year, month, day = now.year, now.month, now.day

        if year == self.birth_year:
            return 0
        if self.birth_month > month or (
            self.birth_month == month and self.birth_day > day
        ):
            return year - self.birth_year - 1
        return year - self.birth_year

    def get_sex(self):
        """通过身份证号获取性别，女生：0，男生：1"""
        return int(self.id[16:17]) % 2

    def get_check_digit(self):
        """通过身份证号获取校验码"""
        check_sum = 0
        for i in range(0, 17):
            check_sum += ((1 << (17 - i)) % 11) * int(self.id[i])
        check_digit = (12 - (check_sum % 11)) % 11
        return check_digit if check_digit < 10 else "X"

    @classmethod
    def verify_id(cls, id_number):
        """校验身份证是否正确"""
        if re.match(ID_NUMBER_18_REGEX, id_number):
            check_digit = cls(id_number).get_check_digit()
            return str(check_digit) == id_number[-1]
        return bool(re.match(ID_NUMBER_15_REGEX, id_number))

    @classmethod
    def generate_id(cls, random_sex=None):
        """
        随机生成身份证号，sex = 0 表示女性，sex = 1 表示男性
        """
        if random_sex is None:
            random_sex = random.randint(0, 1)
        id_number = str(random.choice(list(AREA_INFO.keys())))
        start = datetime.strptime("1960-01-01", "%Y-%m-%d")
        end = datetime.strptime("2000-12-30", "%Y-%m-%d")
        birth_days = datetime.strftime(
            start + timedelta(random.randint(0, (end - start).days + 1)), "%Y%m%d"
        )
        id_number += str(birth_days)
        id_number += str(random.randint(10, 99))
        id_number += str(random.randrange(random_sex, 10, step=2))
        return id_number + str(cls(id_number).get_check_digit())


def RandomIDCards(random_sex=None):
    """生成身份证号码"""
    return IdCardNumber.generate_id(random_sex)
