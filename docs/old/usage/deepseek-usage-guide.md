# DeepSeek V3 使用指南

## 📋 概述

本指南详细介绍如何在 TradingAgents-CN 中使用 DeepSeek V3 进行股票投资分析。DeepSeek V3 是一个高性价比的大语言模型，特别适合中文金融分析场景。

## 🚀 快速开始

### 1. 环境准备

#### 获取 API 密钥

1. 访问 [DeepSeek 平台](<https://platform.deepseek.com/)>
2. 注册账号并完成认证
3. 进入控制台 → API Keys
4. 创建新的 API Key
5. 复制 API Key（格式：sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx）

#### 配置环境变量

```bash

# 编辑.env 文件

DEEPSEEK_API_KEY=sk-your_deepseek_api_key_here
DEEPSEEK_BASE_URL=<https://api.deepseek.com>
DEEPSEEK_ENABLED=true

```bash

### 2. 验证配置

```bash

# 测试 API 连接

python -c "
import os
from dotenv import load_dotenv
from tradingagents.llm_adapters.deepseek_adapter import ChatDeepSeek

load_dotenv()
llm = ChatDeepSeek(model='deepseek-chat')
response = llm.invoke('你好，请简单介绍 DeepSeek')
print('✅ DeepSeek 连接成功')
print('响应:', response.content[:100])
"

```bash

## 💰 成本优势

### 定价对比

| 模型 | 输入 Token | 输出 Token | 相对 GPT-4 成本 |

|------|-----------|-----------|---------------|

| **DeepSeek V3**| ¥0.001/1K | ¥0.002/1K |**节省 90%+** |

| GPT-4 | ¥0.03/1K | ¥0.06/1K | 基准 |

| GPT-3.5 | ¥0.0015/1K | ¥0.002/1K | 节省 75% |

### 成本计算示例

```python

# 典型股票分析的 Token 使用量

输入 Token: ~2,000 (股票数据 + 分析提示)
输出 Token: ~1,500 (分析报告)

# DeepSeek V3 成本

成本 = (2000 *0.001 + 1500*0.002) / 1000 = ¥0.005

# GPT-4 成本

成本 = (2000*0.03 + 1500* 0.06) / 1000 = ¥0.15

# 节省: 97%

```bash

## 📊 使用方式

### 1. Web 界面使用

#### 启动 Web 界面

```bash
streamlit run web/app.py

```bash

#### 操作步骤

1. **选择模型**：在左侧边栏选择"DeepSeek V3"
2. **配置参数**：
   - 模型：deepseek-chat
   - 温度：0.1（推荐，确保分析一致性）
   - 最大 Token：2000（适中长度）
1. **输入股票代码**：如 000001、600519、AAPL 等
2. **选择分析师**：建议选择"基本面分析师"
3. **开始分析**：点击"开始分析"按钮

#### 结果查看

- **决策摘要**：投资建议和关键指标
- **详细报告**：完整的基本面分析
- **Token 统计**：实时的使用量和成本
- **配置信息**：使用的模型和参数

### 2. CLI 界面使用

#### 启动 CLI

```bash
python -m cli.main

```bash

#### 交互流程

1. **选择 LLM 提供商**：选择"DeepSeek V3"
2. **选择模型**：选择"deepseek-chat"
3. **输入股票代码**：输入要分析的股票
4. **选择分析师**：选择需要的分析师类型
5. **查看结果**：等待分析完成并查看报告

### 3. Python API 使用

#### 基础使用

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# 配置 DeepSeek

config = DEFAULT_CONFIG.copy()
config.update({
    "llm_provider": "deepseek",
    "llm_model": "deepseek-chat",
    "quick_think_llm": "deepseek-chat",
    "deep_think_llm": "deepseek-chat",
    "backend_url": "<https://api.deepseek.com",>
})

# 创建分析图

ta = TradingAgentsGraph(
    selected_analysts=["fundamentals"],
    config=config
)

# 执行分析

result = ta.run_analysis("000001", "2025-01-08")
print(result)

```bash

#### 高级配置

```python
from tradingagents.llm_adapters.deepseek_adapter import ChatDeepSeek

# 创建自定义 DeepSeek 实例

llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.1,        # 降低随机性
    max_tokens=2000,        # 适中输出长度
    session_id="my_session" # 会话级别统计

)

# 直接调用

response = llm.invoke(
    "分析平安银行(000001)的投资价值",
    session_id="analysis_001",
    analysis_type="fundamentals"
)

```bash

## 📈 分析功能

### 1. 基本面分析

#### 支持的指标

- **估值指标**：PE、PB、PS、股息收益率
- **盈利能力**：ROE、ROA、毛利率、净利率
- **财务健康**：资产负债率、流动比率、速动比率
- **成长性**：营收增长率、利润增长率

#### 分析输出

```python

# 示例输出

{
    "investment_advice": "买入",
    "confidence": 0.75,
    "risk_score": 0.3,
    "fundamental_score": 7.5,
    "valuation_score": 8.0,
    "growth_score": 6.5,
    "key_metrics": {
        "PE": 5.2,
        "PB": 0.65,
        "ROE": 12.5,
        "debt_ratio": 0.15
    }
}

```bash

### 2. 多智能体协作

#### 支持的分析师

- **基本面分析师**：财务指标和投资价值分析
- **技术分析师**：技术指标和趋势分析
- **新闻分析师**：新闻事件影响分析
- **社交媒体分析师**：市场情绪分析

#### 协作流程

```python

# 多分析师协作

ta = TradingAgentsGraph(
    selected_analysts=["fundamentals", "market", "news"],
    config=config
)

# 获得综合分析结果

result = ta.run_analysis("AAPL", "2025-01-08")

```bash

## 🔧 高级配置

### 1. 性能优化

#### 推荐参数

```python

# 快速分析（成本优先）

config = {
    "temperature": 0.1,
    "max_tokens": 1000,
    "max_debate_rounds": 1
}

# 深度分析（质量优先）

config = {
    "temperature": 0.05,
    "max_tokens": 3000,
    "max_debate_rounds": 2
}

```bash

#### 缓存策略

```python

# 启用缓存减少重复调用

config["enable_cache"] = True
config["cache_ttl"] = 3600  # 1 小时缓存

```bash

### 2. Token 管理

#### 使用量监控

```python
from tradingagents.config.config_manager import config_manager

# 查看使用统计

stats = config_manager.get_usage_statistics(days=7)
print(f"7 天总成本: ¥{stats['total_cost']:.4f}")
print(f"DeepSeek 使用: {stats['provider_stats']['deepseek']}")

```bash

#### 成本控制

```python

# 设置成本警告

config_manager.update_settings({
    "cost_alert_threshold": 10.0,  # ¥10 警告阈值
    "enable_cost_tracking": True
})

```bash

## 🧪 测试和验证

### 1. 功能测试

#### 基础连接测试

```bash
python tests/test_deepseek_integration.py

```bash

#### 基本面分析测试

```bash
python tests/test_fundamentals_analysis.py

```bash

#### Token 统计测试

```bash
python tests/test_deepseek_token_tracking.py

```bash

### 2. 性能测试

#### 响应时间测试

```python
import time
start_time = time.time()
result = llm.invoke("简单分析 AAPL")
end_time = time.time()
print(f"响应时间: {end_time - start_time:.2f}秒")

```bash

#### 并发测试

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def concurrent_analysis():
    with ThreadPoolExecutor(max_workers=3) as executor:
        tasks = [
            executor.submit(ta.run_analysis, "000001", "2025-01-08"),
            executor.submit(ta.run_analysis, "600519", "2025-01-08"),
            executor.submit(ta.run_analysis, "AAPL", "2025-01-08")
        ]
        results = [task.result() for task in tasks]
    return results

```bash

## 🐛 故障排除

### 常见问题

#### 1. API 密钥错误

```bash
错误：Authentication failed
解决：检查 DEEPSEEK_API_KEY 是否正确配置

```bash

#### 2. 网络连接问题

```bash
错误：Connection timeout
解决：检查网络连接，确认能访问 api.deepseek.com

```bash

#### 3. Token 统计不准确

```bash
问题：显示¥0.0000
解决：检查 API 响应中的 usage 字段，启用调试模式

```bash

### 调试方法

#### 启用详细日志

```bash
export TRADINGAGENTS_LOG_LEVEL=DEBUG
python your_script.py

```bash

#### 检查 API 响应

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 查看详细的 API 调用信息

```bash

## 📚 最佳实践

### 1. 成本控制

- 使用缓存减少重复调用
- 设置合理的 max_tokens 限制
- 监控每日使用量和成本

### 2. 分析质量

- 使用较低的 temperature（0.1）确保一致性
- 选择合适的分析师组合
- 验证分析结果的合理性

### 3. 系统稳定性

- 配置错误重试机制
- 使用 fallback 模型
- 定期检查 API 密钥余额

- --

通过本指南，您应该能够充分利用 DeepSeek V3 的高性价比优势，进行专业的股票投资分析。如有问题，请参考故障排除部分或提交 GitHub Issue。
