#coding=utf-8
import time

from log.user_log import UserLog
from handle.RY_Handle.RY_Login_Handle import RYLoginHandle
from handle.RY_Handle.RY_UserManage_Handle import RYUserManageHandle


class RYLoginBusiness:

    def __init__(self,driver):
        """
        :param driver:
        """
        self.logger = UserLog().get_log()

        self.LoginBusiness = RYLoginHandle(driver)
        self.UserManageBusiness = RYUserManageHandle(driver)


    def LoginTest(self,username, password):
        """
        :param username:
        :param password:
        :param num:
        :return:
        """
        try:
            self.LoginBusiness.RY_Login_Register_Element(username, password)
            self.UserManageBusiness.RY_UserManage()
        except Exception as e:
            # 不要吞异常：让上层 case/测试框架能够触发截图与 fail
            self.logger.error(f"RY 登录失败：{e}")
            raise

        return None


