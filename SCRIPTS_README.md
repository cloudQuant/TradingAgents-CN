# Scripts 目录说明

本文档详细说明 `scripts/` 目录下所有脚本的用途和使用方法。

> **整理日期**: 2024年  
> **整理结果**: 已将 173 个不常用脚本归档到 `archive/` 目录

---

## 一、目录结构概览（整理后）

```
scripts/                          # 活跃脚本 (~80个)
├── deployment/                   # 部署发布 (6个)
├── development/                  # 开发辅助 (1个)
├── maintenance/                  # 维护管理 (8个)
├── setup/                        # 安装配置 (13个)
├── validation/                   # 验证检查 (6个)
├── docker/                       # Docker相关 (7个)
├── git/                          # Git工具 (3个)
├── migrations/                   # 数据迁移 (5个)
├── archive/                      # 归档脚本 (173个) ⬅️ 历史/调试/一次性脚本
└── *.py / *.sh / *.ps1          # 根目录核心脚本 (~45个)
```

---

## 二、子目录脚本详解

### 📦 setup/ - 安装配置脚本 (13个)

| 脚本 | 用途 |
|------|------|
| `init_database.py` | 初始化数据库结构和索引 |
| `init_mongodb_indexes.py` | 创建MongoDB索引 |
| `initialize_system.py` | 系统初始化 |
| `setup_databases.py` | 数据库设置 |
| `create_financial_data_collection.py` | 创建财务数据集合 |
| `create_historical_data_collection.py` | 创建历史数据集合 |
| `create_message_collections.py` | 创建消息集合 |
| `create_news_data_collection.py` | 创建新闻数据集合 |
| `init_multi_market_collections.py` | 初始化多市场集合 |
| `update_historical_data_indexes.py` | 更新历史数据索引 |
| `check_fund_collection_indexes.py` | 检查基金集合索引 |
| `quick_install.py` | 快速安装依赖 |
| `install_pdf_tools.py` | 安装PDF工具 |

---

### 🔍 validation/ - 验证检查脚本 (6个)

| 脚本 | 用途 |
|------|------|
| `check_system_status.py` | 检查系统状态 |
| `check_dependencies.py` | 检查依赖完整性 |
| `check_imports.py` | 检查导入问题 |
| `check_stock_collections.py` | 检查股票集合 |
| `smart_config.py` | 智能配置检查 |

---

### 🔧 maintenance/ - 维护管理脚本 (8个)

| 脚本 | 用途 |
|------|------|
| `optimize_mongodb_indexes.py` | 优化MongoDB索引 |
| `cleanup_cache.py` | 清理缓存 |
| `sync_upstream.py` | 同步上游仓库 |
| `version_manager.py` | 版本管理 |
| `branch_manager.py` | 分支管理 |
| `cleanup_duplicate_stocks.py` | 清理重复股票数据 |
| `fix_mongodb_reports.py` | 修复MongoDB报告 |
| `fix_timezone_data.py` | 修复时区数据 |

---

### 🛠️ development/ - 开发辅助脚本 (1个)

| 脚本 | 用途 |
|------|------|
| `adaptive_cache_manager.py` | 自适应缓存管理 |

---

### 🚀 deployment/ - 部署发布脚本 (6个)

| 脚本 | 用途 |
|------|------|
| `create_github_release.py` | 创建GitHub发布 |
| `build_portable_package.ps1` | 构建便携包 |
| `sync_and_build_only.ps1` | 同步并构建 |
| `sync_to_portable.ps1` | 同步到便携版 |
| `verify_venv.ps1` | 验证虚拟环境 |

---

### 🐳 docker/ - Docker相关脚本 (7个)

| 脚本 | 用途 |
|------|------|
| `start_docker_services.sh` | 启动Docker服务 (Linux) |
| `start_docker_services.bat` | 启动Docker服务 (Windows) |
| `stop_docker_services.sh` | 停止Docker服务 (Linux) |
| `stop_docker_services.bat` | 停止Docker服务 (Windows) |
| `mongo-init.js` | MongoDB初始化脚本 |
| `docker-compose-start.bat` | Docker Compose启动 |

---

### 📋 git/ - Git工具脚本 (3个)

| 脚本 | 用途 |
|------|------|
| `upstream_git_workflow.sh` | 上游Git工作流 |
| `branch_manager.py` | 分支管理器 |

---

### 🔄 migrations/ - 数据迁移脚本 (5个)

| 脚本 | 用途 |
|------|------|
| `standardize_stock_code_fields.py` | 标准化股票代码字段 |
| `migrate_stock_basic_info_add_source_index.py` | 添加来源索引 |
| `add_symbol_field_to_stock_basic_info.py` | 添加symbol字段 |
| `fix_stock_basic_info_symbol.py` | 修复symbol字段 |
| `migrate_financial_data_add_symbol.py` | 迁移财务数据 |

---

## 三、根目录重要脚本

### 🔑 核心脚本

| 脚本 | 用途 | 重要性 |
|------|------|--------|
| `create_default_admin.py` | 创建默认管理员用户 | ⭐⭐⭐ 高 |
| `create_default_users.py` | 创建默认用户 | ⭐⭐⭐ 高 |
| `init_system_data.py` | 初始化系统数据 | ⭐⭐⭐ 高 |
| `init_scheduler_metadata.py` | 初始化调度器元数据 | ⭐⭐⭐ 高 |
| `init_paper_trading_market_rules.py` | 初始化模拟交易规则 | ⭐⭐⭐ 高 |
| `generate_stock_collections.py` | 生成股票集合代码 | ⭐⭐⭐ 高 |
| `user_password_manager.py` | 用户密码管理 | ⭐⭐⭐ 高 |
| `user_manager.ps1` / `.bat` | 用户管理脚本 | ⭐⭐⭐ 高 |
| `mongo-init.js` | MongoDB初始化 | ⭐⭐⭐ 高 |
| `container_init.sh` | 容器初始化 | ⭐⭐⭐ 高 |

### 🔧 构建与部署

| 脚本 | 用途 | 重要性 |
|------|------|--------|
| `build-amd64.sh` / `.ps1` | AMD64架构构建 | ⭐⭐⭐ 高 |
| `build-arm64.sh` | ARM64架构构建 | ⭐⭐⭐ 高 |
| `build-multiarch.sh` / `.ps1` | 多架构构建 | ⭐⭐⭐ 高 |
| `build-and-publish-linux.sh` | Linux构建发布 | ⭐⭐⭐ 高 |
| `publish-docker-images.sh` / `.ps1` | 发布Docker镜像 | ⭐⭐⭐ 高 |
| `deploy_demo.sh` | 部署演示环境 | ⭐⭐ 中 |
| `full_redeploy_linux.sh` | Linux完整重新部署 | ⭐⭐ 中 |
| `docker-init.sh` / `.ps1` | Docker初始化 | ⭐⭐ 中 |
| `docker_init.ps1` | Docker初始化(增强版) | ⭐⭐ 中 |
| `start_docker.sh` / `.ps1` | 启动Docker | ⭐⭐ 中 |
| `easy_install.sh` / `.ps1` | 简易安装 | ⭐⭐ 中 |
| `smart_start.sh` / `.ps1` | 智能启动 | ⭐⭐ 中 |

### 📊 数据同步与管理

| 脚本 | 用途 | 重要性 |
|------|------|--------|
| `akshare_sync_optimized.py` | AKShare优化同步 | ⭐⭐ 中 |
| `sync_akshare_catalog.py` | 同步AKShare目录 | ⭐⭐ 中 |
| `sync_financial_data.py` | 同步财务数据 | ⭐⭐ 中 |
| `sync_market_news.py` | 同步市场新闻 | ⭐⭐ 中 |
| `unified_data_manager.py` | 统一数据管理 | ⭐⭐ 中 |
| `download_finnhub_data.py` | 下载Finnhub数据 | ⭐ 低 |
| `fetch_all_etf_dividend_sina.py` | 获取ETF分红数据 | ⭐ 低 |

### 🔍 诊断与检查

| 脚本 | 用途 | 重要性 |
|------|------|--------|
| `diagnose_system.py` | 系统诊断 | ⭐⭐⭐ 高 |
| `diagnose_env_vars.py` | 环境变量诊断 | ⭐⭐ 中 |
| `diagnose_empty_data.py` | 空数据诊断 | ⭐⭐ 中 |
| `diagnose_nginx.ps1` | Nginx诊断 | ⭐⭐ 中 |
| `log_analyzer.py` | 日志分析器 | ⭐⭐ 中 |
| `view_logs.py` | 查看日志 | ⭐⭐ 中 |
| `get_container_logs.py` | 获取容器日志 | ⭐⭐ 中 |
| `check_api_config.py` | 检查API配置 | ⭐⭐ 中 |
| `check_config_coverage.py` | 检查配置覆盖率 | ⭐⭐ 中 |

### 🔄 迁移脚本

| 脚本 | 用途 | 重要性 |
|------|------|--------|
| `migrate_auth_to_db.py` | 迁移认证到数据库 | ⭐⭐ 中 |
| `migrate_config.py` | 迁移配置 | ⭐⭐ 中 |
| `migrate_config_to_db.py` | 迁移配置到数据库 | ⭐⭐ 中 |
| `migrate_config_to_webapi.py` | 迁移配置到WebAPI | ⭐⭐ 中 |
| `migrate_data_directories.py` | 迁移数据目录 | ⭐⭐ 中 |
| `migrate_to_unified_logging.py` | 迁移到统一日志 | ⭐ 低 |
| `migrate_user_preferences.py` | 迁移用户偏好 | ⭐ 低 |
| `migrate_users_to_api.py` | 迁移用户到API | ⭐ 低 |

---

## 四、归档目录 (archive/)

已将 **173个** 不常用脚本移动到 `scripts/archive/` 目录，按类别组织：

| 子目录 | 内容 | 数量 |
|--------|------|------|
| `specific_stock_checks/` | 特定股票检查脚本 | 6 |
| `historical_releases/` | 历史版本发布脚本 | 4 |
| `one_time_migrations/` | 一次性迁移脚本 | 9 |
| `debug_tests/` | 调试和测试脚本 | 26 |
| `issue_fixes/` | 特定问题修复脚本 | 7 |
| `docs_analysis/` | 文档和分析脚本 | 8 |
| `backup_restore/` | 备份恢复脚本 | 8 |
| `redundant/` | 冗余/重复脚本 | 105 |

如需使用归档脚本，请先检查其兼容性。详见 `scripts/archive/README.md`。

---

## 五、总结

| 统计项 | 整理前 | 整理后 |
|--------|--------|--------|
| **活跃脚本** | ~336个 | ~80个 |
| **归档脚本** | 0 | 173个 |
| **已删除** | 0 | 3个 (.pkl/.json临时文件) |

**整理效果**：scripts 主目录从 336 个文件精简到约 80 个核心脚本，目录结构更加清晰。
