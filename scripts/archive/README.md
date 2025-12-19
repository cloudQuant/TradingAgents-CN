# 归档脚本目录

此目录包含已归档的脚本，这些脚本不再日常使用，但保留以供参考。

## 目录结构

| 目录 | 内容 | 数量 |
|------|------|------|
| `specific_stock_checks/` | 特定股票检查脚本 | 6 |
| `historical_releases/` | 历史版本发布脚本 | 4 |
| `one_time_migrations/` | 一次性迁移脚本 | 9 |
| `debug_tests/` | 调试和测试脚本 | 26 |
| `issue_fixes/` | 特定问题修复脚本 | 7 |
| `docs_analysis/` | 文档和分析脚本 | 8 |
| `backup_restore/` | 备份恢复脚本 | 8 |
| `redundant/` | 冗余/重复脚本 | 105 |

## 说明

- **归档时间**: 2024年
- **归档原因**: 清理 scripts 目录，保持主目录整洁
- **使用建议**: 如需使用归档脚本，请先检查其兼容性

## 各目录详情

### specific_stock_checks/
检查特定股票数据的脚本，如 `check_000001_data.py`、`check_688788_info.py` 等。

### historical_releases/
历史版本的发布脚本，如 `release_v0.1.2.py`、`release_v0.1.3.py` 等。

### one_time_migrations/
已完成的一次性数据迁移脚本，如字段迁移、配置清理等。

### debug_tests/
开发调试和测试脚本，如港股测试、PE/PB测试等。

### issue_fixes/
针对特定问题的修复脚本，如数据诊断、配置修复等。

### docs_analysis/
文档生成和代码分析脚本。

### backup_restore/
数据备份和恢复脚本，特定环境使用。

### redundant/
功能重复或已被替代的脚本。
