# Google AI 配置指南

本指南将帮助您配置 Google AI (Gemini)模型，以便在 TradingAgents-CN 中使用 Google 的强大 AI 能力进行股票分析。

## 🎯 概述

TradingAgents-CN v0.1.2 新增了对 Google AI 的完整支持，包括：

- **Gemini 2.5 Pro**- 🚀 最新旗舰模型，推荐使用
- **Gemini 2.0 Flash**- 最新模型，推荐使用
- **Gemini 1.5 Pro**- 强大性能，适合深度分析
- **Gemini 1.5 Flash**- 快速响应，适合简单分析
- **智能混合嵌入**- Google AI 推理 + 阿里百炼嵌入

## 🔑 获取 Google AI API 密钥

### 1. 访问 Google AI Studio

1. 打开 [Google AI Studio](<https://aistudio.google.com/)>
2. 使用您的 Google 账号登录
3. 如果是首次使用，需要同意服务条款

### 2. 创建 API 密钥

1. 在左侧导航栏中点击**"API keys"**
2. 点击 **"Create API key"**按钮
3. 选择一个 Google Cloud 项目（或创建新项目）
4. 复制生成的 API 密钥

### 3. 配置 API 密钥

在项目根目录的 `.env` 文件中添加：

```env

# Google AI API 密钥

GOOGLE_API_KEY=your_google_api_key_here

```bash

## 🤖 支持的模型

### Gemini 2.5 系列 (🚀 最新推荐)

#### Gemini 2.5 Pro

- **模型名称**: `gemini-2.5-pro`
- **特点**: Google 最新旗舰模型，性能卓越
- **适用场景**: 复杂股票分析，重要投资决策
- **优势**:
  - 🧠 最强的推理能力
  - 🌍 优秀的中文理解
  - 🔧 完美的 LangChain 集成
  - 💾 支持超长上下文
  - 🎯 精准的金融分析

#### Gemini 2.5 Flash

- **模型名称**: `gemini-2.5-flash`
- **特点**: 最新快速模型，平衡了速度和性能
- **适用场景**: 实时市场分析、快速交易决策、日常投资咨询
- **优势**: 响应迅速，成本效益高

#### Gemini 2.5 Flash Lite

- **模型名称**: `gemini-2.5-flash-lite`
- **特点**: 轻量级快速模型，专注于效率
- **适用场景**: 简单查询、基础分析、高频次调用
- **优势**: 极低延迟，成本最优

#### Gemini 2.5 Pro-002

- **模型名称**: `gemini-2.5-pro-002`
- **特点**: Gemini 2.5 Pro 的优化版本
- **适用场景**: 需要最高精度的专业分析
- **优势**: 经过优化的性能表现

#### Gemini 2.5 Flash-002

- **模型名称**: `gemini-2.5-flash-002`
- **特点**: Gemini 2.5 Flash 的优化版本
- **适用场景**: 快速且准确的分析任务
- **优势**: 优化的速度和准确性平衡

### Gemini 2.0 系列

#### Gemini 2.0 Flash (推荐)

- **模型名称**: `gemini-2.0-flash`
- **特点**: 最新版本，性能优秀，LangChain 集成稳定
- **适用场景**: 日常股票分析，推荐首选
- **优势**:
  - 🧠 优秀的推理能力
  - 🌍 完美的中文支持
  - 🔧 稳定的 LangChain 集成
  - 💾 完整的内存学习功能

### Gemini 1.5 系列

#### Gemini 1.5 Pro

- **模型名称**: `gemini-1.5-pro`
- **特点**: 强大性能，适合复杂分析
- **适用场景**: 深度分析，重要投资决策
- **优势**: 功能强大，分析深度高

#### Gemini 1.5 Flash

- **模型名称**: `gemini-1.5-flash`
- **特点**: 快速响应，成本较低
- **适用场景**: 快速查询，批量分析
- **优势**: 响应速度快，适合高频使用

## 🔧 配置方法

### 1. Web 界面配置

1. **启动 Web 界面**:

   ```bash
   python -m streamlit run web/app.py
   ```

1. **在左侧边栏中**:
   - 选择 **"Google AI - Gemini 模型"**作为 LLM 提供商
   - 选择具体的 Gemini 模型
   - 启用记忆功能获得更好效果

3.**开始分析**:

   - 输入股票代码
   - 选择分析师
   - 点击"开始分析"

### 2. CLI 配置

```bash

# 使用 Gemini 2.0 Flash 模型

python -m cli.main --llm-provider google --model gemini-2.0-flash --stock AAPL

# 使用 Gemini 1.5 Pro 进行深度分析

python -m cli.main --llm-provider google --model gemini-1.5-pro --stock TSLA --analysts market fundamentals news

```bash

### 3. Python API 配置

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# 配置 Google AI

config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "google"
config["deep_think_llm"] = "gemini-2.0-flash"
config["quick_think_llm"] = "gemini-2.0-flash"
config["memory_enabled"] = True

# 创建分析图

graph = TradingAgentsGraph(["market", "fundamentals"], config=config)

# 执行分析

state, decision = graph.propagate("AAPL", "2025-06-27")

```bash

## 🔄 智能混合嵌入

TradingAgents-CN 的一个独特功能是智能混合嵌入服务：

### 工作原理

```bash
🧠 Google Gemini (主要推理)
    ↓
🔍 阿里百炼嵌入 (向量化和记忆)
    ↓
💾 ChromaDB (向量数据库)
    ↓
🎯 中文股票分析结果

```bash

### 优势

- **最佳性能**: Google AI 的强大推理能力
- **中文优化**: 阿里百炼的中文嵌入优势
- **成本控制**: 合理的 API 调用成本
- **稳定可靠**: 经过充分测试的集成方案

## 🧪 测试配置

### 1. 运行测试脚本

```bash

# 测试 Google AI 连接

python tests/test_gemini_correct.py

# 测试 Web 界面 Google 模型功能

python tests/test_web_interface.py

# 完整的 Gemini 功能测试

python tests/final_gemini_test.py

```bash

### 2. 验证配置

```bash

# 检查 API 密钥配置

python tests/test_all_apis.py

# 测试中文输出功能

python tests/test_chinese_output.py

```bash

## 💡 使用建议

### 模型选择建议

1. **重要决策**: 推荐 `gemini-2.5-pro` 🚀 或 `gemini-2.5-pro-002` 🔧
   - Google 最新旗舰模型
   - 最强推理和分析能力
   - 适合重要投资决策

1. **日常使用**: 推荐 `gemini-2.5-flash` ⚡ 或 `gemini-2.0-flash`
   - 性能优秀，成本合理
   - LangChain 集成稳定
   - 中文支持完美

1. **深度分析**: 使用 `gemini-1.5-pro`
   - 适合复杂分析任务
   - 分析深度更高
   - 推理能力强

1. **快速查询**: 使用 `gemini-2.5-flash-lite` 💡 或 `gemini-1.5-flash`
   - 响应速度快
   - 适合批量分析
   - 成本较低

1. **最新功能**: 推荐 `gemini-2.5-pro` 🚀 或 `gemini-2.5-flash` ⚡
   - 最新模型版本
   - 优化的性能表现
   - 最佳用户体验

### 最佳实践

1. **启用内存功能**: 让 AI 学习您的分析偏好
2. **合理选择分析师**: 根据需要选择相关的分析师
3. **设置适当的研究深度**: 平衡分析质量和时间成本
4. **定期检查 API 额度**: 确保有足够的 API 调用额度

## ⚠️ 注意事项

### API 限制

- Google AI 有 API 调用频率限制
- 建议合理控制分析频率
- 监控 API 使用量和成本

### 网络要求

- 需要稳定的网络连接
- 某些地区可能需要特殊网络配置
- 建议使用稳定的网络环境

### 数据安全

- API 密钥仅在本地使用
- 不会上传到任何服务器
- 建议定期更换 API 密钥

## 🔧 故障排除

### 常见问题

#### 1. API 密钥无效

```bash

# 检查 API 密钥格式

echo $GOOGLE_API_KEY

# 验证 API 密钥有效性

python tests/test_correct_apis.py

```bash

#### 2. 模型调用失败

- 检查网络连接
- 验证 API 额度是否充足
- 确认模型名称正确

#### 3. 中文输出异常

- 检查字符编码设置
- 验证模型配置
- 运行中文输出测试

### 获取帮助

如果遇到问题：

1. 📖 查看 [完整文档](../README.md)
2. 🧪 运行 [测试程序](../../tests/)
3. 💬 提交 [GitHub Issue](<https://github.com/hsliuping/TradingAgents-CN/issues)>

## 🎉 开始使用

现在您已经完成了 Google AI 的配置，可以开始享受 Gemini 模型的强大分析能力了！

```bash

# 启动 Web 界面

python -m streamlit run web/app.py

# 或使用 CLI

python -m cli.main --llm-provider google --model gemini-2.0-flash --stock AAPL

```bash
祝您投资分析愉快！🚀
