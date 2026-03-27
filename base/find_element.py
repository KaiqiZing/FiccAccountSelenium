# coding=utf-8
import time
from util.read_ini import ReadIni
from log.user_log import get_logger


class FindElement:
    """元素查找器，支持配置驱动、定位器缓存和重试机制（Selenium 3版本）"""

    def __init__(self, driver):
        self.driver = driver
        self.logger = get_logger()

        # 【优点保留】预加载常用配置，避免反复进行磁盘 I/O 读取文件
        self.configs = {
            'default': ReadIni(file_name="../config/LocalElement.ini"),
            'login': ReadIni(file_name="../config/LoginElement.ini"),
            'UserManageModule': ReadIni(file_name="../config/LoginElement.ini")

        }

        # 【修正】将“元素缓存”改为“定位器缓存”
        # 只缓存解析后的 (by, value) 元组，绝对不能缓存 WebElement 对象
        self.locator_cache = {}

        # 【优点保留】重试机制配置
        self.retry_attempts = 3
        self.retry_delay = 1  # 秒

    def _parse_locator(self, key: str, config_name: str) -> tuple:
        """安全地解析配置文件中的定位信息，并利用缓存加速"""
        cache_key = f"{config_name}_{key}"

        # 如果已经解析过这个 key，直接从内存返回 (by, value)
        if cache_key in self.locator_cache:
            return self.locator_cache[cache_key]

        # 如果没解析过，去读取 ini 文件
        config = self.configs.get(config_name, self.configs['default'])
        data = config.get_value(key)

        # 【修正】拦截空值，防止 AttributeError
        if not data:
            self.logger.error(f"配置文件 [{config_name}] 中未找到 Key: {key}")
            return None, None

        # 【修正】使用 split('>', 1) 解决 XPath 中含有 '>' 导致的崩溃漏洞
        parts = data.split('>', 1)
        if len(parts) == 2:
            by, value = parts[0].strip(), parts[1].strip()
            if by == '':
                by = 'xpath'  # 兼容 "=>//*[@id=...]" 这种缺省写法
        else:
            by, value = 'xpath', data.strip()

        # 存入定位器缓存
        self.locator_cache[cache_key] = (by, value)
        return by, value

    def _execute_find(self, by: str, value: str) -> object:
        """内部元素查找方法，使用Selenium 3 API"""
        if by == 'id':
            return self.driver.find_element_by_id(value)
        elif by == 'name':
            return self.driver.find_element_by_name(value)
        elif by == 'className':
            return self.driver.find_element_by_class_name(value)
        elif by == 'css':
            return self.driver.find_element_by_css_selector(value)
        else:
            return self.driver.find_element_by_xpath(value)

    def get_element(self, key: str, config_name: str = 'default') -> object:
        """获取元素，带重试机制（实时查找，防止过期）"""
        by, value = self._parse_locator(key, config_name)
        if not by or not value:
            return None

        # 【优点保留】重试机制，提高不稳定性网络/页面渲染的容错率
        for attempt in range(self.retry_attempts):
            try:
                # 每次都必须实时向浏览器发起查询，不能复用旧的 WebElement
                return self._execute_find(by, value)
            except Exception as e:
                if attempt == self.retry_attempts - 1:
                    self.logger.error(f"元素查找彻底失败: {key} in {config_name}. Error: {str(e)}")
                    return None
                time.sleep(self.retry_delay)

    def get_text(self, key: str, config_name: str = 'default') -> str:
        """安全地获取元素配置文本"""
        by, value = self._parse_locator(key, config_name)
        return value if value else ""

    # --- 以下特定的快捷方法保持完全兼容 ---
    def get_Login_element(self, key: str) -> object:
        return self.get_element(key, 'login')

    def get_Login_element_txt(self, key: str) -> str:
        return self.get_text(key, 'login')

    def get_UserManageModule_element(self, key: str) -> object:
        return self.get_element(key, 'UserManageModule')

    def get_UserManageModule_element_txt(self, key: str) -> str:
        return self.get_text(key, 'UserManageModule')

    def clear_cache(self):
        """清除定位器缓存"""
        self.locator_cache.clear()

    def set_retry_config(self, attempts: int = 3, delay: int = 1):
        """设置重试配置"""
        self.retry_attempts = attempts
        self.retry_delay = delay