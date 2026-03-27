# coding=utf-8
import time
from log.user_log import UserLog
from base.find_element import FindElement
from selenium.webdriver.common.action_chains import ActionChains
from common.CommonWebDriverWaitOperaton import WebDriverWaitCommon
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class WindowsDraftBoxCommon:
    def __init__(self, driver):
        """
        :param driver:
        """
        self.driver = driver
        self.logger = UserLog().get_log()
        self.fd = FindElement(driver)
        self.WebDriver = WebDriverWaitCommon(self.driver)


    def WindowsDraftsBox(self):
        # # 使用 XPath 定位到弹窗元素，需要先判断是否存在，要是存在在进行下一步点击操作
        try:
            # 思考针对容易被挡板的界面，设计成捕获到对应的异常信息，说明其不存在，但是还需继续执行后续代码
            self.error_message_element = self.WebDriver.WebDriverWaitOperaton(self.fd.get_accountCPH_element_txt("error_message_element"))
            error_message_txt = self.error_message_element.text
            # 获取报错内容
            if error_message_txt == "您所填写的信息已存在于草稿箱，请勿重复录入":
                self.error_message_button = self.WebDriver.WebDriverWaitOperaton(
                    self.fd.get_accountCPH_element_txt("error_message_button"))
                self.driver.execute_script("$(arguments[0]).click()", self.error_message_button)
                # 定位到要悬停的元素
                self.driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(2)
                self.hover_element = self.fd.get_accountCPH_element('hover_element')
                self.actions = ActionChains(self.driver)
                self.actions.move_to_element(self.hover_element).perform()
                # 悬停操作后的操作，例如点击悬停后出现的菜单项
                time.sleep(2)
                self.hover_element = self.fd.get_accountCPH_element('hover_elements').click()
                # 窗口选择
                try:
                    # 思考针对容易被挡板的界面，设计成捕获到对应的异常信息，说明其不存在，但是还需继续执行后续代码
                    self.infocontinue = self.WebDriver.WebDriverWaitOperaton(self.fd.get_accountCPH_element_txt("infocontinue"))
                    self.driver.execute_script("arguments[0].click();", self.infocontinue)
                except TimeoutException as info_error_content:
                    self.logger.info("实际窗口选择报错:" + str(info_error_content))
                try:
                    #滚动到底端
                    time.sleep(2)
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    # 找到并点击最后一个按钮
                    # 找到所有输入按钮
                    input_buttons = self.driver.find_elements_by_xpath(
                        '//*[@id="app"]/div[1]/div[2]/div/div/main/div/div[1]/div[5]/div[2]/table/tbody/tr/td[7]/div/div/button[1]')

                    # 确保至少有一个按钮存在
                    if input_buttons:
                        # 获取最后一个按钮并点击
                        last_button = input_buttons[-1]
                        self.driver.execute_script("arguments[0].click();", last_button)
                    # 页面开始跳转，点击下一步
                    # 点击业务信息下一步
                    time.sleep(2)
                    self.ywxx_next = self.WebDriver.WebDriverWaitOperaton(self.fd.get_accountCPH_element_txt("ywxx_next"))
                    self.driver.execute_script("$(arguments[0]).click()", self.ywxx_next)
                    # 滚动到最底层
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                except NoSuchElementException:
                    print("元素定位出错")
                except Exception as e:
                    print(f"发生未知异常: {e}")
        except TimeoutException as info_error_content:
            self.logger.info("实际窗口选择报错:" + str(info_error_content))