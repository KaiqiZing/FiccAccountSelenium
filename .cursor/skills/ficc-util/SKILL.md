---
name: ficc-util
description: >-
  DriverFactory, DataFactory, loaders, cache, screenshot, error popup check, and
  logging for FiccAccountSelenium util/ and log/. Use when adding drivers, data
  sources, or execution helpers in this repo.
---

# 模块：Util & Log（`util/`、`log/`）

## `driver_factory.py` · `DriverFactory`

- **`create_driver(browser_type=None, headless=None)`**：从 `Config` 读 `browser` 块（类型、headless、隐式等待、页超时、窗口）。
- 优先 **`webdriver-manager`**（若已安装）；否则本地 `chrome_driver_path` 或 Selenium 默认行为，并打日志 warning。

## `data_factory.py` · `DataFactory`

- **单例**；注册 `YamlLoader`、`IniLoader`、`ExcelLoader`；可按需 `register_loader`（如 DB）。
- **`get(source_type, source_id, parse=True, **kwargs)`**：按 Loader 的 **`CACHE_STRATEGY`**（`static` / `template` / `volatile`）与 `CacheManager` 协作。
- 便捷方法：`get_yaml`、`get_ini`、`get_excel`、`get_db`。
- **`DataManager`**（`data_manager.py`）为 **`DataFactory` 别名**，旧代码兼容。

## 运行辅助

- **`screenshot_util.py`**：统一截图路径策略；失败与业务错误场景复用。
- **`CheckErrorCapture.py`**：`check_and_capture_error(driver)` — 短超时检测 Element UI 错误提示，避免拖慢成功用例。
- **`run_tests.py`**：封装 smoke/regression/all/allure 模式。

## `log/user_log.py`

- 各层通过 **`get_logger()`** 取 logger；保持级别与格式与现有用例输出一致。

## 扩展数据源

1. 在 `util/loaders/` 实现 Loader（`source_type`、`CACHE_STRATEGY`、`load`、`cache_key`）。
2. 在 `DataFactory._register_default_loaders` 或运行时 `register_loader` 注册。
