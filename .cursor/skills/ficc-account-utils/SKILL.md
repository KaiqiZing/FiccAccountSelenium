---
name: ficc-account-utils
description: >-
  AccountUtils template generators and related helpers for FiccAccountSelenium test
  data placeholders. Use when editing AccountUtils/ or registering new template
  functions for YAML-driven tests.
---

# 模块：AccountUtils（`AccountUtils/`）

## 与数据工厂的关系

- `DataFactory` 初始化时会 **`register_template_generators()`**（见 `AccountUtils/template_generators.py` 及包内注册逻辑）。
- YAML 中占位符经 **`TemplateParser`** 解析；生成器负责 **`{xxx}`** 或项目约定的模板语法（以实现为准）。

## 扩展生成器

1. 在 `AccountUtils` 下实现纯函数或小型类方法，**无副作用**、适合测试数据（随机串、身份证规则、密码策略等）。
2. 在 **`register_template_generators`** 中注册名称与可调用对象，保证与 YAML 键引用一致。
3. 用户管理密码等字段应使用**语义正确**的生成器，避免误用邮箱等占位符。

## 原则

- 生成逻辑与 **业务断言** 解耦：生成器只负责数据形状与合法性，不依赖 `driver`。
- 新增依赖若较重，考虑放入 `requirements-ocr.txt` 或可选依赖，并保持核心 `requirements.txt` 可安装可跑 CI collect。

## 目录

- `generators/`、`template_generators.py` 等为常见入口；修改后运行相关 YAML 用例做快速验证。
