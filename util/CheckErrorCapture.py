import time
import os
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 1. 引入重构后的 get_logger
from log.user_log import get_logger

logger = get_logger()


def check_and_capture_error(driver, screenshot_dir="screenshots"):
    """
    专注检查业务弹窗错误。
    注意：为了不拖慢成功用例的速度，将等待时间缩短为 1~2 秒即可。
    因为如果是真的业务报错，弹窗通常是瞬间出现的。
    """
    try:
        error_xpath = "//div[@role='alert' and contains(@class, 'el-message--error') and .//p[@class='el-message__content']]"

        # 2. 将 5 秒改为 1.5 秒，避免成功用例在这里干等
        error_element = WebDriverWait(driver, 1.5).until(
            EC.visibility_of_element_located((By.XPATH, error_xpath))
        )

        error_text = error_element.text
        logger.error(f"⚠️ 捕获到业务弹窗错误: {error_text}")

        # 将路径拼接改为基于当前项目的绝对路径，防止路径错乱
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_screenshot_dir = os.path.join(base_dir, screenshot_dir)
        os.makedirs(full_screenshot_dir, exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(full_screenshot_dir, f"business_error_{timestamp}.png")

        driver.save_screenshot(screenshot_path)
        return True

    except (TimeoutException, NoSuchElementException):
        return False