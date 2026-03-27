# 业务层：RY_Login_Business.py
# coding=utf-8
# 把原来的 from log.user_log import UserLog 换成下面这句：
from log.user_log import get_logger
from handle.RY_Handle.RY_Login_Handle import RYLoginHandle
from handle.RY_Handle.RY_UserManage_Handle import RYUserManageHandle

class RYLoginBusiness:
    def __init__(self, driver):
        # 修改点：直接调用 get_logger()
        self.logger = get_logger()
        self.LoginBusiness = RYLoginHandle(driver)
        self.UserManageBusiness = RYUserManageHandle(driver)

    def LoginTest(self, username, password):
        try:
            self.LoginBusiness.RY_Login_Register_Element(username, password)
            self.UserManageBusiness.RY_UserManage()
        except Exception as e:
            self.logger.error(f"RY 登录失败：{e}")
            raise # 这里 raise 保持得非常好！