---
name: ficc-config
description: >-
  Unified Config singleton and config files for FiccAccountSelenium—settings.yaml,
  legacy base_config merge, element INIs, test YAML paths. Use when changing
  config/settings.py, YAML/INI, or env-specific keys.
---

# 模块：Config（`config/`）

## `settings.py` · `Config`

- **单例**；加载 `config/settings.yaml`。
- **`get("a.b.c", default?)`**：点路径访问；缺失且无 default 时抛 **`ConfigError`**。
- **`get_env_config()`**：读取 `env.<active>` 下字典，供 `base_url`、`timeout`、`browser` 等使用。
- **Legacy**：若 `settings.yaml` 中 `legacy.base_config_file` 指向旧文件，会将其中 `global_config` 合并进当前环境（如默认 `base_url`、`timeout`）。

## 元素配置

- `*Element.ini`：`FindElement` 使用的 section/key；修改 key 时同步 **INI、FindElement 快捷方法、Handle 调用名**。

## 测试数据 YAML

- 位于 `config/test_data_yaml/`；由 `DataFactory.get_yaml` 加载；模板占位符见 `AccountUtils` 注册生成器。

## 注意事项

- 勿在业务代码中硬编码环境 URL；优先 `Config` + `settings.yaml` 的 `env.active` 切换。
- 新增配置项时更新示例或团队内文档，避免 `get` 键名漂移。
