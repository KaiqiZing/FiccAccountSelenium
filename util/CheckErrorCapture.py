from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from log.user_log import get_logger
from util.screenshot_util import ScreenshotUtil

logger = get_logger()


def check_and_capture_error(driver):
    """
    专注检查业务弹窗错误。
    等待时间缩短为 1.5 秒，避免拖慢成功用例——真正的业务报错弹窗通常是瞬间出现的。
    """
    try:
        error_xpath = (
            "//div[@role='alert' and contains(@class, 'el-message--error')"
            " and .//p[@class='el-message__content']]"
        )

        error_element = WebDriverWait(driver, 1.5).until(
            EC.visibility_of_element_located((By.XPATH, error_xpath))
        )

        error_text = error_element.text
        logger.error(f"捕获到业务弹窗错误: {error_text}")

        ScreenshotUtil.capture(driver, "business_error")
        return True

    except (TimeoutException, NoSuchElementException):
        return False
