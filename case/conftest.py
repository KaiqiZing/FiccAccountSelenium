# conftest.py
import pytest
import os
import time



@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest 钩子：获取每个测试用例的执行结果。
    如果用例失败了，自动获取 driver 并截图。
    """
    outcome = yield
    rep = outcome.get_result()

    # 我们只关注 setup 和 call 阶段的失败
    if rep.when in ("setup", "call") and rep.failed:
        # 尝试从该测试用例中获取 fixture 叫 'driver' 的对象
        if "driver" in item.fixturenames:
            driver = item.funcargs.get("driver")
            if driver:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                screenshot_dir = os.path.join(base_dir, "screenshots")
                os.makedirs(screenshot_dir, exist_ok=True)

                timestamp = time.strftime("%Y%m%d_%H%M%S")
                # 截图命名加上用例名称，更清晰
                node_name = item.name.replace("/", "_").replace(":", "_")
                screenshot_path = os.path.join(screenshot_dir, f"CRASH_{node_name}_{timestamp}.png")

                driver.save_screenshot(screenshot_path)
                print(f"\n📸 [全局拦截] 用例失败，已保存崩溃现场截图: {screenshot_path}")
