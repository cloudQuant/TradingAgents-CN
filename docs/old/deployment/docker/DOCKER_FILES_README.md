# Docker 文件说明

> 📦 TradingAgents-CN v1.0.0-preview Docker 配置文件说明

## 📋 概述

TradingAgents-CN v1.0.0-preview 采用**前后端分离架构**，使用独立的 Docker 镜像分别构建和部署前端和后端服务。

- --

## 🐳 Docker 文件列表

### 核心文件（v1.0.0 使用）

| 文件 | 用途 | 说明 |

|------|------|------|

| **Dockerfile.backend**| 后端服务镜像 | FastAPI + Python 3.10 |

|**Dockerfile.frontend**| 前端服务镜像 | Vue 3 + Vite + Nginx |

|**docker-compose.v1.0.0.yml**| Docker Compose 配置 | 前后端分离部署 |

|**docker/nginx.conf**| Nginx 配置 | 前端静态文件服务 |

### 旧版文件（已废弃）

| 文件 | 说明 | 状态 |

|------|------|------|

|**Dockerfile.legacy**| 旧版 Streamlit Web 应用 | ❌ 已废弃，不适用于 v1.0.0 |

|**docker-compose.yml**| 旧版 Docker Compose | ⚠️ 可能不适用于 v1.0.0 |

|**docker-compose.split.yml**| 早期前后端分离配置 | ⚠️ 已被 docker-compose.v1.0.0.yml 替代 |

- --

## 🏗️ 架构说明

### v1.0.0-preview 前后端分离架构

```bash
┌─────────────────────────────────────────────────────────┐
│                    Docker Network                        │
│                 (tradingagents-network)                  │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Frontend   │  │   Backend    │  │   MongoDB    │  │
│  │   (Nginx)    │  │  (FastAPI)   │  │              │  │
│  │   Port: 5173 │  │  Port: 8000  │  │  Port: 27017 │  │
│  │              │  │              │  │              │  │
│  │  Vue 3 +     │  │  Python 3.10 │  │  Mongo 4.4   │  │
│  │  Vite        │  │  + Uvicorn   │  │              │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │    Redis     │  │Redis Commander│ │Mongo Express │  │
│  │              │  │  (可选)       │  │  (可选)      │  │
│  │  Port: 6379  │  │  Port: 8081  │  │  Port: 8082  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘

```bash

- --

## 📦 Dockerfile.backend

### 基础信息

- **基础镜像**: `python:3.10-slim`
- **工作目录**: `/app`
- **暴露端口**: `8000`
- **启动命令**: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### 包含内容

```bash
/app/
├── app/              # FastAPI 应用

├── tradingagents/    # 核心业务逻辑

├── config/           # 配置文件

├── logs/             # 日志目录（挂载）

└── data/             # 数据目录（挂载）

```bash

### 环境变量

- `PYTHONDONTWRITEBYTECODE=1`: 不生成.pyc 文件
- `PYTHONUNBUFFERED=1`: 实时输出日志
- `DOCKER_CONTAINER=true`: Docker 环境标识
- `TZ=Asia/Shanghai`: 时区设置

### 构建命令

```bash

# 构建后端镜像

docker build -f Dockerfile.backend -t tradingagents-backend:v1.0.0-preview .

# 运行后端容器

docker run -d \

  - -name tradingagents-backend \
  - p 8000:8000 \
  - v $(pwd)/logs:/app/logs \
  - v $(pwd)/config:/app/config \
  - -env-file .env \

  tradingagents-backend:v1.0.0-preview

```bash

- --

## 📦 Dockerfile.frontend

### 基础信息

- **构建镜像**: `node:22-alpine`（与项目开发环境一致）
- **运行镜像**: `nginx:alpine`
- **工作目录**: `/usr/share/nginx/html`
- **暴露端口**: `80`（映射到主机 5173）
- **包管理器**: `yarn 1.22.22`（必需）

### 多阶段构建

#### 阶段 1：构建（build）

```dockerfile
FROM node:22-alpine AS build

- 使用 yarn 安装依赖
- 使用 vite 构建生产版本
- 生成 dist 目录

```bash

#### 阶段 2：运行（runtime）

```dockerfile
FROM nginx:alpine AS runtime

- 复制构建产物（dist/）
- 配置 Nginx 支持 SPA 路由
- 提供静态文件服务

```bash

### 包含内容

```bash
/usr/share/nginx/html/
├── index.html
├── assets/
│   ├── *.js
│   ├── *.css
│   └── *.svg
└── ...

```bash

### Nginx 配置

- **SPA 路由支持**: `try_files $uri $uri/ /index.html`
- **静态资源缓存**: 7 天缓存
- **健康检查**: `/health` 端点

### 构建命令

```bash

# 构建前端镜像

docker build -f Dockerfile.frontend -t tradingagents-frontend:v1.0.0-preview .

# 运行前端容器

docker run -d \

  - -name tradingagents-frontend \
  - p 5173:80 \

  tradingagents-frontend:v1.0.0-preview

```bash

- --

## 🚀 使用 Docker Compose 部署

### 推荐方式：使用 docker-compose.v1.0.0.yml

```bash

# 1. 配置环境变量

cp .env.example .env

# 编辑.env 文件，配置 API 密钥

# 2. 启动所有服务

docker-compose -f docker-compose.v1.0.0.yml up -d

# 3. 查看服务状态

docker-compose -f docker-compose.v1.0.0.yml ps

# 4. 查看日志

docker-compose -f docker-compose.v1.0.0.yml logs -f

# 5. 停止服务

docker-compose -f docker-compose.v1.0.0.yml down

```bash

### 启动管理界面（可选）

```bash

# 启动 Redis Commander 和 Mongo Express

docker-compose -f docker-compose.v1.0.0.yml --profile management up -d

```bash

- --

## 🔧 常用命令

### 构建镜像

```bash

# 构建所有镜像

docker-compose -f docker-compose.v1.0.0.yml build

# 仅构建后端

docker-compose -f docker-compose.v1.0.0.yml build backend

# 仅构建前端

docker-compose -f docker-compose.v1.0.0.yml build frontend

# 强制重新构建（不使用缓存）

docker-compose -f docker-compose.v1.0.0.yml build --no-cache

```bash

### 管理容器

```bash

# 启动服务

docker-compose -f docker-compose.v1.0.0.yml up -d

# 停止服务

docker-compose -f docker-compose.v1.0.0.yml stop

# 重启服务

docker-compose -f docker-compose.v1.0.0.yml restart

# 删除容器（保留数据卷）

docker-compose -f docker-compose.v1.0.0.yml down

# 删除容器和数据卷

docker-compose -f docker-compose.v1.0.0.yml down -v

```bash

### 查看日志

```bash

# 查看所有服务日志

docker-compose -f docker-compose.v1.0.0.yml logs -f

# 查看后端日志

docker-compose -f docker-compose.v1.0.0.yml logs -f backend

# 查看前端日志

docker-compose -f docker-compose.v1.0.0.yml logs -f frontend

# 查看最近 100 行日志

docker-compose -f docker-compose.v1.0.0.yml logs --tail=100

```bash

### 进入容器

```bash

# 进入后端容器

docker exec -it tradingagents-backend bash

# 进入前端容器

docker exec -it tradingagents-frontend sh

# 进入 MongoDB 容器

docker exec -it tradingagents-mongodb mongo -u admin -p tradingagents123

```bash

- --

## 📊 镜像大小优化

### 当前镜像大小

| 镜像 | 大小（预估） | 说明 |

|------|-------------|------|

| **tradingagents-backend**| ~800MB | Python 3.10 + 依赖 |

|**tradingagents-frontend**| ~25MB | Nginx + 静态文件 |

|**总计**| ~825MB | 前后端镜像总和 |

### 优化建议

1.**使用多阶段构建**: ✅ 前端已使用

1. **使用 Alpine 镜像**: ✅ 前端已使用
2. **清理构建缓存**: ✅ 已实现
3. **使用.dockerignore**: ⚠️ 建议添加

- --

## 🐛 故障排除

### 问题 1：后端容器无法启动

- *症状**: 后端容器启动后立即退出

- *解决方案**:

```bash

# 查看详细日志

docker-compose -f docker-compose.v1.0.0.yml logs backend

# 检查环境变量

docker-compose -f docker-compose.v1.0.0.yml config

# 检查端口占用

netstat -ano | findstr :8000  # Windows

lsof -i :8000                 # macOS/Linux

```bash

### 问题 2：前端无法访问后端

- *症状**: 前端显示"网络错误"

- *解决方案**:

```bash

# 1. 检查后端健康状态

curl <http://localhost:8000/health>

# 2. 检查 CORS 配置

# 编辑 docker-compose.v1.0.0.yml

CORS_ORIGINS: "<http://localhost:5173,<http://localhost:8080>">

# 3. 重启后端

docker-compose -f docker-compose.v1.0.0.yml restart backend

```bash

### 问题 3：前端构建失败

- *症状**: 前端镜像构建时报错

- *解决方案**:

```bash

# 1. 检查 yarn.lock 是否存在

ls frontend/yarn.lock

# 2. 清理 node_modules 后重新构建

rm -rf frontend/node_modules
docker-compose -f docker-compose.v1.0.0.yml build --no-cache frontend

# 3. 检查 Node.js 版本

# Dockerfile.frontend 应使用 node:22-alpine

```bash

- --

## 📚 相关文档

- [Docker 部署指南](DOCKER_DEPLOYMENT_v1.0.0.md)
- [快速开始指南](QUICKSTART_v1.0.0.md)
- [环境准备指南](ENVIRONMENT_SETUP_v1.0.0.md)
- [Docker 安装指南](docs/v1.0.0-preview/10-installation/01-install-docker.md)

- --

## 🤝 获取帮助

如有问题，请联系：

- **GitHub Issues**: <https://github.com/hsliuping/TradingAgents-CN/issues>
- **QQ 群**: 782124367
- **邮箱**: hsliup@163.com

- --

- *更新日期**: 2025-10-15
- *适用版本**: TradingAgents-CN v1.0.0-preview
- *维护者**: TradingAgents-CN Team
