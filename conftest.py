# conftest.py
import os
import re
import datetime

import pytest

try:
    from pytest_html import extras as pytest_html_extras
except Exception:  # pragma: no cover
    pytest_html_extras = None


def _safe_filename(s: str) -> str:
    # nodeid 里可能带 / : [ ] 等，做个保守清洗
    s = s.replace("\n", " ").strip()
    s = re.sub(r"[/\\:]+", "_", s)
    s = re.sub(r"\s+", "_", s)
    return s[:180] if len(s) > 180 else s


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # 只处理执行阶段失败
    if rep.when != "call" or not rep.failed:
        return

    # 取 driver（你的用例里是 function 级别 fixture）
    driver = None
    try:
        driver = item.funcargs.get("driver")
    except Exception:
        driver = None

    if driver is None or not hasattr(driver, "save_screenshot"):
        return

    # 截图保存
    os.makedirs("screenshots", exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_nodeid = _safe_filename(item.nodeid)
    screenshot_path = os.path.abspath(os.path.join("screenshots", f"{safe_nodeid}_{ts}.png"))

    try:
        driver.save_screenshot(screenshot_path)
    except Exception:
        return

    # 叠加到 pytest-html 报告（如果安装了 pytest-html）
    if pytest_html_extras is not None:
        try:
            rep.extra = getattr(rep, "extra", [])
            rep.extra.append(pytest_html_extras.image(screenshot_path))
        except Exception:
            pass

    return