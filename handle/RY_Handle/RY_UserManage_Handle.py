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
        UserNickName = "dadadaddddda"
        self.WebDriver.send_keys_params(self.fd.get_UserManageModule_element_txt("UserNickName"), UserNickName)

        # 添加手机号和密码
        self.WebDriver.send_keys_params(self.fd.get_UserManageModule_element_txt("MobilePhone"), AccountInfoSet.generate_random_phone_number())
        self.WebDriver.send_keys_params(self.fd.get_UserManageModule_element_txt("UserManagePassword"), AccountInfoSet.RandomEmail())

        # 保存
        self.WebDriver.click_params(self.fd.get_UserManageModule_element_txt("EnsureButton"))



        # 在 RY_UserManage_Handle.py 中新增此方法
    def RY_UserManage_From_Dict(self,user_manage_data):
        """
        基于字典数据（YAML解析后）执行用户添加
        """
        # 1. 点击系统管理 -> 用户管理菜单
        self.WebDriver.click_params(self.fd.get_UserManageModule_element_txt("SystenManage"))
        self.WebDriver.click_params(self.fd.get_UserManageModule_element_txt("UserManage"))
        self.WebDriver.click_params(self.fd.get_UserManageModule_element_txt("UserManageUser"))

        # 2. 填写 page1: 基本信息
        # 注意：这里的 Key 必须和 test_data.yaml 中的定义严格一致
        self.WebDriver.send_keys_params(
            self.fd.get_UserManageModule_element_txt("UserName"),
            user_manage_data.get("UserName")
        )
        self.WebDriver.send_keys_params(
            self.fd.get_UserManageModule_element_txt("UserNickName"),
            user_manage_data.get("UserNickName")
        )
        self.WebDriver.send_keys_params(
            self.fd.get_UserManageModule_element_txt("MobilePhone"),
            user_manage_data.get("MobilePhone")
        )

        self.WebDriver.send_keys_params(
            self.fd.get_UserManageModule_element_txt("UserManagePassword"),
            user_manage_data.get("UserManagePassword")
        )

        # 4. 保存
        self.WebDriver.click_params(self.fd.get_UserManageModule_element_txt("EnsureButton"))
