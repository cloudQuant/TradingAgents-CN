# 调试日志增强 - 2025-10-11

## 📋 问题背景

用户报告：

- **1 级分析深度**：市场分析师正常调用统一工具 ✅
- **2 级分析深度**：市场分析师出错，可能调用了错误的工具 ❌

关键差异：

- 1 级深度：`quick_think_llm = qwen-turbo`, `deep_think_llm = qwen-plus`
- 2 级深度：`quick_think_llm = qwen-plus`, `deep_think_llm = qwen-plus`

## 🎯 目标

添加详细的日志来追踪：

1. 使用的 LLM 模型
2. 绑定的工具列表
3. LLM 返回的 tool_calls
4. 条件判断的决策过程

## 📝 添加的日志

### 1. 市场分析师 (`market_analyst.py`)

#### 工具选择阶段

```python
logger.info(f"📊 [市场分析师] 使用统一市场数据工具，自动识别股票类型")
logger.info(f"📊 [市场分析师] 配置: online_tools={toolkit.config['online_tools']}")
logger.info(f"📊 [市场分析师] 绑定的工具: {tool_names_debug}")
logger.info(f"📊 [市场分析师] 目标市场: {market_info['market_name']}")

```bash

#### LLM 调用阶段

```python
logger.info(f"📊 [市场分析师] LLM 类型: {llm.__class__.__name__}")
logger.info(f"📊 [市场分析师] LLM 模型: {getattr(llm, 'model_name', 'unknown')}")
logger.info(f"📊 [市场分析师] 消息历史数量: {len(state['messages'])}")
logger.info(f"📊 [市场分析师] 开始调用 LLM...")
logger.info(f"📊 [市场分析师] LLM 调用完成")

```bash

#### 结果检查阶段

```python
logger.info(f"📊 [市场分析师] 非 Google 模型 ({llm.__class__.__name__})，使用标准处理逻辑")
logger.info(f"📊 [市场分析师] 检查 LLM 返回结果...")
logger.info(f"📊 [市场分析师] - 是否有 tool_calls: {hasattr(result, 'tool_calls')}")
if hasattr(result, 'tool_calls'):
    logger.info(f"📊 [市场分析师] - tool_calls 数量: {len(result.tool_calls)}")
    if result.tool_calls:
        for i, tc in enumerate(result.tool_calls):
            logger.info(f"📊 [市场分析师] - tool_call[{i}]: {tc.get('name', 'unknown')}")

```bash

#### 分支处理阶段

```python

# 无工具调用

logger.info(f"📊 [市场分析师] ✅ 直接回复（无工具调用），长度: {len(report)}")

# 有工具调用

logger.info(f"📊 [市场分析师] 🔧 检测到工具调用: {[call.get('name', 'unknown') for call in result.tool_calls]}")

```bash

### 2. 基本面分析师 (`fundamentals_analyst.py`)

#### 工具选择阶段

```python
logger.info(f"📊 [基本面分析师] 使用统一基本面分析工具，自动识别股票类型")
logger.info(f"📊 [基本面分析师] 配置: online_tools={toolkit.config['online_tools']}")
logger.info(f"📊 [基本面分析师] 绑定的工具: {tool_names_debug}")
logger.info(f"📊 [基本面分析师] 目标市场: {market_info['market_name']}")

```bash

#### LLM 调用阶段

```python
logger.info(f"📊 [基本面分析师] LLM 类型: {fresh_llm.__class__.__name__}")
logger.info(f"📊 [基本面分析师] LLM 模型: {getattr(fresh_llm, 'model_name', 'unknown')}")
logger.info(f"📊 [基本面分析师] 消息历史数量: {len(state['messages'])}")
logger.info(f"📊 [基本面分析师] ✅ 工具绑定成功，绑定了 {len(tools)} 个工具")
logger.info(f"📊 [基本面分析师] 开始调用 LLM...")
logger.info(f"📊 [基本面分析师] LLM 调用完成")

```bash

#### 结果检查阶段

```python
logger.info(f"📊 [基本面分析师] - 是否有 tool_calls: {hasattr(result, 'tool_calls')}")
if hasattr(result, 'tool_calls'):
    logger.info(f"📊 [基本面分析师] - tool_calls 数量: {len(result.tool_calls)}")
    if result.tool_calls:
        for i, tc in enumerate(result.tool_calls):
            logger.info(f"📊 [基本面分析师] - tool_call[{i}]: {tc.get('name', 'unknown')}")

```bash

### 3. 条件判断逻辑 (`conditional_logic.py`)

#### 市场分析师条件判断

```python
logger.info(f"🔀 [条件判断] should_continue_market")
logger.info(f"🔀 [条件判断] - 消息数量: {len(messages)}")
logger.info(f"🔀 [条件判断] - 报告长度: {len(market_report)}")
logger.info(f"🔀 [条件判断] - 最后消息类型: {type(last_message).__name__}")
logger.info(f"🔀 [条件判断] - 是否有 tool_calls: {hasattr(last_message, 'tool_calls')}")
if hasattr(last_message, 'tool_calls'):
    logger.info(f"🔀 [条件判断] - tool_calls 数量: {len(last_message.tool_calls) if last_message.tool_calls else 0}")
    if last_message.tool_calls:
        for i, tc in enumerate(last_message.tool_calls):
            logger.info(f"🔀 [条件判断] - tool_call[{i}]: {tc.get('name', 'unknown')}")

# 决策结果

logger.info(f"🔀 [条件判断] ✅ 报告已完成，返回: Msg Clear Market")

# 或

logger.info(f"🔀 [条件判断] 🔧 检测到 tool_calls，返回: tools_market")

# 或

logger.info(f"🔀 [条件判断] ✅ 无 tool_calls，返回: Msg Clear Market")

```bash

#### 基本面分析师条件判断

```python
logger.info(f"🔀 [条件判断] should_continue_fundamentals")
logger.info(f"🔀 [条件判断] - 消息数量: {len(messages)}")
logger.info(f"🔀 [条件判断] - 报告长度: {len(fundamentals_report)}")
logger.info(f"🔀 [条件判断] - 最后消息类型: {type(last_message).__name__}")
logger.info(f"🔀 [条件判断] - 是否有 tool_calls: {hasattr(last_message, 'tool_calls')}")
if hasattr(last_message, 'tool_calls'):
    logger.info(f"🔀 [条件判断] - tool_calls 数量: {len(last_message.tool_calls) if last_message.tool_calls else 0}")

# 决策结果

logger.info(f"🔀 [条件判断] ✅ 报告已完成，返回: Msg Clear Fundamentals")

# 或

logger.info(f"🔀 [条件判断] 🔧 检测到 tool_calls，返回: tools_fundamentals")

# 或

logger.info(f"🔀 [条件判断] ✅ 无 tool_calls，返回: Msg Clear Fundamentals")

```bash

## 📊 日志分析指南

### 正常流程的日志模式

#### 市场分析师正常流程

```bash
📊 [市场分析师] 使用统一市场数据工具，自动识别股票类型
📊 [市场分析师] 配置: online_tools=True
📊 [市场分析师] 绑定的工具: ['get_stock_market_data_unified']
📊 [市场分析师] 目标市场: 中国 A 股
📊 [市场分析师] LLM 类型: ChatDashScopeOpenAI
📊 [市场分析师] LLM 模型: qwen-turbo  # 或 qwen-plus

📊 [市场分析师] 消息历史数量: 1
📊 [市场分析师] 开始调用 LLM...
📊 [市场分析师] LLM 调用完成
📊 [市场分析师] 非 Google 模型 (ChatDashScopeOpenAI)，使用标准处理逻辑
📊 [市场分析师] 检查 LLM 返回结果...
📊 [市场分析师] - 是否有 tool_calls: True
📊 [市场分析师] - tool_calls 数量: 1
📊 [市场分析师] - tool_call[0]: get_stock_market_data_unified  # ✅ 正确

📊 [市场分析师] 🔧 检测到工具调用: ['get_stock_market_data_unified']
🔀 [条件判断] should_continue_market
🔀 [条件判断] - 消息数量: 2
🔀 [条件判断] - 报告长度: 0
🔀 [条件判断] - 最后消息类型: AIMessage
🔀 [条件判断] - 是否有 tool_calls: True
🔀 [条件判断] - tool_calls 数量: 1
🔀 [条件判断] - tool_call[0]: get_stock_market_data_unified
🔀 [条件判断] 🔧 检测到 tool_calls，返回: tools_market

# 工具执行...

🔀 [条件判断] should_continue_market
🔀 [条件判断] - 消息数量: 4
🔀 [条件判断] - 报告长度: 1500  # ✅ 报告已生成

🔀 [条件判断] ✅ 报告已完成，返回: Msg Clear Market

```bash

### 异常流程的日志模式

#### 错误的工具调用

```bash
📊 [市场分析师] 绑定的工具: ['get_stock_market_data_unified']
📊 [市场分析师] LLM 模型: qwen-plus
📊 [市场分析师] - tool_call[0]: get_YFin_data  # ❌ 错误！调用了未绑定的工具

```bash

#### 死循环模式

```bash

# 第 1 次循环

📊 [市场分析师] 消息历史数量: 1
📊 [市场分析师] - tool_call[0]: get_stock_market_data_unified
🔀 [条件判断] - 报告长度: 0
🔀 [条件判断] 🔧 检测到 tool_calls，返回: tools_market

# 第 2 次循环

📊 [市场分析师] 消息历史数量: 3  # 增加了 2 条消息

📊 [市场分析师] - tool_call[0]: get_stock_market_data_unified  # ❌ 又调用了相同工具

🔀 [条件判断] - 报告长度: 0  # ❌ 报告仍然为空

🔀 [条件判断] 🔧 检测到 tool_calls，返回: tools_market

# 第 3 次循环

📊 [市场分析师] 消息历史数量: 5  # 继续增加

...

```bash

## 🔍 诊断步骤

### 步骤 1：确认配置

查找日志：

```bash
📊 [市场分析师] 配置: online_tools=True
📊 [市场分析师] 绑定的工具: ['get_stock_market_data_unified']

```bash

### 步骤 2：确认 LLM 模型

查找日志：

```bash
📊 [市场分析师] LLM 类型: ChatDashScopeOpenAI
📊 [市场分析师] LLM 模型: qwen-turbo  # 或 qwen-plus

```bash

### 步骤 3：检查工具调用

查找日志：

```bash
📊 [市场分析师] - tool_call[0]: get_stock_market_data_unified

```bash

- *如果工具名称不匹配绑定的工具，说明 LLM 调用了错误的工具！**

### 步骤 4：检查循环次数

统计日志中 `should_continue_market` 或 `should_continue_fundamentals` 出现的次数。

- *如果超过 3 次，说明进入了死循环！**

### 步骤 5：检查报告生成

查找日志：

```bash
🔀 [条件判断] - 报告长度: 1500

```bash

- *如果报告长度始终为 0，说明报告没有生成！**

## 📈 预期效果

通过这些日志，我们可以：

1. **快速定位问题**：
   - 是配置问题？
   - 是 LLM 模型问题？
   - 是工具调用问题？
   - 是条件判断问题？

1. **对比不同深度**：
   - 1 级深度使用 `qwen-turbo`
   - 2 级深度使用 `qwen-plus`
   - 对比两者的工具调用行为

1. **追踪死循环**：
   - 消息数量持续增加
   - 报告长度始终为 0
   - 重复调用相同工具

1. **验证修复效果**：
   - 修复后，日志应该显示正常流程
   - 报告长度应该 > 100
   - 循环次数应该 <= 2

## 🎯 下一步

1. **运行测试**：
   - 分别测试 1 级和 2 级深度
   - 收集完整日志

1. **对比分析**：
   - 对比两个深度的日志差异
   - 找出导致问题的关键差异

1. **实施修复**：
   - 根据日志分析结果
   - 实施针对性的修复方案

- --

- *创建日期**: 2025-10-11
- *创建人员**: AI Assistant
- *状态**: ✅ 已完成
