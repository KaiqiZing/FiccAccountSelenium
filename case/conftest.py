# coding=utf-8
"""case 级 Pytest 配置：基础地址、浏览器 driver、失败截图。"""
from __future__ import annotations

import os
import time
from typing import Optional

import pytest
from selenium import webdriver

from util.data_factory import DataFactory

_BASE_URL_CACHE: Optional[str] = None


def get_base_url() -> str:
    """
    从 config/test_data_yaml/base_config.yaml 读取 global_config.base_url。
    进程内只解析一次，避免每条用例重复读盘。
    """
    global _BASE_URL_CACHE
    if _BASE_URL_CACHE is None:
        cfg = DataFactory().get_yaml("base_config.yaml", is_parse=False)
        url = (cfg.get("global_config") or {}).get("base_url")
        if not url:
            raise ValueError(
                "请在 config/test_data_yaml/base_config.yaml 中配置 global_config.base_url"
            )
        _BASE_URL_CACHE = str(url).strip()
    return _BASE_URL_CACHE


@pytest.fixture(scope="function")
def driver(request):
    """
    统一浏览器入口：
    - Excel 参数化用例：依赖 should_run；为 False 时不启动浏览器（仅占位失败用例）。
    - YAML 等用例：无 should_run，直接启动并打开 base_url。
    """
    base_url = get_base_url()
    if "should_run" in request.fixturenames:
        should_run = request.getfixturevalue("should_run")
        if not should_run:
            yield None
            return

    d = webdriver.Chrome()
    d.get(base_url)
    d.maximize_window()
    yield d
    d.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest 钩子：获取每个测试用例的执行结果。
    如果用例失败了，自动获取 driver 并截图。
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when in ("setup", "call") and rep.failed:
        if "driver" in item.fixturenames:
            drv = item.funcargs.get("driver")
            if drv:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                screenshot_dir = os.path.join(base_dir, "screenshots")
                os.makedirs(screenshot_dir, exist_ok=True)

                timestamp = time.strftime("%Y%m%d_%H%M%S")
                node_name = item.name.replace("/", "_").replace(":", "_")
                screenshot_path = os.path.join(
                    screenshot_dir, f"CRASH_{node_name}_{timestamp}.png"
                )

                drv.save_screenshot(screenshot_path)
                print(f"\n📸 [全局拦截] 用例失败，已保存崩溃现场截图: {screenshot_path}")
