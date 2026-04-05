---
name: ficc-handle
description: >-
  Handle layer UI actions for FiccAccountSelenium—RYLoginHandle,
  RYUserManageHandle, using FindElement and WebDriverWaitCommon. Use when
  editing handle/RY_Handle/*.py or adding page operation sequences.
---

# 模块：Handle（`handle/RY_Handle/`）

## 职责

- **页面怎么做**：点击菜单、填入表单、提交；组合为若干可复用方法（如 `RY_Login_Register_Element`、`RY_UserManage_From_Dict`）。
- 典型成员：`self.driver`、`self.fd = FindElement(driver)`、`self.WebDriver = WebDriverWaitCommon(self.driver)`、`get_logger()`。

## 约定

- 定位：通过 `self.fd.get_Login_element_txt(...)`、`get_UserManageModule_element_txt(...)` 等拿到 **XPath 字符串**（或解析结果），交给 `WebDriver` 的 `click_params` / `send_keys_params`。
- **不**在 Handle 中重复实现「读 INI 解析 by/value」的逻辑（属于 `FindElement`）。
- 字典驱动方法（如 `RY_UserManage_From_Dict`）的 **dict 键**必须与 `config/test_data_yaml/` 中字段名一致。

## 扩展新区块时

1. 在对应 `config/*Element.ini` 增加键值（`by>value` 或 XPath）。
2. 在 `FindElement` 的 `configs_map` 如需新模块则注册（保持 section 名与 INI 一致）。
3. 在 Handle 中按步骤调用 `WebDriver` 方法，保持与现有登录/用户管理相同的错误传播方式（交由上层 Business/Case）。
