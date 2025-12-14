# DeepSeek 集成说明

本文档记录了 DeepSeek V3 模型的集成过程和技术细节。

## 🎯 集成目标

- 支持 DeepSeek V3 高性价比大语言模型
- 提供完整的 Token 使用统计
- 确保与现有系统的兼容性
- 优化中文输出质量

## 🔧 技术实现

### 1. DeepSeek 适配器

- **文件**: `tradingagents/llm_adapters/deepseek_adapter.py`
- **功能**: 支持 Token 统计的 DeepSeek 聊天模型
- **特性**: 继承 ChatOpenAI，添加使用量跟踪

### 2. Token 统计功能

- 自动提取 API 响应中的 token 使用量
- 智能估算 fallback 机制
- 集成到 TokenTracker 系统
- 支持会话级别成本跟踪

### 3. 系统集成

- **TradingGraph**: 自动使用 DeepSeek 适配器
- **配置管理**: 支持 DeepSeek 相关配置
- **成本跟踪**: 完整的使用成本统计

## 📊 性能特点

### 成本优势

- **输入 Token**: ¥0.001/1K tokens
- **输出 Token**: ¥0.002/1K tokens
- **性价比**: 相比 GPT-4 显著降低成本

### 质量表现

- **中文理解**: 优秀的中文语言理解能力
- **专业分析**: 适合金融分析任务
- **推理能力**: 强大的逻辑推理能力

## 🚀 使用方法

### 配置设置

```bash

# .env 文件配置

DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=<https://api.deepseek.com>

```bash

### 代码使用

```python
from tradingagents.llm_adapters.deepseek_adapter import ChatDeepSeek

# 创建 DeepSeek 实例

llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.1,
    max_tokens=2000
)

# 调用模型

response = llm.invoke("分析一下股票市场")

```bash

## 📈 集成效果

### 功能验证

- ✅ Token 使用统计正常
- ✅ 成本计算准确
- ✅ 中文输出优质
- ✅ 系统集成稳定

### 用户体验

- 显著降低使用成本
- 保持分析质量
- 提供透明的成本统计
- 支持高并发使用

- --

更多技术细节请参考相关代码和测试文件。
