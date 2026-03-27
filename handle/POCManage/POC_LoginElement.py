# coding=utf-8
import datetime
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

from base.find_element import FindElement
from util.excel_util import ExcelUtil
from util.pandas_excel import Read_Pandas_Excel
from log.user_log import UserLog
from common.CommonWebDriverWaitOperaton import WebDriverWaitCommon
from handle.account_Login_handle import AccountLoginHandle
from AccountUtils import AccountInfoSet
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class POCLoginHandle:
    def __init__(self, driver):
        self.driver = driver
        self.logger = UserLog().get_log()
        self.fd = FindElement(driver)
        self.exceldata = ExcelUtil('../config/acoountdata.xls')
        self.WebDriver = WebDriverWaitCommon(self.driver)
        self.wait = WebDriverWait(driver, 20,0.5)

        # 读取csv文件信息
        self.pandasdata = Read_Pandas_Excel()
        self.accountloginhandle = AccountLoginHandle(self.driver)

    def poc_login_element(self, username, password):
        self.WebDriver.send_keys_params(self.fd.get_poc_element_txt("poc_username"), "click",
                                        username)
        self.WebDriver.send_keys_params(self.fd.get_poc_element_txt("poc_password"), "click",
                                        password)
        self.WebDriver.click_focus_params(self.fd.get_poc_element_txt("poc_login"), "click")

    def poc_user_operatecheck_element(self):
        """
        :return:
        """
        #输入参数
        time.sleep(2)
        print("已启动")
        authority_username="道合操作用户审核"
        self.WebDriver.send_keys_params(self.fd.get_poc_element_txt("poc_input"), "focus", authority_username)
        # 点击搜索框
        self.WebDriver.click_focus_params(self.fd.get_poc_element_txt("poc_input_search"), "click")
        #点击查询全部
        self.WebDriver.click_focus_params(self.fd.get_poc_element_txt("poc_searchAll"), "click")
        #点击输入的内容
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])
        self.WebDriver.click_focus_params(self.fd.get_poc_element_txt("poc_search_contents"), "click")
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[2])
        # 申请提交时间
        #点击日历
        self.WebDriver.click_focus_params(self.fd.get_poc_element_txt("poc_apply_date"), "click")
        #点击今天
        self.WebDriver.click_focus_params(self.fd.get_poc_element_txt("poc_apply_date_today"), "click")
        #点击查询
        time.sleep(2)
        self.WebDriver.click_focus_params(self.fd.get_poc_element_txt("poc_search_button"), "click")

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 检查元素
        self.NoCheckElements = WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, self.fd.get_poc_element_txt("no_checks"))))
        #编辑元素
        self.editor_button_first = WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, self.fd.get_poc_element_txt("editor_button"))))
        while True:
            if(len(self.NoCheckElements))>1:
                for i in range(len(self.NoCheckElements)):
                    if ("ant-table-row-cell-break-word" in self.NoCheckElements[i].get_attribute("class")):
                        self.driver.execute_script("arguments[0].click();", self.editor_button_first[i])
                        time.sleep(3)
                        self.child_editor_element()
                #再次检查元素总数量
                if len(self.NoCheckElements)<1:
                    break


    def child_editor_element(self):
        #点击审核通过
        # self.WebDriver.click_focus_params(self.fd.get_poc_element_txt("poc_editor_input"), "click")

        checkbox = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//label[@class='ant-checkbox-wrapper']/span[@class='ant-checkbox']/input[@type='checkbox' and @class='ant-checkbox-input' and @value='']")))
        self.driver.execute_script("arguments[0].click();", checkbox)


        #点击用户审核通过
        # self.WebDriver.click_focus_params(self.fd.get_poc_element_txt("poc_editor_checkuserpass"), "click")
        # #点击确定
        # self.WebDriver.click_focus_params(self.fd.get_poc_element_txt("poc_editor_checkuserpass_ensure"), "click")
        # #点击关闭
        # self.WebDriver.click_focus_params(self.fd.get_poc_element_txt("poc_editor_close"), "click")
        # time.sleep(2)
        # self.WebDriver.click_focus_params(self.fd.get_poc_element_txt("poc_search_button"), "click")





