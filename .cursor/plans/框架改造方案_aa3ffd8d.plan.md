---
name: 框架改造方案
overview: 基于 SeleniumTestDemo 参考项目，分三个阶段对 FiccAccountSelenium 进行渐进式改造：先做零风险的基础设施补全，再做中等风险的核心能力升级，最后做可选的架构优化。每个阶段都保持现有用例可运行。
todos:
  - id: phase1-pytest-ini
    content: "Phase 1.1: 新增 pytest.ini 统一 pytest 配置"
    status: completed
  - id: phase1-requirements
    content: "Phase 1.2: 新增 requirements.txt 依赖管理"
    status: pending
  - id: phase1-exceptions
    content: "Phase 1.3: 新增 common/exceptions.py 自定义异常体系"
    status: completed
  - id: phase1-screenshot
    content: "Phase 1.4: 新增 util/screenshot_util.py 截图工具类"
    status: completed
  - id: phase2-webdriver-common
    content: "Phase 2.1: 扩展 WebDriverWaitCommon 支持多定位方式 + 新增方法"
    status: completed
  - id: phase2-driver-factory
    content: "Phase 2.2: 引入 DriverFactory + webdriver-manager 自动驱动管理"
    status: completed
  - id: phase2-logger
    content: "Phase 2.3: 日志增强(控制台输出 + 轮转 + 脱敏)"
    status: completed
  - id: phase3-config-center
    content: "Phase 3.1: [可选] 统一配置中心 config/settings.yaml"
    status: completed
  - id: phase3-run-script
    content: "Phase 3.2: [可选] 新增 run_tests.py 多模式运行脚本"
    status: completed
  - id: phase3-base-page
    content: "Phase 3.3: [可选/长期] 引入 BasePage 基类，新页面试点 POM 模式"
    status: pending
  - id: todo-1774716304177-bea0d35wl
    content: ""
    status: pending
isProject: false
---

# 框架改造实施方案

## 现状概要

当前项目分层: `base/find_element.py` (INI定位解析) -> `common/WebDriverWaitCommon` (显式等待,仅XPath) -> `handle/` (操作层) -> `business/` (业务层) -> `case/` (用例层)

参考项目分层: `page_objects/base_page.py` (页面基类,多定位方式) -> `page_objects/modules/` (页面模块) -> `business/` (业务流程) -> `testcases/` (用例层)

改造核心原则: **渐进式改进，不破坏现有用例**。

---

## Phase 1: 基础设施补全 (零破坏风险)

全部是新增文件，不修改任何现有代码。

### 1.1 新增 `pytest.ini`

在项目根目录新增，统一 pytest 行为。

```ini
[pytest]
testpaths = case
python_files = *TestModule*.py
python_classes = Test*
python_functions = test_*+
addopts = -v --tb=short
markers =
    smoke: 冒烟测试
    regression: 回归测试
log_cli = true
log_cli_level = INFO
```

- **可行性**: 纯新增，零风险。当前用例命名已符合 `test_`* 模式，`testpaths = case` 直接指向现有目录。
- **收益**: 无需每次手动指定路径，IDE 和 CI 都受益。

### 1.2 新增 `requirements.txt`

```
selenium>=4.10.0
pytest>=9.0.0
PyYAML>=6.0
openpyxl>=3.1.0
allure-pytest>=2.13.0
webdriver-manager>=4.0.0
pytest-rerunfailures>=12.0
```

- **可行性**: 纯新增，零风险。
- **收益**: 环境可复现，新成员 `pip install -r requirements.txt` 一键搭建。

### 1.3 新增自定义异常模块 `common/exceptions.py`

新增文件，定义三种核心异常:

- `ElementNotFoundError(message, locator, screenshot_path)` -- 元素找不到时抛出，携带定位器信息和截图路径
- `BusinessError(message, business_context)` -- 业务逻辑失败，携带上下文字典
- `ConfigError(message, config_key, config_file)` -- 配置错误
- **可行性**: 纯新增文件，不影响现有代码。后续改造中逐步替换裸 `Exception`。
- **收益**: 错误信息从 "Exception: xxx" 变成 "ElementNotFoundError: xxx / 定位器: (xpath, ...) / 截图: ..."，排查问题效率翻倍。

### 1.4 新增截图工具类 `util/screenshot_util.py`

从 [case/conftest.py](case/conftest.py) 和 [util/CheckErrorCapture.py](util/CheckErrorCapture.py) 中提取公共截图逻辑:

- `ScreenshotUtil.capture(driver, case_id) -> str` -- 页面截图
- `ScreenshotUtil.capture_element(driver, element, case_id) -> str` -- 元素截图
- 自动消毒文件名（去除非法字符）
- 统一截图存放到 `logs/screenshots/`
- **可行性**: 纯新增，现有 conftest.py 和 CheckErrorCapture 不动。新用例可选择使用新工具类。
- **收益**: 截图逻辑统一，不再每处手写 `os.makedirs` + `save_screenshot`。

---

## Phase 2: 核心能力升级 (中等风险，需逐步替换)

### 2.1 扩展 `WebDriverWaitCommon` 支持多种定位方式

改动文件: [common/CommonWebDriverWaitOperaton.py](common/CommonWebDriverWaitOperaton.py)

当前只支持 XPath 字符串:

```python
def wait_for_visible(self, xpath_locator):
    return WebDriverWait(...).until(
        EC.visibility_of_element_located((By.XPATH, xpath_locator))
    )
```

改造后支持 tuple 定位器 + 向后兼容 XPath 字符串:

```python
def _resolve_locator(self, locator):
    """兼容两种格式: 纯字符串(XPath) 或 元组(By.ID, 'xxx')"""
    if isinstance(locator, tuple):
        return locator
    return (By.XPATH, locator)

def wait_for_visible(self, locator):
    return WebDriverWait(...).until(
        EC.visibility_of_element_located(self._resolve_locator(locator))
    )
```

新增方法:

- `get_text(locator)` -- 获取元素文本
- `get_attribute(locator, attr)` -- 获取属性值
- `is_element_visible(locator, timeout)` -- 判断可见性(返回 bool，不抛异常)
- `wait_for_disappear(locator)` -- 等待元素消失
- `scroll_to_element(locator)` -- 滚动到元素
- **可行性**: `_resolve_locator` 向后兼容，所有现有 Handle 代码传入 XPath 字符串仍正常工作。新代码可以传 `(By.CSS_SELECTOR, '#submit')` 元组。**零破坏**。
- **风险点**: 需要回归测试所有现有用例确认兼容性。
- **收益**: 解锁 CSS_SELECTOR / ID / NAME 等定位方式，为后续 POM 打基础。

### 2.2 引入 DriverFactory

新增文件: `util/driver_factory.py`

```python
class DriverFactory:
    @staticmethod
    def create_driver(browser_type="chrome", headless=False, ...):
        # webdriver-manager 自动管理驱动版本
        # 支持 Chrome / Firefox / Edge
        # 从 base_config.yaml 读取配置
```

改动文件: [case/conftest.py](case/conftest.py) 第 48 行

```python
# Before:
d = webdriver.Chrome()

# After:
from util.driver_factory import DriverFactory
d = DriverFactory.create_driver()
```

- **可行性**: 只改 conftest.py 一行创建代码，其余不动。`DriverFactory.create_driver()` 默认返回 Chrome，行为一致。
- **依赖**: 需要 `pip install webdriver-manager`。
- **收益**: 告别手动下载 chromedriver，版本自动匹配；一行配置切换 Firefox/Edge。

### 2.3 日志增强

改动文件: [log/user_log.py](log/user_log.py)

三项改进:

1. **开启控制台输出** -- 取消第 35-37 行注释
2. **日志轮转** -- 替换 `FileHandler` 为 `TimedRotatingFileHandler`，保留 30 天
3. **敏感信息脱敏** -- 新增 `SensitiveFilter`，自动把 password/token 值替换为 `*`**

- **可行性**: 改动集中在一个文件，不影响任何调用方（`get_logger()` 签名不变）。
- **收益**: 调试时控制台直接看日志；日志文件不会无限增长；密码不会明文出现在日志中。

---

## Phase 3: 架构优化 (较大改动，可选执行)

### 3.1 统一配置中心

新增: `config/settings.yaml`，合并所有配置:

```yaml
env:
  test:
    base_url: "http://localhost:1024/login?redirect=%2Findex"
    timeout: 10
  prod:
    base_url: "https://prod.example.com"
browser:
  type: chrome
  headless: false
  window_size: [1920, 1080]
screenshot:
  on_failure: true
  path: logs/screenshots
```

新增: `config/settings.py`，单例 Config 类，支持 `Config().get("env.test.base_url")`。

改动: [case/conftest.py](case/conftest.py) 的 `get_base_url()` 改为从 Config 读取。

- **可行性**: 中等。需要迁移 `base_config.yaml` 中的 `global_config` 到新结构，conftest 需要适配。
- **风险**: 现有 `DataFactory().get_yaml("base_config.yaml")` 路径需要兼容。
- **建议**: 保留 `base_config.yaml` 不删，Config 类先作为新入口，旧入口逐步迁移。

### 3.2 多模式运行脚本 `run_tests.py`

新增项目根目录文件:

```python
# python run_tests.py --mode smoke
# python run_tests.py --mode all
# python run_tests.py --mode allure
```

- **可行性**: 纯新增，零风险。
- **收益**: CI/CD 集成和本地执行都更方便。

### 3.3 BasePage 基类引入 (长期方向)

新增: `common/base_page.py`，继承自 `WebDriverWaitCommon`，增加页面级封装。

这一步改动量较大，需要在新页面中试点：

1. 先为一个新页面写 Locators 类 + Page 类
2. 验证与现有 Handle 模式共存无冲突
3. 新业务模块逐步切到 POM 模式，旧模块不强制迁移

- **可行性**: 可以与现有 Handle 模式共存。新增页面用 BasePage，旧页面保持 Handle 不改。
- **风险**: 团队需要学习新模式。
- **建议**: 作为长期方向，不急于全面铺开。

---

## 各改造项可行性总结

- Phase 1 (1.1-1.4): 全部是新增文件，零破坏风险，可立即执行
- Phase 2.1 (WebDriverWaitCommon): 向后兼容设计，风险低，回归测试即可
- Phase 2.2 (DriverFactory): 仅改 conftest 一行，风险低，需装 webdriver-manager
- Phase 2.3 (日志增强): 改一个文件，签名不变，风险极低
- Phase 3.1 (配置中心): 中等风险，建议新旧并存过渡
- Phase 3.2 (run_tests.py): 纯新增，零风险
- Phase 3.3 (BasePage): 大改动，建议新页面试点，旧页面不动
