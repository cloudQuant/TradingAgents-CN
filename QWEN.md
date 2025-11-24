# TradingAgents-CN 项目上下文

## 项目概述

TradingAgents-CN 是一个基于多智能体大语言模型的**中文金融交易决策框架**，专为中文用户优化，提供完整的A股/港股/美股分析能力。该项目基于原版 [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) 进行中文增强和功能扩展。

### 核心特性

- **多智能体架构**：包含市场分析师、基本面分析师、新闻分析师、社交媒体分析师等
- **多LLM提供商支持**：支持 OpenAI、Google AI、Anthropic、DeepSeek、DashScope(阿里百炼)、千帆(文心一言)等
- **完整A股支持**：集成 Tushare、AkShare、BaoStock 等中国数据源
- **现代化架构**：v1.0.0-preview 版本采用 FastAPI + Vue 3 的前后端分离架构
- **企业级功能**：用户权限管理、配置中心、缓存管理、实时通知、批量分析等
- **报告导出**：支持 Markdown/Word/PDF 多格式专业报告导出
- **容器化部署**：完整 Docker 支持，支持 amd64 + arm64 多架构

## 技术栈

### 后端技术
- **框架**：FastAPI (替代 v0.1.x 的 Streamlit)
- **数据库**：MongoDB + Redis (双数据库架构)
- **异步处理**：使用 asyncio、uvicorn
- **AI/LLM**：langchain、langgraph、openai、anthropic、google-genai 等
- **数据处理**：pandas、numpy、yfinance、akshare、tushare 等

### 前端技术
- **框架**：Vue 3 + Vite + Element Plus
- **构建工具**：Yarn
- **样式**：CSS3、现代化UI组件库

### 部署技术
- **容器化**：Docker + Docker Compose
- **反向代理**：Nginx
- **缓存**：Redis (支持 Redis Commander 管理界面)
- **数据库管理**：MongoDB (支持 Mongo Express 管理界面)

## 项目结构

```
F:\source_code\TradingAgents-CN\
├── app/                    # FastAPI 后端应用 (专有组件)
├── frontend/               # Vue 3 前端应用 (专有组件)
├── tradingagents/          # 核心多智能体框架
│   ├── agents/             # 各种分析师智能体
│   ├── api/                # API 接口 (旧版)
│   ├── config/             # 配置管理
│   ├── graph/              # 核心图执行引擎 (LangGraph)
│   ├── llm_adapters/       # LLM 适配器
│   ├── models/             # 数据模型
│   ├── tools/              # 数据获取工具
│   └── utils/              # 通用工具函数
├── config/                 # 配置文件
├── data/                   # 数据目录
├── docker/                 # Docker 相关配置
├── docs/                   # 文档
├── tests/                  # 测试文件
├── scripts/                # 脚本文件
├── logs/                   # 日志目录
├── results/                # 结果输出目录
├── eval_results/           # 评估结果目录
└── main.py                 # 项目入口文件 (旧版 CLI)
```

## 架构演进

| 版本 | 前端 | 后端 | 数据库 | 部署方式 |
|------|------|------|--------|----------|
| v0.1.x | Streamlit | Streamlit | 可选 MongoDB | 本地/Docker |
| v1.0.0-preview | Vue 3 + Element Plus | FastAPI + Uvicorn | MongoDB + Redis | Docker 多架构 + GitHub Actions |

## 核心功能模块

### 1. 多智能体系统 (tradingagents.graph)
- **TradingAgentsGraph**: 主类，协调整个交易代理框架
- **LangGraph**: 基于 LangGraph 的图执行引擎
- 支持多种分析师角色：市场、基本面、新闻、社交媒体
- 支持投资辩论和风险管理辩论

### 2. LLM 适配器系统 (tradingagents.llm_adapters)
- 支持多种 LLM 提供商和自定义端点
- 统一的 LLM 创建接口
- 支持 Google、OpenAI、Anthropic、DashScope、DeepSeek、千帆等

### 3. 数据工具 (tradingagents.tools)
- 统一数据获取接口
- 多种数据源：yfinance、akshare、tushare、baostock
- 在线/离线工具切换

### 4. 内存系统 (tradingagents.agents.utils.memory)
- 金融情境记忆系统
- 支持牛市/熊市/交易员/投资判断/风险管理等专用内存

## 构建和运行

### 开发环境启动
```bash
# 1. 安装依赖
pip install -e .

# 2. 设置环境变量
cp .env.example .env
# 编辑 .env 文件，配置 API 密钥

# 3. 启动后端 (FastAPI)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 4. 启动前端 (Vue)
cd frontend
yarn install
yarn dev
```

### Docker 部署
```bash
# 1. 构建和启动完整栈
docker compose up -d

# 2. 构建特定服务
docker compose up --build backend
docker compose up --build frontend

# 3. 查看服务状态
docker compose ps
docker compose logs -f backend
```

### 本地快速测试
```bash
# 运行简单的股票分析
python main.py
```

## 配置说明

### 主要配置项 (tradingagents.default_config.py)
- `llm_provider`: LLM 提供商 (openai, google, dashscope, deepseek 等)
- `deep_think_llm` / `quick_think_llm`: 深度/快速思考模型
- `max_debate_rounds` / `max_risk_discuss_rounds`: 辩论轮次
- `online_tools`: 是否启用在线工具
- `data_dir`: 数据目录

### 环境变量
- API 密钥: `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `DASHSCOPE_API_KEY` 等
- 数据库连接: `TRADINGAGENTS_MONGODB_URL`, `TRADINGAGENTS_REDIS_URL`
- 日志配置: `TRADINGAGENTS_LOG_LEVEL`

## 开发约定

### 代码风格
- 遵循 Python PEP 8 标准
- 使用类型提示 (typing)
- 详细日志记录 (loguru)
- 配置使用 pydantic-settings

### 测试
- 使用 pytest 进行单元测试
- 配置文件: pytest.ini
- 测试目录: tests/

### 文档
- 中文文档优先
- 详细的 README.md 和使用指南
- 微信公众号: TradingAgents-CN

## 关键文件

- `tradingagents/graph/trading_graph.py`: 核心多智能体图执行引擎
- `tradingagents/default_config.py`: 默认配置
- `pyproject.toml`: 依赖管理和构建配置
- `docker-compose.yml`: Docker Compose 部署配置
- `app/main.py`: FastAPI 后端入口 (v1.0.0-preview)
- `frontend/src/App.vue`: Vue 3 前端主组件

## 许可证信息

该项目采用**混合许可证**模式:
- **开源部分** (Apache 2.0): 除 `app/` 和 `frontend/` 外的所有文件
- **专有部分**: `app/` (FastAPI后端) 和 `frontend/` (Vue前端) 目录需要商业授权

## 版本信息

- **当前版本**: v1.0.0-preview
- **项目状态**: 预览版，前后端分离架构重构完成

## 风险提示

**重要声明**: 本框架仅用于研究和教育目的，不构成投资建议。AI模型的预测存在不确定性，投资有风险，决策需谨慎。