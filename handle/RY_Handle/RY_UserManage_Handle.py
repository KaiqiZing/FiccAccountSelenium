# coding=utf-8
import time
from base.find_element import FindElement
from log.user_log import UserLog
from common.CommonWebDriverWaitOperaton import WebDriverWaitCommon
from AccountUtils import AccountInfoSet

class RYUserManageHandle:

    def __init__(self, driver):
        self.driver = driver
        self.logger = UserLog().get_log()
        self.fd = FindElement(driver)
        self.WebDriver = WebDriverWaitCommon(self.driver)

    def RY_UserManage(self):
        """

        :param username: 用户名
        :param password: 用户密码
        :return:
        """
        try:
            # 点击系统管理（需先等待元素可见再点击，不能直接传 XPath 字符串给 execute_script_func）
            self.WebDriver.click_focus_params(self.fd.get_UserManageModule_element_txt("SystenManage"), "click")
            # 点击用户管理
            self.WebDriver.click_focus_params(self.fd.get_UserManageModule_element_txt("UserManage"), "click")
            # 点击添加用户菜单
            self.WebDriver.click_focus_params(self.fd.get_UserManageModule_element_txt("UserManageUser"), "click")

            # 添加用户名称


            UserName = "王自然da"
            self.WebDriver.send_keys_params(self.fd.get_UserManageModule_element_txt("UserName"), "focus", UserName)

            # 添加用户曾用名
            UserName2 = "dadadaddddda"
            self.WebDriver.send_keys_params(self.fd.get_UserManageModule_element_txt("UserName2"), "focus",
                                            UserName2)
            # 添加用户手机号码
            self.WebDriver.send_keys_params(self.fd.get_UserManageModule_element_txt("MobilePhone"), "focus",
                                            AccountInfoSet.generate_random_phone_number())
            # 添加用户密码
            self.WebDriver.send_keys_params(self.fd.get_UserManageModule_element_txt("Password"), "focus",
                                            AccountInfoSet.RandomEmail())
            # 保存
            self.WebDriver.click_focus_params(self.fd.get_UserManageModule_element_txt("EnsureButton"), "click")

        except Exception as RY_UserManageError:

            print(f"Error in RY_UserManage报错内容: {str(RY_UserManageError)}")
            self.logger.info("RY_UserManage报错内容:" + str(RY_UserManageError))
