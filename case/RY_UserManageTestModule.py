# coding=utf-8
import os
import pytest

from business.RY_Login_Business import RYLoginBusiness
from log.user_log import get_logger
from util.CheckErrorCapture import check_and_capture_error
from util.data_factory import DataFactory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Excel 账号表（与 YAML 用例共用统一数据工厂，静态缓存避免重复读盘）
RY_ACCOUNT_EXCEL_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "config", "RYAccountData.xlsx"))


def _load_login_cases():
    test_data = DataFactory().get_excel(RY_ACCOUNT_EXCEL_PATH) or []

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


def test_login_account_from_excel(driver, should_run, row_num, username, password):
    logger = get_logger()

    if not should_run:
        pytest.fail(f"Excel读取失败：{globals().get('_excel_load_error', 'unknown error')}")

    case_desc = f"第{row_num}行：账号={username}"
    logger.info(f"========== 开始执行：{case_desc} ==========")

    biz = RYLoginBusiness(driver)
    biz.LoginTest(username, password)

    # 只关注业务逻辑：如果有红色错误弹窗，就主动把用例 Fail 掉
    # Fail 之后，conftest.py 会自动接管并截取一张 CRASH 截图
    if check_and_capture_error(driver):
        pytest.fail(f"登录失败，出现了错误弹窗：{case_desc}")

    # 如果代码中途因为元素找不到等问题抛出 Exception 崩溃了
    # 也会被 conftest.py 自动拦截截图，无需这里操心

    logger.info(f"========== 执行成功：{case_desc} ==========")