# coding=utf-8
import datetime
import os

import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from AccountUtils.AccountExcelUtil import ExcelUtil
from business.RY_Login_Business import RYLoginBusiness
from log.user_log import UserLog
from util.CheckErrorCapture import check_and_capture_error

LOGIN_URL = "http://localhost:1025/login?redirect=%2Findex"


def _excel_path() -> str:
    # 基于脚本目录拼接，避免“从不同工作目录运行”导致相对路径失效
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(base_dir, "..", "config", "RYAccountData.xlsx"))


def _load_login_cases():
    """
    从 Excel 读取账号密码并返回参数列表。
    约定：第 1 行表头，第 2 行开始是数据。

    返回：should_run,row_num,username,password 的列表。
    """
    excel_util = ExcelUtil(excel_path=_excel_path())
    test_data = excel_util.get_data() or []

    if len(test_data) <= 1:
        raise ValueError("Excel中未找到有效数据行：RYAccountData.xlsx")

    cases = []
    for row_idx, row_data in enumerate(test_data[1:], start=2):
        if not row_data or len(row_data) < 2:
            continue
        username, password = row_data[0], row_data[1]
        if username is None or password is None:
            continue

        username = str(username).strip()
        password = str(password).strip()
        if not username or not password:
            continue

        cases.append((True, row_idx, username, password))

    if not cases:
        raise ValueError("Excel中没有解析到可执行的账号/密码数据行")

    return cases


def pytest_generate_tests(metafunc):
    """
    把 Excel 行数据变成 pytest 参数。

    Excel 读取失败时不会导致整个 pytest 崩溃，而是生成一个应当失败的参数用例。
    """
    if not {"should_run", "row_num", "username", "password"}.issubset(set(metafunc.fixturenames)):
        return

    try:
        cases = _load_login_cases()
        ids = [f"row_{row_num}" for (_, row_num, _, _) in cases]
        metafunc.parametrize("should_run,row_num,username,password", cases, ids=ids)
    except Exception as e:
        globals()["_excel_load_error"] = str(e)
        metafunc.parametrize(
            "should_run,row_num,username,password",
            [(False, -1, "", "")],
            ids=["excel_load_failed"],
        )


@pytest.fixture(scope="function")
def driver(should_run):
    """
    每条参数化用例都新开浏览器，满足“每行重开浏览器”的执行约束。
    should_run=False 时不启动浏览器（Excel 失败也不阻塞后续业务）。
    """
    if not should_run:
        yield None
        return

    d = webdriver.Chrome()
    d.get(LOGIN_URL)
    d.maximize_window()
    yield d

    try:
        WebDriverWait(d, 5).until(
            lambda x: x.execute_script("return document.readyState") == "complete"
        )
    except Exception:
        pass
    finally:
        d.quit()


def test_login_account_from_excel(driver, should_run, row_num, username, password):
    log = UserLog()
    logger = log.get_log()

    if not should_run:
        try:
            log.close_handle()
        except Exception:
            pass
        pytest.fail(f"Excel读取失败：{globals().get('_excel_load_error', 'unknown error')}")

    case_desc = f"第{row_num}行：账号={username}"
    logger.info(f"========== 开始执行：{case_desc} ==========")

    try:
        biz = RYLoginBusiness(driver)
        # 执行登录账号开通验证
        biz.LoginTest(username, password)

        # 执行过程中检查是否出现错误提示（有错误则截图并 fail）
        if check_and_capture_error(driver):
            pytest.fail(f"登录失败：{case_desc}")
            

        logger.info(f"========== 执行成功：{case_desc} ==========")
    except Exception as e:
        # 有异常时也调用一次错误捕获（尽量复用统一截图逻辑）
        try:
            check_and_capture_error(driver)
        except Exception:
            pass

        # 再额外保存一张“异常现场”截图，方便排查（不依赖错误元素存在）
        try:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            driver.save_screenshot(f"{screenshot_dir}/exception_{timestamp}.png")
        except Exception:
            pass

        logger.error(f"{case_desc} 执行异常：{e}")
        pytest.fail(f"{case_desc} 执行异常：{e}")
    finally:
        try:
            log.close_handle()
        except Exception:
            pass
