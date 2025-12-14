# 🛠️ 开发环境配置指南

## 📋 概述

本文档介绍如何配置 TradingAgents-CN 的开发环境，包括 Docker 映射配置和快速调试方法。

## 🐳 Docker 开发环境

### Volume 映射配置

项目已配置了以下目录映射，支持实时代码更新：

```yaml
volumes:

  - .env:/app/.env

# 开发环境代码映射

  - ./web:/app/web                    # Web 界面代码
  - ./tradingagents:/app/tradingagents # 核心分析代码
  - ./scripts:/app/scripts            # 脚本文件
  - ./test_conversion.py:/app/test_conversion.py # 测试脚本

```bash

### 启动开发环境

```bash

# 停止现有服务

docker-compose down

# 启动开发环境（带 volume 映射）

docker-compose up -d

# 查看服务状态

docker-compose ps

```bash

## 🔧 快速调试流程

### 1. 代码修改

在本地开发目录直接修改代码，无需重新构建镜像。

### 2. 测试转换功能

```bash

# 运行独立转换测试

docker exec TradingAgents-web python test_conversion.py

# 查看容器日志

docker logs TradingAgents-web --follow

# 进入容器调试

docker exec -it TradingAgents-web bash

```bash

### 3. Web 界面测试

- 访问: <http://localhost:8501>
- 修改代码后刷新页面即可看到更新

## 📁 目录结构说明

```bash
TradingAgentsCN/
├── web/                    # Web 界面代码 (映射到容器)

│   ├── app.py             # 主应用

│   ├── utils/             # 工具模块

│   │   ├── report_exporter.py  # 报告导出

│   │   └── docker_pdf_adapter.py # Docker 适配器

│   └── pages/             # 页面模块

├── tradingagents/         # 核心分析代码 (映射到容器)

├── scripts/               # 脚本文件 (映射到容器)

├── test_conversion.py     # 转换测试脚本 (映射到容器)

└── docker-compose.yml     # Docker 配置

```bash

## 🧪 调试技巧

### 1. 实时日志监控

```bash

# 监控 Web 应用日志

docker logs TradingAgents-web --follow

# 监控所有服务日志

docker-compose logs --follow

```bash

### 2. 容器内调试

```bash

# 进入 Web 容器

docker exec -it TradingAgents-web bash

# 检查 Python 环境

docker exec TradingAgents-web python --version

# 检查依赖

docker exec TradingAgents-web pip list | grep pandoc

```bash

### 3. 文件同步验证

```bash

# 检查文件是否同步

docker exec TradingAgents-web ls -la /app/web/utils/

# 检查文件内容

docker exec TradingAgents-web head -10 /app/test_conversion.py

```bash

## 🔄 开发工作流

### 标准开发流程

1. **修改代码**- 在本地 IDE 中编辑

2.**保存文件**- 自动同步到容器
3.**测试功能**- 刷新 Web 页面或运行测试脚本
4.**查看日志**- 检查错误和调试信息
5.**迭代优化**- 重复上述步骤

### 导出功能调试流程

1.**修改导出代码**- 编辑 `web/utils/report_exporter.py`
2.**运行转换测试**- `docker exec TradingAgents-web python test_conversion.py`
3.**检查结果**- 查看生成的测试文件
4.**Web 界面测试**- 在浏览器中测试实际导出功能

## ⚠️ 注意事项

### 文件权限

- Windows 用户可能遇到文件权限问题
- 确保 Docker 有权限访问项目目录

### 性能考虑

- Volume 映射可能影响 I/O 性能
- 生产环境建议使用镜像构建方式

### 依赖更新

- 修改 requirements.txt 后需要重新构建镜像
- 添加新的系统依赖需要更新 Dockerfile

## 🚀 生产部署

开发完成后，生产部署流程：

```bash

# 1. 停止开发环境

docker-compose down

# 2. 重新构建镜像

docker build -t tradingagents-cn:latest .

# 3. 启动生产环境（不使用 volume 映射）

# 修改 docker-compose.yml 移除 volume 映射

docker-compose up -d

```bash

## 💡 最佳实践

1.**代码同步**- 确保本地修改及时保存
2.**日志监控**- 保持日志窗口开启
3.**增量测试**- 小步快跑，频繁测试
4.**备份重要**- 定期提交代码到 Git
5.**环境隔离**- 开发和生产环境分离

## 🎯 功能开发指南

### 导出功能开发

如果需要修改或扩展导出功能：

1.**核心文件位置**

   ```

   web/utils/report_exporter.py     # 主要导出逻辑
   web/utils/docker_pdf_adapter.py  # Docker 环境适配
   test_conversion.py               # 转换功能测试
   ```

1. **关键修复点**

   ```python

# YAML 解析问题修复
   extra_args = ['--from=markdown-yaml_metadata_block']

# 内容清理函数
   def _clean_markdown_for_pandoc(self, content: str) -> str:

# 保护表格分隔符，清理 YAML 冲突字符
   ```

1. **测试流程**

   ```bash

# 测试基础转换功能
   docker exec TradingAgents-web python test_conversion.py
   ```

### Memory 功能开发

如果遇到 memory 相关错误：

1. **安全检查模式**

   ```python

# 在所有使用 memory 的地方添加检查
   if memory is not None:
       past_memories = memory.get_memories(curr_situation, n_matches=2)
   else:
       past_memories = []
   ```

1. **相关文件**

   ```

   tradingagents/agents/researchers/bull_researcher.py
   tradingagents/agents/researchers/bear_researcher.py
   tradingagents/agents/managers/research_manager.py
   tradingagents/agents/managers/risk_manager.py
   ```

### 缓存功能开发

处理缓存相关错误：

1. **类型安全检查**

   ```python

# 检查数据类型，避免 'str' object has no attribute 'empty'
   if cached_data is not None:
       if hasattr(cached_data, 'empty') and not cached_data.empty:

# DataFrame 处理
       elif isinstance(cached_data, str) and cached_data.strip():

# 字符串处理
   ```

1. **相关文件**

   ```

   tradingagents/dataflows/tushare_adapter.py
   tradingagents/dataflows/tushare_utils.py
   tradingagents/dataflows/cache_manager.py
   ```

## 🚀 部署指南

### 生产环境部署

开发完成后的部署流程：

1. **停止开发环境**

   ```bash
   docker-compose down
   ```

1. **移除 volume 映射**

   ```yaml

# 编辑 docker-compose.yml，注释掉开发映射

# volumes:

# - ./web:/app/web

# - ./tradingagents:/app/tradingagents
   ```

1. **重新构建镜像**

   ```bash
   docker build -t tradingagents-cn:latest .
   ```

1. **启动生产环境**

   ```bash
   docker-compose up -d
   ```

### 版本发布

1. **更新版本号**

   ```bash
   echo "cn-0.1.8" > VERSION
   ```

1. **提交代码**

   ```bash
   git add .
   git commit -m "🎉 发布 v0.1.8 - 导出功能完善"
   git tag cn-0.1.8
   git push origin develop --tags
   ```

1. **更新文档**
   - 更新 README.md 中的版本信息
   - 更新 VERSION_*.md 发布说明
   - 更新相关功能文档

- --

- 最后更新: 2025-07-13*
- 版本: v0.1.7*
