# coding=utf-8
import time
from log.user_log import UserLog
from base.find_element import FindElement
from common.CommonWebDriverWaitOperaton import WebDriverWaitCommon


class FiccExceptionModuleCommon:

    def __init__(self, driver):
        """
        :param driver:
        """
        self.driver = driver
        self.logger = UserLog().get_log()
        self.fd = FindElement(driver)
        self.WebDriver = WebDriverWaitCommon(self.driver)


    def FiccExceptionModule(self):
        """集合FICC中常见的报错类型和报错后的处理方式"""
        self.error_message_element = self.WebDriver.WebDriverWaitOperaton(
            self.fd.get_accountCPH_element_txt("error_message_element"))
        error_message_txt = self.error_message_element.text
        if error_message_txt == "您所填写的信息已存在于草稿箱，请勿重复录入":
            pass
        elif error_message_txt == "您所填写的信息已存在于草稿箱":
            pass


