---
name: ficc-common
description: >-
  WebDriverWaitCommon explicit waits and framework exceptions in FiccAccountSelenium
  common/. Use when editing CommonWebDriverWaitOperation.py or exceptions.py.
---

# 模块：Common（`common/`）

## `WebDriverWaitCommon`（`CommonWebDriverWaitOperation.py`）

- **职责**：显式等待（可见、可点击、消失等）与封装后的 **点击、输入** 等动作入口（如 `click_params`、`send_keys_params`）。
- **超时**：默认从 `Config().get_env_config()` 的 `timeout` 读取；构造参数可覆盖。
- **定位器**：支持 `(By, str)` 元组或 XPath 字符串；内部 `_resolve_locator` 统一解析。
- **失败**：`TimeoutException` 时构造 **`ElementNotFoundError`**，可附带 `ScreenshotUtil.capture` 路径。

## 异常（`exceptions.py`）

- `FrameworkError` 基类；常用子类：`ElementNotFoundError`、`ConfigError`、`BusinessError`。
- 扩展新业务异常时继承 `FrameworkError`，保留 `message` 及必要的结构化字段（如 `config_key`）。

## 原则

- Handle 层对「等元素 + 操作」的重复逻辑应收敛到此模块，避免各处复制 `WebDriverWait` 样板代码。
