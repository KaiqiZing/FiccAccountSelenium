# 操作层：RY_UserManage_Handle.py
# coding=utf-8
from base.find_element import FindElement
from log.user_log import get_logger
from common.CommonWebDriverWaitOperaton import WebDriverWaitCommon
from AccountUtils import AccountInfoSet

class RYUserManageHandle:
    def __init__(self, driver):
        self.driver = driver
        self.logger = get_logger()
        self.fd = FindElement(driver)
        self.WebDriver = WebDriverWaitCommon(self.driver)

    def RY_UserManage(self):
        # 修改点 1：把整个 try...except 删掉，不要在操作层处理异常，让它自然抛出

        # 点击系统管理、用户管理、添加用户菜单 (替换为新的 click_params)
        self.WebDriver.click_params(self.fd.get_UserManageModule_element_txt("SystenManage"))
        self.WebDriver.click_params(self.fd.get_UserManageModule_element_txt("UserManage"))
        self.WebDriver.click_params(self.fd.get_UserManageModule_element_txt("UserManageUser"))

        # 添加用户名称 (去掉 "focus" 参数)
        UserName = "王自然da"
        self.WebDriver.send_keys_params(self.fd.get_UserManageModule_element_txt("UserName"), UserName)

        # 添加用户曾用名
        UserName2 = "dadadaddddda"
        self.WebDriver.send_keys_params(self.fd.get_UserManageModule_element_txt("UserNickName"), UserName2)

        # 添加手机号和密码
        self.WebDriver.send_keys_params(self.fd.get_UserManageModule_element_txt("MobilePhone"), AccountInfoSet.generate_random_phone_number())
        self.WebDriver.send_keys_params(self.fd.get_UserManageModule_element_txt("UserManagePassword"), AccountInfoSet.RandomEmail())

        # 保存
        self.WebDriver.click_params(self.fd.get_UserManageModule_element_txt("EnsureButton"))