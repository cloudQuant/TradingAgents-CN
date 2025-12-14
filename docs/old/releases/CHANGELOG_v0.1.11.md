# TradingAgents-CN v0.1.11 更新日志

## 🚀 版本概述

- *发布日期**: 2025-01-27
- *版本号**: cn-0.1.11
- *主题**: 多 LLM 提供商集成与模型选择持久化

这是一个重大功能更新版本，全面集成了多个 LLM 提供商，实现了真正的模型选择持久化，并大幅优化了 Web 界面用户体验。

## ✨ 新功能

### 🤖 多 LLM 提供商集成

#### 支持的提供商

- **DashScope (阿里百炼)**
  - qwen-turbo: 快速响应
  - qwen-plus-latest: 平衡性能
  - qwen-max: 最强性能

- **DeepSeek V3**
  - deepseek-chat: 最新 V3 模型

- **Google AI**
  - gemini-2.0-flash: 推荐使用
  - gemini-1.5-pro: 强大性能
  - gemini-1.5-flash: 快速响应

- **OpenRouter (60+模型)**
  - **OpenAI 类别**: o4-mini-high, o3-pro, o1-pro, GPT-4o 等
  - **Anthropic 类别**: Claude 4 Opus, Claude 4 Sonnet, Claude 3.5 等
  - **Meta 类别**: Llama 4 Maverick, Llama 4 Scout, Llama 3.3 等
  - **Google 类别**: Gemini 2.5 Pro, Gemini 2.5 Flash 等
  - **自定义模型**: 支持任意 OpenRouter 模型 ID

#### 快速选择按钮

- 🧠 Claude 3.7 Sonnet - 最新对话模型
- 💎 Claude 4 Opus - 顶级性能模型
- 🤖 GPT-4o - OpenAI 旗舰模型
- 🦙 Llama 4 Scout - Meta 最新模型
- 🌟 Gemini 2.5 Pro - Google 多模态

### 💾 模型选择持久化

#### 技术实现

- **URL 参数存储**: 使用`st.query_params`实现真正的持久化
- **Session State 缓存**: 内存中快速访问配置
- **双重保险**: URL 参数 + Session State 结合
- **自动恢复**: 页面加载时自动恢复设置

#### 功能特点

- ✅ 支持浏览器刷新后配置保持
- ✅ 支持书签保存特定配置
- ✅ 支持 URL 分享模型配置
- ✅ 支持跨会话持久化
- ✅ 无需外部存储依赖

### 🎨 Web 界面优化

#### 侧边栏优化

- **320px 宽度**: 优化空间利用率
- **响应式设计**: 适配不同屏幕尺寸
- **清晰分类**: 模型按提供商和类别组织
- **详细描述**: 每个模型都有清晰的功能说明

#### 用户体验改进

- **一键选择**: 快速按钮提升操作效率
- **实时反馈**: 配置变化立即生效
- **错误处理**: 友好的错误提示和恢复机制
- **调试支持**: 详细的日志追踪配置变化

## 🔧 技术改进

### 新增模块

#### `web/utils/persistence.py`

```python
class ModelPersistence:
    """模型选择持久化管理器"""

    def save_config(self, provider, category, model):
        """保存配置到 session state 和 URL"""

    def load_config(self):
        """从 session state 或 URL 加载配置"""

    def clear_config(self):
        """清除配置"""

```bash

### 核心改进

#### 侧边栏组件 (`web/components/sidebar.py`)

- 集成持久化模块
- 支持 4 个 LLM 提供商
- 实现 60+模型选择
- 添加详细的调试日志
- 优化用户界面布局

#### 内存管理 (`tradingagents/agents/utils/memory.py`)

- 解决 ChromaDB 并发冲突
- 实现单例模式
- 改进错误处理机制

#### 分析运行器 (`web/utils/analysis_runner.py`)

- 增强错误处理
- 改进日志记录
- 优化性能表现

## 📊 支持统计

### 模型覆盖

- **4 个 LLM 提供商**
- **5 个 OpenRouter 类别**
- **60+个具体模型**
- **5 个快速选择按钮**
- **无限自定义模型**

### 功能覆盖

- ✅ 所有提供商支持持久化
- ✅ 所有模型选择支持持久化
- ✅ 快速按钮支持持久化
- ✅ 自定义模型支持持久化
- ✅ URL 参数完整支持

## 🧪 测试验证

### 基础测试场景

1. 选择 DashScope → qwen-max → 刷新 → 检查保持
2. 选择 DeepSeek → deepseek-chat → 刷新 → 检查保持
3. 选择 Google → gemini-2.0-flash → 刷新 → 检查保持

### OpenRouter 测试场景

1. 选择 OpenRouter → OpenAI → o4-mini-high → 刷新
2. 选择 OpenRouter → Anthropic → claude-opus-4 → 刷新
3. 选择 OpenRouter → Meta → llama-4-maverick → 刷新
4. 选择 OpenRouter → Google → gemini-2.5-pro → 刷新

### 自定义模型测试

1. 选择 OpenRouter → Custom → 输入模型 ID → 刷新
2. 选择 OpenRouter → Custom → 点击快速按钮 → 刷新
3. 检查 URL 参数是否包含正确配置

## 🔍 观察要点

### 成功标志

- 日志显示 `🔧 [Persistence] 恢复` 而不是 `初始化`
- URL 包含参数: `?provider=...&category=...&model=...`
- 刷新后选择完全保持
- 配置正确传递给分析系统

### 调试日志

- `🔧 [Persistence] 恢复 llm_provider: xxx`
- `🔄 [Persistence] 模型变更: xxx → yyy`
- `💾 [Persistence] 模型已保存: xxx`
- `🔄 [Persistence] 返回配置 - provider: xxx, model: yyy`

## 🚀 升级指南

### 从 v0.1.10 升级

1. **拉取最新代码**

   ```bash
   git pull origin main
   ```

1. **重新启动应用**

   ```bash
   streamlit run web/app.py
   ```

1. **验证功能**
   - 检查侧边栏是否显示新的 LLM 提供商选项
   - 测试模型选择是否在刷新后保持
   - 验证 URL 参数是否正确更新

### 配置要求

确保`.env`文件包含所需的 API 密钥：

```env

# DashScope (阿里百炼)

DASHSCOPE_API_KEY=your_dashscope_key

# DeepSeek

DEEPSEEK_API_KEY=your_deepseek_key

# Google AI

GOOGLE_API_KEY=your_google_key

# OpenRouter

OPENROUTER_API_KEY=your_openrouter_key

```bash

## 🎯 下一步计划

### v0.1.12 规划

- 更多 LLM 提供商集成 (Anthropic 直连、OpenAI 直连等)
- 模型性能对比和推荐系统
- 高级配置选项 (温度、最大 token 等)
- 模型使用统计和成本分析

### 长期规划

- 多模态模型支持 (图像、语音等)
- 模型微调和个性化
- 企业级部署方案
- 更多语言支持

## 🙏 致谢

感谢所有用户的反馈和建议，特别是对模型选择持久化功能的需求。这个版本的改进直接来源于用户的真实使用体验。

- --

- *完整更新内容**: 8 个文件修改，763 行新增，408 行删除
- *核心新增**: `web/utils/persistence.py` 持久化模块
- *主要优化**: 侧边栏组件、内存管理、分析运行器
