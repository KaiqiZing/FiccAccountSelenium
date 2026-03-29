"""统一 WebDriver 创建入口。"""
from __future__ import annotations

from typing import Any

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

from common.exceptions import ConfigError
from config.settings import Config
from log.user_log import get_logger

try:
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.firefox import GeckoDriverManager
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
except ImportError:  # pragma: no cover - 依赖未安装时走 Selenium 默认行为
    ChromeDriverManager = None
    GeckoDriverManager = None
    EdgeChromiumDriverManager = None


class DriverFactory:
    logger = get_logger()

    @staticmethod
    def _build_common_options(options: Any, headless: bool) -> Any:
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if headless:
            options.add_argument("--headless=new")
        return options

    @staticmethod
    def _create_chrome(headless: bool):
        options = DriverFactory._build_common_options(ChromeOptions(), headless)
        if ChromeDriverManager:
            service = ChromeService(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=options)

        DriverFactory.logger.warning("未安装 webdriver-manager，改为使用本地 ChromeDriver。")
        driver_path = Config().get("browser.chrome_driver_path", None)
        if driver_path and str(driver_path).strip():
            path = str(driver_path).strip()
            service = ChromeService(path)
            return webdriver.Chrome(service=service, options=options)

        return webdriver.Chrome(options=options)

    @staticmethod
    def _create_firefox(headless: bool):
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        if GeckoDriverManager:
            service = FirefoxService(GeckoDriverManager().install())
            return webdriver.Firefox(service=service, options=options)
        DriverFactory.logger.warning("未安装 webdriver-manager，改为使用本地 GeckoDriver。")
        return webdriver.Firefox(options=options)

    @staticmethod
    def _create_edge(headless: bool):
        options = DriverFactory._build_common_options(EdgeOptions(), headless)
        if EdgeChromiumDriverManager:
            service = EdgeService(EdgeChromiumDriverManager().install())
            return webdriver.Edge(service=service, options=options)
        DriverFactory.logger.warning("未安装 webdriver-manager，改为使用本地 EdgeDriver。")
        return webdriver.Edge(options=options)

    @staticmethod
    def create_driver(browser_type: str | None = None, headless: bool | None = None):
        cfg = Config()
        browser_cfg = cfg.get("browser", {})
        browser_name = str(browser_type or browser_cfg.get("type", "chrome")).strip().lower()
        use_headless = bool(browser_cfg.get("headless", False) if headless is None else headless)

        creators = {
            "chrome": DriverFactory._create_chrome,
            "firefox": DriverFactory._create_firefox,
            "edge": DriverFactory._create_edge,
        }
        if browser_name not in creators:
            raise ConfigError("不支持的浏览器类型", config_key="browser.type", config_file=str(cfg.settings_file))

        driver = creators[browser_name](use_headless)

        implicit_wait = browser_cfg.get("implicit_wait", 0)
        page_load_timeout = browser_cfg.get("page_load_timeout", 30)
        window_size = browser_cfg.get("window_size", [1920, 1080])
        maximize_window = bool(browser_cfg.get("maximize_window", True))

        if implicit_wait:
            driver.implicitly_wait(int(implicit_wait))
        if page_load_timeout:
            driver.set_page_load_timeout(int(page_load_timeout))
        if maximize_window:
            driver.maximize_window()
        elif isinstance(window_size, (list, tuple)) and len(window_size) == 2:
            driver.set_window_size(int(window_size[0]), int(window_size[1]))

        DriverFactory.logger.info(
            "浏览器已启动: type=%s, headless=%s", browser_name, use_headless
        )
        return driver
