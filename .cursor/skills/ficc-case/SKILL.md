---
name: ficc-case
description: >-
  Pytest cases, conftest fixtures, Excel parametrization, and Allure annotations
  for FiccAccountSelenium under case/. Use when editing case/*.py or pytest hooks
  in this repo.
---

# 模块：Case（`case/`）

## 职责

- 用例入口：组装数据、调用 **Business**，断言或 `pytest.fail`。
- **不**在此层写页面定位字符串或复杂显式等待（交给 Handle + `WebDriverWaitCommon`）。

## `conftest.py` 要点

- **`driver`**：`DriverFactory.create_driver()`，打开 `get_base_url()` 后 `yield`，结束 `quit()`。
- **Excel 场景**：若存在 fixture `should_run` 且为 `False`，**不启动浏览器**（仅占位失败用例）。
- **`get_base_url()`**：优先 `Config().get_env_config()`；兜底 `DataFactory` + `base_config.yaml`。
- **`pytest_runtest_makereport`**：setup/call 失败时对有效 `driver` 截图，受 `screenshot.on_failure` 控制。

## 数据驱动

- **Excel**：`pytest_generate_tests` 注入 `should_run, row_num, username, password`；加载失败时单条占位并携带错误信息。
- **YAML**：通过 `DataFactory` / `DataManager` 取数，字段名与 Handle 中 `dict.get(...)` **一致**。

## Allure

- 类/函数级：`@allure.feature`、`@allure.story`；步骤级主要在 Business，Case 可增加高层 step。

## 收集规则

- 由根目录 `pytest.ini` 限定：`testpaths = case`，文件名模式含 `*TestModule*.py` 等。
