# 📈 升级指南: v0.1.12 → v0.1.13

## 🎯 升级概述

本指南将帮助您从 TradingAgents-CN v0.1.12 升级到 v0.1.13，享受原生 OpenAI 支持和 Google AI 全面集成的新功能。

## ⏰ 预计升级时间

- **简单升级**: 5-10 分钟 (仅更新代码和依赖)
- **完整配置**: 15-20 分钟 (包含 Google AI 配置和测试)
- **深度定制**: 30-45 分钟 (包含自定义端点配置)

## 📋 升级前检查

### 1. 环境要求

```bash

# 检查 Python 版本 (需要 >= 3.10)

python --version

# 检查当前版本

cat VERSION

# 应该显示: cn-0.1.12

```bash

### 2. 备份重要数据

```bash

# 备份配置文件

cp .env .env.backup
cp -r reports reports_backup

# 备份自定义配置 (如果有)

cp -r config config_backup

```bash

### 3. 检查当前分支

```bash
git branch

# 确认当前在合适的分支

```bash

## 🚀 升级步骤

### 步骤 1: 切换到预览版分支

```bash

# 切换到预览版分支

git checkout feature/native-openai-support

# 拉取最新代码

git pull origin feature/native-openai-support

# 确认版本

cat VERSION

# 应该显示: cn-0.1.13-preview

```bash

### 步骤 2: 更新依赖包

```bash

# 方法 1: 使用 requirements.txt

pip install -r requirements.txt

# 方法 2: 使用 pyproject.toml (推荐)

pip install -e .

# 验证 Google AI 相关包（统一 LangChain）

pip list | grep -E "(google-genai|langchain-google-genai)"

```bash

### 步骤 3: 配置 Google AI (可选但推荐)

```bash

# 在 .env 文件中添加 Google API 密钥

echo "GOOGLE_API_KEY=your_google_api_key_here" >> .env

# 如果没有 Google API 密钥，可以从以下地址获取:

# <https://makersuite.google.com/app/apikey>

```bash

### 步骤 4: 验证安装

```bash

# 测试 Google AI 包导入

python -c "
import langchain_google_genai
import google.genai
print('✅ Google AI packages imported successfully (LangChain unified)')
"

# 运行简单测试

python tests/test_gemini_simple.py

```bash

### 步骤 5: 启动和测试

```bash

# 启动 Web 界面

streamlit run web/app.py

# 在浏览器中访问 <http://localhost:8501>

# 测试新的模型选择功能

```bash

## 🔧 配置新功能

### 1. Google AI 配置

#### 获取 API 密钥

1. 访问 [Google AI Studio](<https://makersuite.google.com/app/apikey)>
2. 创建新的 API 密钥
3. 复制密钥到 `.env` 文件

#### 配置示例

```bash

# .env 文件

GOOGLE_API_KEY=AIzaSyC...your_key_here

```bash

#### 测试配置

```python

# 测试脚本

import os
from langchain_google_genai import ChatGoogleGenerativeAI

# 检查 API 密钥

api_key = os.getenv('GOOGLE_API_KEY')
if api_key:
    print("✅ Google API 密钥已配置")

# 测试模型
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key
    )
    print("✅ Google AI 模型创建成功")
else:
    print("⚠️ 请配置 GOOGLE_API_KEY 环境变量")

```bash

### 2. 原生 OpenAI 端点配置

#### 配置自定义端点

```bash

# .env 文件中添加

OPENAI_API_BASE=<https://your-custom-endpoint.com/v1>
OPENAI_API_KEY=your_custom_api_key

```bash

#### 支持的端点格式

- OpenAI 官方: `<https://api.openai.com/v1`>
- 自建服务: `<https://your-domain.com/v1`>
- 代理服务: `<https://proxy.example.com/v1`>

### 3. Web 界面新功能

#### 智能模型选择

- 🎯 自动检测可用模型
- 🔄 智能降级机制
- ⚡ 快速模型切换
- 🛡️ 错误恢复

#### 使用方法

1. 打开 Web 界面
2. 在侧边栏选择"Google AI"提供商
3. 选择具体的 Google AI 模型
4. 开始分析任务

## 🧪 功能测试

### 1. 基础功能测试

```bash

# 测试 CLI 功能

python cli/main.py --help

# 测试 Web 界面

streamlit run web/app.py

```bash

### 2. Google AI 功能测试

```bash

# 运行 Google AI 测试套件

python tests/test_gemini_simple.py
python tests/test_gemini_final.py
python tests/test_google_memory_fix.py

```bash

### 3. 集成测试

```bash

# 运行完整的股票分析测试

python tests/test_analysis.py

# 测试新闻分析功能

python tests/test_web_fix.py

```bash

## ⚠️ 常见问题和解决方案

### 问题 1: 依赖冲突

```bash

# 症状: pip 安装时出现依赖冲突

# 解决方案:

pip install --upgrade pip
pip install --force-reinstall -r requirements.txt

```bash

### 问题 2: Google AI 包导入失败

```bash

# 症状: 依赖冲突或旧 SDK 导入失败

# 解决方案（统一为 LangChain，移除旧 SDK）:

# 1) 移除 google-generativeai 依赖

# 2) 保留/安装 langchain-google-genai 与 google-genai

pip install langchain-google-genai>=2.1.5 google-genai>=0.1.0

```bash

### 问题 3: API 密钥配置问题

```bash

# 症状: Google API 密钥无效

# 解决方案:

# 1. 检查密钥格式 (应以 AIzaSy 开头)

# 2. 确认密钥权限

# 3. 检查 API 配额

```bash

### 问题 4: Web 界面模型选择错误

```bash

# 症状: KeyError in model selection

# 解决方案:

# 1. 清除浏览器缓存

# 2. 重启 Streamlit 应用

# 3. 检查模型配置文件

```bash

## 📊 升级验证清单

### ✅ 基础验证

- [ ] 版本号显示为 `cn-0.1.13-preview`
- [ ] 所有依赖包安装成功
- [ ] Web 界面正常启动
- [ ] CLI 功能正常工作

### ✅ Google AI 验证

- [ ] Google AI 包导入成功
- [ ] API 密钥配置正确
- [ ] 模型创建和调用成功
- [ ] Web 界面显示 Google AI 选项

### ✅ 功能验证

- [ ] 股票分析功能正常
- [ ] 新闻分析功能正常
- [ ] 模型切换功能正常
- [ ] 错误处理机制正常

### ✅ 性能验证

- [ ] 响应速度正常或更快
- [ ] 内存使用稳定
- [ ] 错误恢复正常
- [ ] 日志记录清晰

## 🔄 回滚方案

如果升级过程中遇到问题，可以回滚到 v0.1.12：

```bash

# 回滚到 v0.1.12

git checkout main  # 或之前的稳定分支

git pull origin main

# 恢复依赖

pip install -r requirements.txt

# 恢复配置文件

cp .env.backup .env
cp -r reports_backup reports

```bash

## 📞 获取帮助

### 🐛 问题报告

- **GitHub Issues**: 创建详细的问题报告
- **错误日志**: 提供完整的错误信息和日志
- **环境信息**: 包含 Python 版本、操作系统等信息

### 💡 功能建议

- **功能描述**: 详细描述期望的功能
- **使用场景**: 说明具体的使用需求
- **优先级**: 标明功能的重要性

### 📚 文档资源

- **配置指南**: `docs/configuration/google-ai-setup.md`
- **模型指南**: `docs/google_models_guide.md`
- **故障排除**: `docs/troubleshooting/`

## 🎉 升级完成

恭喜！您已成功升级到 TradingAgents-CN v0.1.13。

现在您可以：

- 🤖 使用原生 OpenAI 端点支持
- 🧠 体验 Google AI 模型的强大功能
- 🔧 享受优化的 LLM 适配器架构
- 🎨 使用改进的 Web 界面

感谢您选择 TradingAgents-CN，祝您使用愉快！
