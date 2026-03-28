# 业务层：RY_Login_Business.py
# coding=utf-8
# 把原来的 from log.user_log import UserLog 换成下面这句：
from log.user_log import get_logger
from handle.RY_Handle.RY_Login_Handle import RYLoginHandle
from handle.RY_Handle.RY_UserManage_Handle import RYUserManageHandle

class RYLoginBusiness:
    def __init__(self, driver):
        self.logger = get_logger()
        self.LoginBusiness = RYLoginHandle(driver)
        self.UserManageBusiness = RYUserManageHandle(driver)

    def Login(self, username, password):
        """纯登录，不做后续业务操作"""
        try:
            self.LoginBusiness.RY_Login_Register_Element(username, password)
        except Exception as e:
            self.logger.error(f"RY 登录失败：{e}")
            raise

