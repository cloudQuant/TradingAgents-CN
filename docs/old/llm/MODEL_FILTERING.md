# 模型列表智能过滤

## 📋 问题描述

从聚合平台（如 OpenRouter）获取模型列表时，会返回大量的模型（可能有几百个），包括：

- 各种小厂商的模型
- 实验性模型（preview、alpha、beta）
- 免费版本（free）
- 特殊版本（extended、nitro、online）
- Fine-tuned 模型

这些模型大多数用户不需要，导致：

1. ❌ 列表过长，难以管理
2. ❌ 包含很多不常用的模型
3. ❌ 影响用户体验

## ✅ 解决方案

实现**智能过滤**功能，只保留主流大厂的常用模型。

### 过滤规则

#### 1. 主流大厂白名单

只保留以下三大厂的模型：

- **OpenAI**(`openai`)
- **Anthropic**(`anthropic`)
- **Google** (`google`)

其他厂商的模型（Meta、Mistral AI、DeepSeek 等）需要手动添加。

#### 2. 排除带日期的旧版本

排除模型 ID 中包含日期的旧版本（如 `2024-05-13`），只保留最新版本。

- *示例**：
- ❌ `openai/gpt-4o-2024-05-13` - 带日期，排除
- ✅ `openai/gpt-4o` - 最新版，保留
- ❌ `anthropic/claude-3-5-sonnet-20241022` - 带日期，排除
- ✅ `anthropic/claude-3.5-sonnet` - 最新版，保留

#### 3. 排除关键词

排除包含以下关键词的模型：

- `preview` - 预览版
- `experimental` - 实验版
- `alpha` - Alpha 版
- `beta` - Beta 版
- `free` - 免费版
- `extended` - 扩展版
- `nitro` - Nitro 版
- `:free` - 免费标记
- `:extended` - 扩展标记
- `online` - 在线搜索版
- `instruct` - Instruct 版本

### 过滤逻辑

```python
def _filter_popular_models(self, models: list) -> list:
    """过滤模型列表，只保留主流大厂的常用模型"""
    import re

# 只保留三大厂
    popular_providers = ["openai", "anthropic", "google"]

# 日期格式正则表达式
    date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')

    filtered = []
    for model in models:
        model_id = model.get("id", "").lower()

# 1. 检查是否属于三大厂
        is_popular_provider = any(provider in model_id for provider in popular_providers)
        if not is_popular_provider:
            continue

# 2. 检查是否包含日期（排除带日期的旧版本）
        if date_pattern.search(model_id):
            continue

# 3. 检查是否包含排除关键词
        has_exclude_keyword = any(keyword in model_id for keyword in exclude_keywords)
        if has_exclude_keyword:
            continue

# 保留该模型
        filtered.append(model)

    return filtered

```bash

## 📊 过滤效果

### OpenRouter 示例

- *过滤前**：
- 总模型数：~300+ 个
- 包含各种小厂商、实验版本、免费版本、带日期的旧版本等

- *过滤后**：
- 保留模型数：~15-25 个
- 只包含 OpenAI、Anthropic、Google 三大厂的最新版本

### 保留的模型示例

```bash
✅ openai/gpt-4o
✅ openai/gpt-4o-mini
✅ openai/gpt-4-turbo
✅ openai/gpt-3.5-turbo
✅ anthropic/claude-3.5-sonnet
✅ anthropic/claude-4.5-sonnet (如果有)
✅ anthropic/claude-3-opus
✅ anthropic/claude-3-haiku
✅ google/gemini-2.0-flash
✅ google/gemini-1.5-pro
✅ google/gemini-1.5-flash

```bash

### 排除的模型示例

```bash
❌ openai/gpt-4o-2024-05-13 (带日期)
❌ openai/gpt-4o-2024-05-13:free (带日期 + 免费版)
❌ openai/gpt-4-turbo-preview (预览版)
❌ anthropic/claude-3-5-sonnet-20241022 (带日期)
❌ anthropic/claude-3-opus:beta (Beta 版)
❌ google/gemini-pro-experimental (实验版)
❌ meta-llama/llama-3.1-405b-instruct (其他厂商)
❌ mistralai/mistral-large (其他厂商)
❌ deepseek/deepseek-chat (其他厂商)
❌ openai/gpt-4o-mini-online (在线搜索版)

```bash

## 🔧 实现细节

### 后端实现

- *文件**：`app/services/config_service.py`

#### 1. 在 `_fetch_models_from_api` 中调用过滤

```python
if "data" in result and isinstance(result["data"], list):
    all_models = result["data"]
    print(f"📊 API 返回 {len(all_models)} 个模型")

# 过滤：只保留主流大厂的常用模型
    filtered_models = self._filter_popular_models(all_models)
    print(f"✅ 过滤后保留 {len(filtered_models)} 个常用模型")

    return {
        "success": True,
        "models": filtered_models,
        "message": f"成功获取 {len(filtered_models)} 个常用模型（已过滤）"
    }

```bash

#### 2. 实现 `_filter_popular_models` 方法

定义主流大厂、常用模型关键词、排除关键词，然后进行三重过滤。

## 🎯 优势

| 特性 | 过滤前 | 过滤后 |

|------|--------|--------|

| 模型数量 | ❌ 300+ 个 | ✅ 15-25 个 |

| 模型质量 | ⚠️ 参差不齐 | ✅ 三大厂最新版 |

| 管理难度 | ❌ 难以管理 | ✅ 易于管理 |

| 用户体验 | ❌ 选择困难 | ✅ 清晰明了 |

| 实用性 | ⚠️ 很多不常用 | ✅ 都是常用 |

| 版本 | ⚠️ 包含旧版本 | ✅ 只有最新版 |

## 📝 使用说明

### 自动过滤

从 API 获取模型列表时，系统会自动应用过滤规则，无需用户干预。

### 查看过滤结果

后端日志会显示过滤前后的模型数量：

```bash
📊 API 返回 312 个模型
✅ 过滤后保留 42 个常用模型

```bash
前端会显示过滤后的数量：

```bash
成功获取 42 个常用模型（已过滤）

```bash

### 自定义过滤规则

如果需要调整过滤规则，可以修改 `_filter_popular_models` 方法中的：

- `popular_providers` - 主流大厂列表
- `common_keywords` - 常用模型关键词
- `exclude_keywords` - 排除关键词

## 🔄 未来优化

### 1. 可配置的过滤规则

允许用户在前端配置过滤规则：

- 选择要包含的大厂
- 选择要包含的模型系列
- 自定义排除关键词

### 2. 分类展示

将模型按厂商分类展示：

- OpenAI 模型
- Anthropic 模型
- Google 模型
- 其他模型

### 3. 标签筛选

为模型添加标签，支持按标签筛选：

- 对话模型
- 代码模型
- 多模态模型
- 长上下文模型

## 📚 相关文档

- [聚合平台模型目录智能管理](AGGREGATOR_MODEL_CATALOG.md)
- [模型目录厂家选择优化](MODEL_CATALOG_PROVIDER_SELECT.md)
- [聚合渠道支持文档](AGGREGATOR_SUPPORT.md)

## 🎉 总结

通过智能过滤功能，用户可以：

- ✅ 快速获取主流大厂的常用模型
- ✅ 避免被大量不常用的模型干扰
- ✅ 提升模型目录管理效率
- ✅ 改善用户体验

- --

- *功能开发日期**：2025-10-12
- *开发人员**：AI Assistant
- *需求提出人**：用户
