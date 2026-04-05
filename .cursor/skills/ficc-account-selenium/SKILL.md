---
name: ficc-account-selenium
description: >-
  Master guide for the FiccAccountSelenium workspace—Selenium 4, Pytest, Allure,
  layered Case/Business/Handle/Base/Common, Config singleton, DataFactory, CI
  with Ruff. Use when adding or refactoring UI automation, tests, or framework
  code in this repository.
---

# FiccAccountSelenium（总项目）

## 适用范围

在本仓库内编写、重构或评审 **UI 自动化** 与 **框架代码** 时优先遵循本文；目录级细节见同目录下各 **分模块** skill（`ficc-case`、`ficc-business` 等）。

## 技术栈（以仓库为准）

- Python 3.11+（CI 使用 3.11）
- Selenium 4、`pytest`、`allure-pytest`
- 配置与数据：`PyYAML`、Excel（`openpyxl` / `pandas`）
- 静态检查：`ruff`（`pyproject.toml`）

## 分层约束（必须遵守）

调用方向只允许：**Case → Business → Handle**；Case **不**直接调 Handle（YAML/用户管理等场景通过 Business 的 `AddUser` 等入口）。

| 层级 | 目录 | 职责 |
|------|------|------|
| 用例 | `case/` | Pytest、参数化、`conftest`、Allure 标注 |
| 业务 | `business/` | 场景编排、`allure.step`、组合多个 Handle |
| 操作 | `handle/RY_Handle/` | 页面操作：输入、点击、与 `FindElement` + `WebDriverWaitCommon` 配合 |
| 定位 | `base/` | `FindElement`：仅解析 INI，不写 WebDriver 逻辑 |
| 公共 | `common/` | 显式等待封装、框架异常类型 |

横切：`config/`（`Config`）、`util/`（驱动与数据工厂、截图等）、`log/`、`AccountUtils/`（生成器与模板注册）。

## 配置与数据

- 运行与环境：`config/settings.yaml` + `config/settings.py`（单例、点路径 `get`）；`base_url` / `timeout` 等走当前环境块。
- 元素：`config/*Element.ini`，由 `FindElement` 按模块名映射读取。
- 测试数据：`config/test_data_yaml/`、Excel（如 `config/RYAccountData.xlsx`）；统一经 **`DataFactory`**（`DataManager` 为其别名）。

## 运行与质量

- 用例收集规则见根目录 `pytest.ini`；多模式入口 `run_tests.py`。
- PR/推送：`/.github/workflows/ci.yml` — Ruff + `pytest --collect-only`。
- 架构总览文档：`docs/ARCHITECTURE.md`。

## 分模块 skill 索引

按需读取（与本项目路径绑定，不依赖外部 skill）：

- `ficc-case` — `case/`、`conftest`、参数化
- `ficc-business` — `business/`
- `ficc-handle` — `handle/`
- `ficc-base` — `base/find_element.py`
- `ficc-common` — `common/` 等待与异常
- `ficc-config` — `config/settings`、INI/YAML 约定
- `ficc-util` — `util/` 驱动工厂、数据工厂、截图与错误检测、`log/`
- `ficc-account-utils` — `AccountUtils/` 生成器与模板扩展

## Selenium 与代码风格（摘要）

- 使用 Selenium 4 API；元素交互优先通过 **`WebDriverWaitCommon`**（`click_params`、`send_keys_params` 等），避免在 Handle 中重复裸 `WebDriverWait`。
- 新增依赖写入 `requirements.txt`；可选/重型依赖可拆到 `requirements-ocr.txt` 等。
- 改动保持与现有文件命名、日志、`allure` 用法一致。
