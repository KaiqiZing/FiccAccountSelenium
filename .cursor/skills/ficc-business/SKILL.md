---
name: ficc-business
description: >-
  Business layer orchestration for FiccAccountSelenium—RYLoginBusiness,
  RYUserManageBusiness, Allure steps, delegating to Handle. Use when editing
  business/*.py or wiring new workflows from cases.
---

# 模块：Business（`business/`）

## 职责

- 表达**用户可理解的场景**：登录、新增用户、登录+用户管理等。
- 持有对应 **Handle** 实例（如 `RYLoginHandle`、`RYUserManageHandle`），**不**直接操作 `FindElement` 解析细节。
- 用 **`with allure.step(...)`** 包裹主要步骤；异常时 `logger.error` 后 **重新抛出**。

## 现有模式

- **登录**：`RYLoginBusiness.LoginTest` / 用户管理里的 `Login` → 调用 `RYLoginHandle.RY_Login_Register_Element`。
- **用户管理**：`RYUserManageBusiness.AddUser(user_data: dict)` → `RYUserManageHandle.RY_UserManage_From_Dict`；组合场景用 `UserManageTest`。

## 约束

- Case 层应调用 Business 的 **`AddUser`** 等公共方法，避免 Case 直调 Handle。
- 新增 Business 方法时：参数类型与 YAML/Excel 字典键名和 Handle 约定对齐；不要在 Business 里拼接 XPath。

## 文件命名

- 保持 `RY_*_Business.py` 与对应用例域一致；构造 `__init__(self, driver)` 注入 driver。
