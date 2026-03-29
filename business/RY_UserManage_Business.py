# 业务层：RY_UserManage_Business.py
# coding=utf-8
import allure

from handle.RY_Handle.RY_Login_Handle import RYLoginHandle
from handle.RY_Handle.RY_UserManage_Handle import RYUserManageHandle
from log.user_log import get_logger


class RYUserManageBusiness:
    def __init__(self, driver):
        self.logger = get_logger()
        self.LoginBusiness = RYLoginHandle(driver)
        self.UserManageBusiness = RYUserManageHandle(driver)

    def Login(self, username, password):
        """纯登录，不做后续业务操作"""
        with allure.step(f"Business: 执行登录 (账号={username})"):
            try:
                self.LoginBusiness.RY_Login_Register_Element(username, password)
            except Exception as e:
                self.logger.error(f"RY 登录失败：{e}")
                raise

    def AddUser(self, user_data: dict):
        """仅执行用户新增（登录后调用）"""
        with allure.step(f"Business: 新增用户 ({user_data.get('UserName', '')})"):
            try:
                self.UserManageBusiness.RY_UserManage_From_Dict(user_data)
            except Exception as e:
                self.logger.error(f"RY 用户新增失败：{e}")
                raise

    def UserManageTest(self, username, password, user_manage_data):
        """登录 + 用户管理"""
        with allure.step(f"Business: 登录并管理用户 (账号={username})"):
            try:
                self.LoginBusiness.RY_Login_Register_Element(username, password)
                self.UserManageBusiness.RY_UserManage_From_Dict(user_manage_data)
            except Exception as e:
                self.logger.error(f"RY 用户管理失败：{e}")
                raise
