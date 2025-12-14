# 数据库依赖包安装指南

## 🎯 概述

本指南帮助您正确安装 TradingAgents 的数据库依赖包，解决 Python 3.10+环境下的兼容性问题。

## ⚠️ 重要提醒

- **Python 版本要求**: Python 3.10 或更高版本
- **已知问题**: `pickle5` 包在 Python 3.10+中会导致兼容性问题
- **推荐方式**: 使用更新后的 `requirements_db.txt`

## 🔧 快速检查

在安装前，运行兼容性检查工具：

```bash
python check_db_requirements.py

```bash
这个工具会：

- ✅ 检查 Python 版本是否符合要求
- ✅ 检查已安装的包版本
- ✅ 识别兼容性问题
- ✅ 提供具体的解决方案

## 📦 安装步骤

### 1. 检查 Python 版本

```bash
python --version

```bash
确保版本 ≥ 3.10.0

### 2. 创建虚拟环境（推荐）

```bash

# 创建虚拟环境

python -m venv venv

# 激活虚拟环境

# Windows:

venv\Scripts\activate

# Linux/Mac:

source venv/bin/activate

```bash

### 3. 升级 pip

```bash
python -m pip install --upgrade pip

```bash

### 4. 安装数据库依赖

```bash
pip install -r requirements_db.txt

```bash

## 🐛 常见问题解决

### 问题 1: pickle5 兼容性错误

- *错误信息**:

```bash
ImportError: cannot import name 'pickle5' from 'pickle'

```bash

- *解决方案**:

```bash

# 卸载 pickle5 包

pip uninstall pickle5

# Python 3.10+已内置 pickle 协议 5 支持，无需额外安装

```bash

### 问题 2: 版本冲突

- *错误信息**:

```bash
ERROR: pip's dependency resolver does not currently have a backtracking

```bash

- *解决方案**:

```bash

# 清理现有安装

pip uninstall pymongo motor redis hiredis pandas numpy

# 重新安装

pip install -r requirements_db.txt

```bash

### 问题 3: MongoDB 连接问题

- *错误信息**:

```bash
pymongo.errors.ServerSelectionTimeoutError

```bash

- *解决方案**:
1. 确保 MongoDB 服务正在运行
2. 检查连接字符串配置
3. 验证网络连接

### 问题 4: Redis 连接问题

- *错误信息**:

```bash
redis.exceptions.ConnectionError

```bash

- *解决方案**:
1. 确保 Redis 服务正在运行
2. 检查 Redis 配置
3. 验证端口和密码设置

## 📋 依赖包详情

| 包名 | 版本要求 | 用途 | 必需性 |

|------|----------|------|--------|

| pymongo | 4.3.0 - 4.x | MongoDB 驱动 | 必需 |

| motor | 3.1.0 - 3.x | 异步 MongoDB | 可选 |

| redis | 4.5.0 - 5.x | Redis 驱动 | 必需 |

| hiredis | 2.0.0 - 2.x | Redis 性能优化 | 可选 |

| pandas | 1.5.0 - 2.x | 数据处理 | 必需 |

| numpy | 1.21.0 - 1.x | 数值计算 | 必需 |

## 🔍 验证安装

运行以下命令验证安装：

```python

# 测试 MongoDB 连接

python -c "import pymongo; print('MongoDB 驱动安装成功')"

# 测试 Redis 连接

python -c "import redis; print('Redis 驱动安装成功')"

# 测试数据处理包

python -c "import pandas, numpy; print('数据处理包安装成功')"

# 测试 pickle 兼容性

python -c "import pickle; print(f'Pickle 协议版本: {pickle.HIGHEST_PROTOCOL}')"

```bash

## 🚀 Docker 方式（推荐）

如果遇到依赖问题，推荐使用 Docker：

```bash

# 构建 Docker 镜像

docker-compose build

# 启动服务

docker-compose up -d

```bash
Docker 方式会自动处理所有依赖关系。

## 📞 获取帮助

如果仍然遇到问题：

1. **运行诊断工具**: `python check_db_requirements.py`
2. **查看详细日志**: 启用详细模式安装 `pip install -v -r requirements_db.txt`
3. **提交 Issue**: 在 GitHub 仓库提交问题，包含：
   - Python 版本
   - 操作系统信息
   - 完整错误信息
   - 诊断工具输出

## 📝 更新日志

### v0.1.7

- ✅ 移除 pickle5 依赖，解决 Python 3.10+兼容性问题
- ✅ 更新包版本要求，提高稳定性
- ✅ 添加兼容性检查工具
- ✅ 完善安装指南和故障排除

### 历史版本

- v0.1.6: 初始数据库支持
- v0.1.5: 基础依赖包配置
