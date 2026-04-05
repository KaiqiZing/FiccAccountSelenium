---
name: ficc-base
description: >-
  Locator-only layer FindElement in FiccAccountSelenium base/find_element.py—INI
  parsing, caching, no WebDriver calls. Use when adding locator keys or modules
  in config/*.ini or editing FindElement.
---

# 模块：Base（`base/find_element.py`）

## 职责

- **仅**从 INI 读取并解析定位串为内部使用的 `(by, value)` 或对外暴露 **XPath 字符串**（供 `WebDriverWaitCommon` 使用 `By.XPATH`）。
- **禁止**在本类中调用 `driver.find_element`、点击、等待等任何浏览器操作。

## `configs_map`

- 键为逻辑模块名（如 `login`、`UserManageModule`）；值为 `(ReadIni(...), "SectionName")`，**SectionName** 必须与 INI 文件 `[Section]` 完全一致。
- 新增页面模块：增加 INI 文件、`ReadIni` 路径、此处映射与快捷方法（如 `get_XXX_element_txt`）。

## 缓存

- `_parse_locator` 使用 `locator_cache`，避免重复读盘与解析。

## 格式

- INI 值支持 `by>value`；单段则按 XPath 处理；兼容 `>//...` 缺省 `by` 时默认 `xpath`。

## 兼容说明

- 构造仍可接收 `driver` 参数，仅为历史兼容；业务上与 WebDriver 解耦。
