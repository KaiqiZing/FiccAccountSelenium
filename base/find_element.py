# coding=utf-8
from util.read_ini import ReadIni
from log.user_log import get_logger


class FindElement:
    """
    元素定位解析器 (纯净严格版)
    职责：仅负责读取 ini 配置文件并解析 XPath 定位字符串，不包含任何 WebDriver 操作。
    """

    def __init__(self, driver=None):
        # 这里的 driver 参数仅仅为了向下兼容现有的 Handle 实例化代码 (self.fd = FindElement(driver))
        # 实际上本类已经彻底与 driver (Selenium) 解耦
        self.driver = driver
        self.logger = get_logger()

        # 严格模式：将 配置实例 和 节点名称(Section) 组合成元组存储
        # 确保这里传入的 node 名称与你在 INI 文件中实际写的 [Section] 保持完全一致
        self.configs_map = {
            'login': (ReadIni("../config/LoginElement.ini"), "LoginElement"),
            'UserManageModule': (ReadIni("../config/LoginElement.ini"), "UserManageElement")
        }

        # 定位器缓存，只缓存解析后的 (by, value) 字符串字典
        self.locator_cache = {}

    def _parse_locator(self, key: str, config_name: str) -> tuple:
        """安全地解析配置文件中的定位信息，并利用缓存加速"""
        cache_key = f"{config_name}_{key}"

        # 1. 查缓存：如果已经解析过，直接返回
        if cache_key in self.locator_cache:
            return self.locator_cache[cache_key]

        # 2. 查映射：防止上层代码传错模块名
        if config_name not in self.configs_map:
            error_msg = f"❌ 未知的配置模块名称: {config_name}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        ini_instance, node_name = self.configs_map[config_name]

        try:
            # 3. 严格读取：明确传入 key 和 node，底层如果找不到会抛出 ValueError
            data = ini_instance.get_value(key=key, node=node_name)
        except ValueError as e:
            # 记录详细日志后继续向上抛出，触发 conftest.py 的全局错误截图
            self.logger.error(str(e))
            raise

            # 4. 解析 "by>value" 格式
        parts = data.split('>', 1)
        if len(parts) == 2:
            by, value = parts[0].strip(), parts[1].strip()
            # 兼容 "=>//*[@id=...]" 这种缺省写法
            if by == '':
                by = 'xpath'
        else:
            by, value = 'xpath', data.strip()

        # 5. 存入定位器缓存
        self.locator_cache[cache_key] = (by, value)
        return by, value

    def get_text(self, key: str, config_name: str = 'default') -> str:
        """
        获取解析后的定位器字符串（通常为 XPath）
        供外部的 WebDriverWaitCommon 显式等待调用
        """
        by, value = self._parse_locator(key, config_name)
        return value if value else ""

    # =========================================================
    # --- 以下特定的快捷方法保持完全兼容，上层 Handle 代码一行都不用改 ---
    # =========================================================

    def get_Login_element_txt(self, key: str) -> str:
        return self.get_text(key, 'login')

    def get_UserManageModule_element_txt(self, key: str) -> str:
        return self.get_text(key, 'UserManageModule')

    def clear_cache(self):
        """清除定位器缓存（预留给长时间运行的测试套件使用）"""
        self.locator_cache.clear()