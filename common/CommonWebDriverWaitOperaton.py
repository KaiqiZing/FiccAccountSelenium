from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from log.user_log import get_logger


class WebDriverWaitCommon:
    def __init__(self, driver):
        self.driver = driver
        self.logger = get_logger()

        self.timeout = 10  # 统一设置默认超时时间，方便管理

    def wait_for_visible(self, xpath_locator):
        """
        等待元素在页面上肉眼可见（适用于输入框、普通文本读取）
        """
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located((By.XPATH, xpath_locator))
        )

    def wait_for_clickable(self, xpath_locator):
        """
        等待元素可被点击（适用于按钮、链接、多选框等）
        """
        return WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath_locator))
        )

    def send_keys_params(self, xpath_locator, params_contents, clear_first=True):
        """
        更健壮的输入方法：等待可见 -> 清空 -> 输入
        :param xpath_locator: XPath 定位字符串
        :param params_contents: 要输入的值
        :param clear_first: 是否先清空输入框
        """
        # 1. 等待元素真实可见
        element = self.wait_for_visible(xpath_locator)

        # 2. 原生清空操作
        if clear_first:
            element.clear()

        # 3. 原生输入操作
        element.send_keys(params_contents)
        return element

    def click_params(self, xpath_locator, force_js=False):
        """
        更健壮的点击方法：等待可点击 -> 点击
        :param xpath_locator: XPath 定位字符串
        :param force_js: 遇到棘手的元素遮挡时，设为 True 强制 JS 点击兜底
        """
        element = self.wait_for_clickable(xpath_locator)

        if force_js:
            self.driver.execute_script("arguments[0].click();", element)
        else:
            try:
                element.click()  # 优先使用模拟真人的原生点击
            except Exception as e:
                # 原生点击如果被遮挡报错，尝试使用 JS 兜底并打印警告
                self.logger.warning(f"原生点击失败，尝试使用 JS 点击兜底: {e}")
                self.driver.execute_script("arguments[0].click();", element)