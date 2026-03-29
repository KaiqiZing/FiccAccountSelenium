# 业务层：RY_Login_Business.py
# coding=utf-8
import allure

from handle.RY_Handle.RY_Login_Handle import RYLoginHandle
from log.user_log import get_logger


class RYLoginBusiness:
    def __init__(self, driver):
        self.logger = get_logger()
        self.LoginBusiness = RYLoginHandle(driver)

    def LoginTest(self, username, password):
        """纯登录，不做后续业务操作"""
        with allure.step(f"Business: 执行登录 (账号={username})"):
            try:
                self.LoginBusiness.RY_Login_Register_Element(username, password)
            except Exception as e:
                self.logger.error(f"RY 登录失败：{e}")
                raise
