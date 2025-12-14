- --

version: cn-0.1.14-preview
last_updated: 2025-01-13
code_compatibility: cn-0.1.14-preview
status: updated

- --

# TradingAgents-CN 快速开始指南

> **版本说明**: 本文档基于 `cn-0.1.14-preview` 版本编写
> **最后更新**: 2025-01-13
> **状态**: ✅ 已更新 - 5 分钟快速上手指南

## 🚀 5 分钟快速上手

### 前提条件

- ✅ 已完成[安装配置](./installation-guide.md)
- ✅ 已配置至少一个 LLM API 密钥
- ✅ 虚拟环境已激活

### 1. 验证安装

```bash

# 运行安装验证脚本

python examples/test_installation.py

# 应该看到 "🎉 恭喜！安装验证全部通过！"

```bash

### 2. 启动应用

```bash

# 启动 Web 应用

python start_web.py

# 或直接使用 streamlit

cd web && streamlit run app.py

```bash

### 3. 访问界面

打开浏览器访问: <http://localhost:8501>

### 4. 首次配置

#### 选择 LLM 提供商

在左侧边栏选择你已配置的 LLM 提供商：

- **OpenAI**- GPT-4, GPT-3.5
- **阿里百炼**- 通义千问系列
- **DeepSeek**- DeepSeek Chat
- **百度千帆**- 文心一言系列
- **Google AI**- Gemini 系列

#### 选择模型

根据你的需求选择具体模型：

- **高性能**: GPT-4, 通义千问 Max, 文心一言 4.0
- **平衡**: GPT-3.5, 通义千问 Plus, 文心一言 3.5
- **经济**: DeepSeek Chat, 文心一言 Lite

### 5. 第一次分析

#### A 股分析示例

```bash
股票代码: 000001
分析日期: 2024-01-15

```bash

#### 美股分析示例

```bash
股票代码: AAPL
分析日期: 2024-01-15

```bash

#### 港股分析示例

```bash
股票代码: 00700
分析日期: 2024-01-15

```bash

## 📊 界面功能介绍

### 左侧边栏

- **LLM 配置**: 选择 AI 模型提供商和具体模型
- **分析参数**: 设置分析日期、股票代码
- **高级选项**: 配置分析深度、数据源等

### 主界面

- **股票输入**: 输入要分析的股票代码
- **分析结果**: 显示 AI 生成的分析报告
- **图表展示**: 股价走势、技术指标图表
- **成本统计**: 显示 API 调用成本

### 分析报告内容

- **基本面分析**: 财务指标、估值分析
- **技术面分析**: 技术指标、趋势分析
- **市场情绪**: 新闻分析、社交媒体情绪
- **投资建议**: 综合评分和操作建议

## 🎯 使用场景示例

### 场景 1: 日常股票分析

```bash
目标: 分析某只股票的投资价值
步骤:

1. 选择 GPT-4 模型 (高质量分析)
2. 输入股票代码: AAPL
3. 设置当前日期
4. 点击"开始分析"
5. 查看综合分析报告

```bash

### 场景 2: 批量股票筛选

```bash
目标: 从多只股票中筛选投资标的
步骤:

1. 选择经济型模型 (降低成本)
2. 逐个分析候选股票
3. 对比分析结果
4. 记录投资评分
5. 选择最优标的

```bash

### 场景 3: 技术分析验证

```bash
目标: 验证技术分析信号
步骤:

1. 选择专业技术分析模型
2. 输入技术信号股票
3. 查看 AI 技术分析结论
4. 对比自己的判断
5. 制定交易策略

```bash

## ⚙️ 常用配置

### 模型选择建议

#### 高质量分析 (成本较高)

- **OpenAI GPT-4**: 最佳分析质量
- **通义千问 Max**: 中文理解优秀
- **文心一言 4.0**: 本土化程度高

#### 平衡选择 (推荐)

- **GPT-3.5 Turbo**: 性价比最佳
- **通义千问 Plus**: 中文优化
- **DeepSeek Chat**: 经济实惠

#### 经济选择 (成本最低)

- **文心一言 Lite**: 基础分析
- **通义千问**: 简单查询
- **DeepSeek**: 预算有限

### 数据源配置

#### A 股数据源优先级

1. **Tushare**(推荐) - 数据最全面

2.**AKShare**- 免费备选
3.**通达信**- 实时数据

#### 美股数据源优先级

1.**Yahoo Finance**- 免费可靠
2.**FinnHub**- 专业数据
3.**Alpha Vantage** - 备用选择

## 🔧 高级功能

### 1. 自定义分析提示词

```python

# 在 config/prompts/目录下创建自定义提示词

# 例如: custom_analysis.txt

```bash

### 2. 批量分析脚本

```python

# 使用 Python 脚本进行批量分析

from tradingagents import TradingAgent

agent = TradingAgent()
stocks = ['AAPL', 'MSFT', 'GOOGL']
for stock in stocks:
    result = agent.analyze(stock)
    print(f"{stock}: {result.recommendation}")

```bash

### 3. 定时分析任务

```bash

# 使用 cron 设置定时任务 (Linux/macOS)

0 9 * * 1-5 cd /path/to/TradingAgents-CN && python scripts/daily_analysis.py

# 使用任务计划程序 (Windows)

# 创建每日 9 点执行的任务

```bash

## 📈 性能优化

### 1. 启用缓存

```bash

# 在.env 文件中启用 Redis 缓存

REDIS_ENABLED=true
REDIS_HOST=localhost
REDIS_PORT=6379

```bash

### 2. 并发设置

```python

# 在 config/settings.json 中调整

{
  "max_workers": 4,
  "request_timeout": 30
}

```bash

### 3. 数据缓存

```bash

# 设置数据缓存时间 (秒)

DATA_CACHE_TTL=3600

```bash

## 🚨 注意事项

### 1. API 成本控制

- 选择合适的模型平衡质量和成本
- 使用缓存避免重复请求
- 监控每日 API 使用量

### 2. 数据准确性

- 验证股票代码格式
- 注意交易日期和时区
- 关注数据源的更新频率

### 3. 投资风险

- AI 分析仅供参考，不构成投资建议
- 结合多种分析方法
- 控制投资风险

## 🆘 常见问题

### Q: 分析结果不准确怎么办？

A:

1. 检查股票代码是否正确
2. 确认分析日期是否为交易日
3. 尝试更换数据源或模型
4. 查看日志文件排查问题

### Q: API 调用失败怎么办？

A:

1. 检查网络连接
2. 验证 API 密钥有效性
3. 确认 API 额度是否充足
4. 查看错误日志详细信息

### Q: 如何降低使用成本？

A:

1. 选择经济型模型
2. 启用缓存功能
3. 避免重复分析
4. 设置使用限额

## 📚 进阶学习

完成快速开始后，建议继续学习：

1. **[配置管理指南](./config-management-guide.md)**- 深入配置

2.**[A 股分析指南](./a-share-analysis-guide.md)**- A 股专项
3.**[API 开发指南](../development/api-development-guide.md)**- 二次开发
4.**[故障排除指南](../troubleshooting/)** - 问题解决

- --

- *开始你的 AI 投资分析之旅！** 🚀
