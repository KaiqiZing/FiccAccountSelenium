# coding=utf-8
"""case 级 Pytest 配置：基础地址、浏览器 driver、失败截图。"""
from __future__ import annotations

from typing import Optional

import pytest

from common.exceptions import ConfigError
from config.settings import Config
from util.data_factory import DataFactory
from util.driver_factory import DriverFactory
from util.screenshot_util import ScreenshotUtil

_BASE_URL_CACHE: Optional[str] = None


def get_base_url() -> str:
    """
    优先从统一配置中心读取 base_url，旧 base_config.yaml 仍作为兜底。
    """
    global _BASE_URL_CACHE
    if _BASE_URL_CACHE is None:
        url = None
        try:
            config = Config()
            env_config = config.get_env_config()
            url = env_config.get("base_url")
        except ConfigError:
            url = None

        if not url:
            cfg = DataFactory().get_yaml("base_config.yaml", is_parse=False)
            url = (cfg.get("global_config") or {}).get("base_url")
        if not url:
            raise ValueError(
                "请在 config/settings.yaml 或 config/test_data_yaml/base_config.yaml 中配置 base_url"
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

    d = DriverFactory.create_driver()
    d.get(base_url)
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
                on_failure = True
                try:
                    on_failure = bool(Config().get("screenshot.on_failure", True))
                except ConfigError:
                    on_failure = True

                if on_failure:
                    screenshot_path = ScreenshotUtil.capture(drv, item.name)
                    print(f"\n[全局拦截] 用例失败，已保存崩溃现场截图: {screenshot_path}")
