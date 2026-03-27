#coding=utf-8
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from base.find_element import FindElement
class RegisterPage(object):
    def __init__(self,driver):
        self.driver = driver
        self.fd = FindElement(driver)

    #获取用户名元素
    def get_username_element(self):
        return self.fd.get_element("user_name")

    #获取密码元素
    def get_password_element(self):
        return self.fd.get_element("password")

    #获取注册按钮元素
    def get_button_element(self):
        return self.fd.get_element("register_button")

    #获取FICC页面
    def FICC_element(self):
        return self.fd.get_element("FICCdk")

    def AccountInput_element(self):
        return self.fd.get_element("accountinput")

    #获取到产品户或者机构户
    def USER_TYPE_element(self):
        return self.fd.get_element("USER_TYPE_CPH")

    # #获取到产品户或者机构户
    # def USER_TYPE_element(self):
    #     return self.fd.get_element("USER_TYPE_JGH")

    def InfoChoose1(self):
        return self.fd.get_element("infochoose1")

    def InfoChoose2(self):
        return self.fd.get_element("infochoose2")

    def next_page(self):
        return self.fd.get_element("next")


    def jgjcsetting(self):
        return self.fd.get_element("jgjcsetting")
