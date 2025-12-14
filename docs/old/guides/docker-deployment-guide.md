# 🐳 Docker 部署使用指南

## 📋 概述

TradingAgents-CN v0.1.7 引入了完整的 Docker 容器化部署方案，让您可以通过一条命令启动完整的股票分析环境。本指南将详细介绍如何使用 Docker 部署和管理 TradingAgents-CN。

## 🎯 Docker 部署优势

### 为什么选择 Docker？

- ✅ **一键部署**: `docker-compose up -d` 启动完整环境
- ✅ **环境一致**: 开发、测试、生产环境完全一致
- ✅ **依赖管理**: 自动处理所有依赖和版本冲突
- ✅ **服务集成**: Web 应用、数据库、缓存一体化
- ✅ **易于维护**: 简化更新、备份、恢复流程

### 与传统部署对比

| 特性 | 传统部署 | Docker 部署 |

|------|---------|-----------|

| **部署时间**| 30-60 分钟 | 5-10 分钟 |

|**环境配置**| 复杂手动配置 | 自动化配置 |

|**依赖管理**| 手动安装 | 自动处理 |

|**服务管理**| 分别启动 | 统一管理 |

|**故障排除**| 复杂 | 简化 |

## 🚀 快速开始

### 前置要求

| 组件 | 最低版本 | 推荐版本 | 安装方法 |

|------|---------|----------|----------|

|**Docker**| 20.0+ | 最新版 | [官方安装指南](<https://docs.docker.com/get-docker/)> |

|**Docker Compose**| 2.0+ | 最新版 | 通常随 Docker 一起安装 |

|**内存**| 4GB | 8GB+ | 系统要求 |

|**磁盘空间** | 10GB | 20GB+ | 存储要求 |

### 安装 Docker

#### Windows

```bash

# 1. 下载 Docker Desktop

# <https://www.docker.com/products/docker-desktop>

# 2. 安装并启动 Docker Desktop

# 3. 验证安装

docker --version
docker-compose --version

```bash

#### Linux (Ubuntu/Debian)

```bash

# 1. 更新包索引

sudo apt update

# 2. 安装 Docker

sudo apt install docker.io docker-compose

# 3. 启动 Docker 服务

sudo systemctl start docker
sudo systemctl enable docker

# 4. 添加用户到 docker 组

sudo usermod -aG docker $USER

# 5. 验证安装

docker --version
docker-compose --version

```bash

#### macOS

```bash

# 1. 使用 Homebrew 安装

brew install --cask docker

# 2. 启动 Docker Desktop

# 3. 验证安装

docker --version
docker-compose --version

```bash

## 🔧 部署步骤

### 步骤 1: 获取代码

```bash

# 克隆项目

git clone <https://github.com/hsliuping/TradingAgents-CN.git>
cd TradingAgents-CN

# 检查版本

cat VERSION

```bash

### 📦 关于 Docker 镜像

- *重要说明**: TradingAgents-CN 目前不提供预构建的 Docker 镜像，需要在本地构建。

#### 为什么需要本地构建？

1. **定制化需求**: 不同用户可能需要不同的配置
2. **安全考虑**: 避免在公共镜像中包含敏感信息
3. **版本灵活性**: 支持用户自定义修改和扩展
4. **依赖优化**: 根据实际需求安装依赖

#### 构建过程说明

```bash

# Docker 构建过程包括：

1. 下载基础镜像 (python:3.10-slim) - 约 200MB
2. 安装系统依赖 (pandoc, wkhtmltopdf, 中文字体) - 约 300MB
3. 安装 Python 依赖 (requirements.txt) - 约 500MB
4. 复制应用代码 - 约 50MB
5. 配置运行环境

# 总镜像大小约 1GB，首次构建需要 5-10 分钟

```bash

### 步骤 2: 配置环境

```bash

# 复制配置模板

cp .env.example .env

# 编辑配置文件

# Windows: notepad .env

# Linux/macOS: nano .env

```bash

#### 必需配置

```bash

# === LLM 模型配置 (至少配置一个) ===

# DeepSeek (推荐 - 成本低)

DEEPSEEK_API_KEY=sk-your_deepseek_api_key_here
DEEPSEEK_ENABLED=true

# 阿里百炼 (推荐 - 中文优化)

QWEN_API_KEY=your_qwen_api_key
QWEN_ENABLED=true

# Google AI (推荐 - 推理能力强)

GOOGLE_API_KEY=your_google_api_key
GOOGLE_ENABLED=true

```bash

#### 可选配置

```bash

# === 数据源配置 ===

TUSHARE_TOKEN=your_tushare_token
FINNHUB_API_KEY=your_finnhub_key

# === 导出功能配置 ===

EXPORT_ENABLED=true
EXPORT_DEFAULT_FORMAT=word,pdf

# === Docker 特定配置 ===

MONGODB_URL=mongodb://mongodb:27017/tradingagents
REDIS_URL=redis://redis:6379

```bash

### 步骤 3: 构建并启动服务

```bash

# 首次启动：构建镜像并启动所有服务

docker-compose up -d --build

# 注意：首次运行会自动构建 Docker 镜像，包含以下步骤：

# - 下载基础镜像 (python:3.10-slim)

# - 安装系统依赖 (pandoc, wkhtmltopdf 等)

# - 安装 Python 依赖

# - 复制应用代码

# 整个过程需要 5-10 分钟，请耐心等待

# 后续启动（镜像已构建）：

# docker-compose up -d

# 查看服务状态

docker-compose ps

# 查看启动日志

docker-compose logs -f

```bash

### 步骤 4: 验证部署

```bash

# 检查服务状态

docker-compose ps

# 应该看到以下服务运行中:

# - TradingAgents-web (Web 应用)

# - TradingAgents-mongodb (数据库)

# - TradingAgents-redis (缓存)

# - TradingAgents-mongo-express (数据库管理)

# - TradingAgents-redis-commander (缓存管理)

```bash

### 步骤 5: 访问应用

| 服务 | 地址 | 用途 |

|------|------|------|

| **主应用**| <http://localhost:8501> | 股票分析界面 |

|**数据库管理**| <http://localhost:8081> | MongoDB 管理 |

|**缓存管理**| <http://localhost:8082> | Redis 管理 |

## 🎯 使用指南

### 进行股票分析

1.**访问主界面**: <http://localhost:8501>

1. **选择 LLM 模型**: 推荐 DeepSeek V3（成本低）
2. **输入股票代码**:
   - A 股: 000001, 600519, 000858
   - 美股: AAPL, TSLA, MSFT
1. **选择分析深度**: 快速/标准/深度
2. **开始分析**: 点击"开始分析"按钮
3. **导出报告**: 选择 Word/PDF/Markdown 格式

### 管理数据库

1. **访问 MongoDB 管理**: <http://localhost:8081>
2. **查看分析结果**: 浏览 tradingagents 数据库
3. **管理数据**: 查看、编辑、删除分析记录

### 管理缓存

1. **访问 Redis 管理**: <http://localhost:8082>
2. **查看缓存数据**: 浏览缓存的股价和分析数据
3. **清理缓存**: 删除过期或无用的缓存

## 🔧 日常管理

### 服务管理

```bash

# 启动服务

docker-compose up -d

# 停止服务

docker-compose down

# 重启服务

docker-compose restart

# 查看服务状态

docker-compose ps

# 查看服务日志

docker-compose logs -f web
docker-compose logs -f mongodb
docker-compose logs -f redis

```bash

### 数据管理

```bash

# 备份数据

docker exec TradingAgents-mongodb mongodump --out /backup
docker exec TradingAgents-redis redis-cli BGSAVE

# 清理缓存

docker exec TradingAgents-redis redis-cli FLUSHALL

# 查看数据使用情况

docker exec TradingAgents-mongodb mongo --eval "db.stats()"

```bash

### 更新应用

```bash

# 1. 停止服务

docker-compose down

# 2. 更新代码

git pull origin main

# 3. 重新构建镜像

docker-compose build

# 4. 启动服务

docker-compose up -d

```bash

## 🚨 故障排除

### 常见问题

#### 1. 端口冲突

- *问题**: 服务启动失败，提示端口被占用

- *解决方案**:

```bash

# 检查端口占用

netstat -tulpn | grep :8501

# 修改端口配置

# 编辑 docker-compose.yml，修改端口映射

ports:

  - "8502:8501"  # 改为其他端口

```bash

#### 2. 内存不足

- *问题**: 容器启动失败或运行缓慢

- *解决方案**:

```bash

# 检查内存使用

docker stats

# 增加 Docker 内存限制

# Docker Desktop -> Settings -> Resources -> Memory

# 建议分配至少 4GB 内存

```bash

#### 3. 数据库连接失败

- *问题**: Web 应用无法连接数据库

- *解决方案**:

```bash

# 检查数据库容器状态

docker logs TradingAgents-mongodb

# 检查网络连接

docker exec TradingAgents-web ping mongodb

# 重启数据库服务

docker-compose restart mongodb

```bash

#### 4. API 密钥问题

- *问题**: LLM 调用失败

- *解决方案**:

```bash

# 检查环境变量

docker exec TradingAgents-web env | grep API_KEY

# 重新配置.env 文件

# 重启服务

docker-compose restart web

```bash

### 性能优化

```bash

# 1. 清理无用镜像

docker image prune

# 2. 清理无用容器

docker container prune

# 3. 清理无用数据卷

docker volume prune

# 4. 查看资源使用

docker stats

```bash

## 📊 监控和维护

### 健康检查

```bash

# 检查所有服务健康状态

docker-compose ps

# 检查特定服务日志

docker logs TradingAgents-web --tail 50

# 检查系统资源使用

docker stats --no-stream

```bash

### 定期维护

```bash

# 每周执行一次

# 1. 备份数据

docker exec TradingAgents-mongodb mongodump --out /backup/$(date +%Y%m%d)

# 2. 清理日志

docker-compose logs --tail 0 -f > /dev/null

# 3. 更新镜像

docker-compose pull
docker-compose up -d

```bash

## 🔮 高级配置

### 生产环境部署

```yaml

# docker-compose.prod.yml

version: '3.8'
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          memory: 2G
    restart: unless-stopped

```bash

### 安全配置

```bash

# 启用认证

MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=secure_password
REDIS_PASSWORD=secure_redis_password

```bash

- --

## 📞 获取帮助

如果在 Docker 部署过程中遇到问题：

- 🐛 [GitHub Issues](<https://github.com/hsliuping/TradingAgents-CN/issues)>
- 💬 [GitHub Discussions](<https://github.com/hsliuping/TradingAgents-CN/discussions)>
- 📚 [Docker 官方文档](<https://docs.docker.com/)>

- --

- 最后更新: 2025-07-13*
- 版本: cn-0.1.7*
- 贡献者: [@breeze303](<https://github.com/breeze303)*>
