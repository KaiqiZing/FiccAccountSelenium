# 操作层：RY_Login_Handle.py
# coding=utf-8
from base.find_element import FindElement
from log.user_log import get_logger
from common.CommonWebDriverWaitOperaton import WebDriverWaitCommon


class RYLoginHandle:
    def __init__(self, driver):
        self.driver = driver
        self.logger = get_logger()  # 修改点：更新日志
        self.fd = FindElement(driver)
        self.WebDriver = WebDriverWaitCommon(self.driver)

    def RY_Login_Register_Element(self, username, password):
        # 修改点：去掉中间那个没用的 "click" 参数
        self.WebDriver.send_keys_params(self.fd.get_Login_element_txt("LoginName"), username)
        self.WebDriver.send_keys_params(self.fd.get_Login_element_txt("LoginPassword"), password)

        # 修改点：直接使用封装好的原生点击，不再手动写 js
        self.WebDriver.click_params(self.fd.get_Login_element_txt("LoginSubmit"))