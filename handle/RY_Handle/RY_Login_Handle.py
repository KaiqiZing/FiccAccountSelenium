# coding=utf-8
import time
from base.find_element import FindElement
from log.user_log import UserLog
from common.CommonWebDriverWaitOperaton import WebDriverWaitCommon


class RYLoginHandle:

    def __init__(self, driver):
        self.driver = driver
        self.logger = UserLog().get_log()
        self.fd = FindElement(driver)
        self.WebDriver = WebDriverWaitCommon(self.driver)

    def RY_Login_Register_Element(self,username, password):
        """

        :param username: 用户名
        :param password: 用户密码
        :return:
        """
        self.WebDriver.send_keys_params(self.fd.get_Login_element_txt("email_element"), "click",
                                        username)

        self.WebDriver.send_keys_params(self.fd.get_Login_element_txt("password_elements"), "click",
                                        password)

        self.submit = self.WebDriver.WebDriverWaitOperaton(self.fd.get_Login_element_txt("submit"))

        self.driver.execute_script("arguments[0].click();", self.submit)



