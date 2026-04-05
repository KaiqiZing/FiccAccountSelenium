# 异常链监控系统设计

## 项目：FiccAccountSelenium

---

# 1. 异常层次结构设计

项目采用**树形异常继承体系**，实现精准的错误分类和上下文保留：

```
Exception (Python 内置)
    ↓
FrameworkError (框架基础异常)
    ├── ElementNotFoundError (元素查找失败)
    ├── BusinessError (业务流程执行失败)
    └── ConfigError (配置读取/解析失败)
```

## 1.1 统一异常基类

**文件**: common/exceptions.py (第7-15行)

```python
class FrameworkError(Exception):
    """框架基础异常，统一保留 message。"""
    
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
    
    def __str__(self) -> str:
        return self.message
```

**设计理念**：
- 统一保存 `message` 属性
- 通过 `__str__` 提供友好的错误描述
- 为所有业务异常提供统一基类

---

# 2. 上下文信息保留机制

## 2.1 元素定位异常

**文件**: common/exceptions.py (第18-37行)

```python
class ElementNotFoundError(FrameworkError):
    def __init__(
        self,
        message: str,
        locator: Optional[Any] = None,           # 定位器信息
        screenshot_path: Optional[str] = None,  # 截图路径
    ) -> None:
        super().__init__(message)
        self.locator = locator
        self.screenshot_path = screenshot_path
    
    def __str__(self) -> str:
        parts = [self.message]
        if self.locator is not None:
            parts.append(f"定位器: {self.locator}")
        if self.screenshot_path:
            parts.append(f"截图: {self.screenshot_path}")
        return " / ".join(parts)
```

**关键设计**：
- ✅ 保留**定位器信息**（方便复现问题）
- ✅ 保存**截图路径**（可视化证据）
- ✅ 格式化输出（多段信息拼接）

## 2.2 业务异常

**文件**: common/exceptions.py (第40-50行)

```python
class BusinessError(FrameworkError):
    def __init__(
        self, 
        message: str, 
        business_context: Optional[dict[str, Any]] = None  # 业务上下文
    ) -> None:
        super().__init__(message)
        self.business_context = business_context or {}
```

**设计理念**：
- 保存**业务上下文字典**（用户名、操作步骤等）
- 用于追踪失败时的完整业务状态

## 2.3 配置异常

**文件**: common/exceptions.py (第53-72行)

```python
class ConfigError(FrameworkError):
    def __init__(
        self,
        message: str,
        config_key: Optional[str] = None,
        config_file: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.config_key = config_key
        self.config_file = config_file
```

---

# 3. 异常链追踪机制

## 3.1 使用 `from exc` 保留原始异常

**位置**：common/CommonWebDriverWaitOperation.py (第60-61行)

```python
def wait_for_visible(self, locator: Any):
    try:
        return self._wait().until(EC.visibility_of_element_located(resolved))
    except TimeoutException as exc:
        # 使用 "from exc" 保留原始异常堆栈
        raise self._build_not_found_error(locator, "等待元素可见") from exc
```

**执行流程**：

```
TimeoutException (Selenium 原生异常)
    ↓ [from exc 链接]
    ↓
ElementNotFoundError (框架自定义异常)
    ↓
捕获时可通过 __cause__ 访问原始异常
```

## 3.2 异常链可视化示例

```
Traceback (most recent call last):
  File "test_case.py", line 45, in test_login
    handle.login("user", "pass")
  File "handle.py", line 23, in login
    self.wait_for_visible(locator)
  File "CommonWebDriverWaitOperation.py", line 59, in wait_for_visible
    raise self._build_not_found_error(locator, "等待元素可见") from exc
ElementNotFoundError: 等待元素可见失败，未找到目标元素 / 定位器: ('xpath', '//input[@id="username"]')
```

---

# 4. 智能错误上下文构建

## 4.1 失败时自动截图

**文件**: common/CommonWebDriverWaitOperation.py (第43-53行)

```python
def _build_not_found_error(self, locator: Any, action: str) -> ElementNotFoundError:
    screenshot_path = ""
    try:
        # 失败时立即截图，保存现场
        screenshot_path = ScreenshotUtil.capture(self.driver, f"{action}_{locator}")
    except Exception as capture_error:
        self.logger.warning("元素异常时截图失败: %s", capture_error)
    
    return ElementNotFoundError(
        message=f"{action}失败，未找到目标元素",
        locator=locator,
        screenshot_path=screenshot_path or None,
    )
```

**设计亮点**：
- ✅ **异常保护**：截图失败不影响主异常抛出
- ✅ **失败即截图**：第一时间保存现场
- ✅ **记录操作类型**：`_build_not_found_error(locator, "等待元素可见")`

---

# 5. 业务错误弹窗监控

## 5.1 快速业务错误检测

**文件**: util/CheckErrorCapture.py

```python
def check_and_capture_error(driver):
    """
    专注检查业务弹窗错误。
    等待时间缩短为 1.5 秒，避免拖慢成功用例——真正的业务报错弹窗通常是瞬间出现的。
    """
    try:
        error_xpath = (
            "//div[@role='alert' and contains(@class, 'el-message--error')"
            " and .//p[@class='el-message__content']]"
        )
        
        error_element = WebDriverWait(driver, 1.5).until(
            EC.visibility_of_element_located((By.XPATH, error_xpath))
        )
        
        error_text = error_element.text
        logger.error(f"捕获到业务弹窗错误: {error_text}")
        
        ScreenshotUtil.capture(driver, "business_error")
        return True
        
    except (TimeoutException, NoSuchElementException):
        return False
```

**设计理念**：
- ✅ **快速检测**：1.5 秒快速轮询，不拖慢正常用例
- ✅ **专门针对 Element UI**：检测 `el-message--error` 组件
- ✅ **自动截图**：捕获业务错误现场
- ✅ **非阻塞**：超时即返回 False，不影响测试流程

---

# 6. Pytest 钩子集成

## 6.1 全局失败拦截

**文件**: case/conftest.py (第63-84行)

```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest 钩子：获取每个测试用例的执行结果。
    如果用例失败了，自动获取 driver 并截图。
    """
    outcome = yield
    rep = outcome.get_result()
    
    # 仅在 setup 或 call 阶段失败时触发
    if rep.when in ("setup", "call") and rep.failed:
        if "driver" in item.fixturenames:
            drv = item.funcargs.get("driver")
            if drv:
                # 读取配置控制是否截图
                on_failure = True
                try:
                    on_failure = bool(Config().get("screenshot.on_failure", True))
                except ConfigError:
                    on_failure = True
                
                if on_failure:
                    screenshot_path = ScreenshotUtil.capture(drv, item.name)
                    print(f"\n[全局拦截] 用例失败，已保存崩溃现场截图: {screenshot_path}")
```

**钩子执行时机**：

```
pytest 执行流程：
  ↓
setup 阶段
  ↓ [pytest_runtest_makereport hook 捕获结果]
  ↓
call 阶段（执行测试）
  ↓ [失败时触发截图]
  ↓
teardown 阶段
```

---

# 7. 统一截图管理系统

## 7.1 智能路径和命名

**文件**: util/screenshot_util.py

```python
class ScreenshotUtil:
    """统一管理页面/元素截图路径与命名。"""
    
    @classmethod
    def _build_path(cls, case_id: str, prefix: str) -> str:
        safe_case_id = cls.sanitize_name(case_id)  # 清理非法字符
        timestamp = time.strftime("%Y%m%d_%H%M%S")  # 时间戳
        target = cls._ensure_dir() / f"{prefix}_{safe_case_id}_{timestamp}.png"
        return str(target)
    
    @classmethod
    def sanitize_name(cls, name: str) -> str:
        # 清理文件名中的非法字符
        cleaned = re.sub(r"[\\/:*?\"<>|\s]+", "_", str(name).strip())
        return cleaned.strip("._") or "screenshot"
```

**命名规范**：

```
page_测试用例名称_20260330_143520.png
element_操作描述_20260330_143521.png
```

---

# 8. 日志脱敏机制

## 8.1 敏感信息过滤

**文件**: log/user_log.py (第10-40行)

```python
class SensitiveFilter(logging.Filter):
    """对常见敏感字段做日志脱敏。"""
    
    PATTERNS = [
        re.compile(r"(?i)(password\s*[=:]\s*)(['\"]?)([^,'\"\s]+)(\2)"),
        re.compile(r"(?i)(token\s*[=:]\s*)(['\"]?)([^,'\"\s]+)(\2)"),
        re.compile(r"(?i)(authorization\s*[=:]\s*)(['\"]?)([^,'\"\s]+)(\2)"),
        re.compile(r'(?i)("password"\s*:\s*")([^"]+)(")'),
        re.compile(r'(?i)("token"\s*:\s*")([^"]+)(")'),
    ]
    
    @classmethod
    def mask(cls, message: str) -> str:
        masked = message
        for pattern in cls.PATTERNS:
            def _replace(match: re.Match[str]) -> str:
                groups = match.groups()
                if len(groups) == 4:
                    return f"{groups[0]}{groups[1]}******{groups[3]}"
                return "******"
            
            masked = pattern.sub(_replace, masked)
        return masked
```

**脱敏示例**：

```
输入: password="abc123"
输出: password="******"

输入: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
输出: Authorization: ******
```

---

# 9. 配置驱动的异常监控

## 9.1 可配置的截图行为

**文件**: config/settings.yaml

```yaml
screenshot:
  on_failure: true  # 失败时自动截图
  path: logs/screenshots  # 截图保存路径
```

**可配置项**：
- ✅ 失败时是否截图
- ✅ 截图保存路径
- ✅ 超时时间
- ✅ 日志级别

---

# 10. 异常监控完整流程

```
1. 测试执行
   ↓
2. 业务逻辑处理
   ↓
3. CheckErrorCapture 检查业务弹窗 (1.5秒快速轮询)
   ↓
4. WebDriverWaitCommon 等待元素
   ↓
5. 元素超时 → 构建 ElementNotFoundError (保留原始异常链)
   ↓
6. 自动截图 → 保存失败现场
   ↓
7. 抛出异常 → pytest_runtest_makereport 捕获
   ↓
8. Pytest 钩子 → 再次截图
   ↓
9. 记录日志 (脱敏处理)
   ↓
10. 测试报告生成
```

---

# 11. 异常监控系统优势总结

| 特性 | 实现 | 收益 |
|------|------|------|
| **异常链追踪** | `from exc` 保留原始异常 | 完整堆栈信息 |
| **上下文保留** | 自定义异常保存定位器、截图、上下文 | 快速定位问题 |
| **自动截图** | 失败即截图 + Pytest 钩子 | 可视化失败现场 |
| **业务监控** | 1.5 秒弹窗检测 | 不拖慢正常用例 |
| **日志脱敏** | SensitiveFilter | 保护敏感信息 |
| **配置驱动** | settings.yaml | 灵活控制开关 |

---

# 12. 建议改进点

1. **异常重试机制**：对网络超时等临时异常增加重试逻辑
2. **异常告警**：失败时自动发送钉钉/企业微信通知
3. **异常聚合**：相同类型的异常合并统计
4. **异常回放**：失败截图 + 操作序列生成测试报告附件

---

# 13. 核心文件索引

| 功能模块 | 文件路径 | 说明 |
|----------|----------|------|
| 异常定义 | common/exceptions.py | FrameworkError 及子类 |
| 元素等待 | common/CommonWebDriverWaitOperation.py | 异常链构建、截图 |
| 业务弹窗检测 | util/CheckErrorCapture.py | 1.5秒快速检测 |
| 截图工具 | util/screenshot_util.py | 统一截图管理 |
| Pytest钩子 | case/conftest.py | 全局失败拦截 |
| 日志系统 | log/user_log.py | 敏感信息脱敏 |
| 配置中心 | config/settings.py | 配置驱动开关 |
