# Google AI 依赖包更新

## 📦 更新内容

### 新增的依赖包

在 `pyproject.toml` 和 `requirements.txt` 中添加了以下 Google AI 相关包：

1. **`google-genai>=0.1.0`**- Google 新的统一 Gen AI SDK
   - 这是 Google 推荐的新 SDK，支持 Gemini 2.0、Veo、Imagen 等模型
   - 提供更好的性能和最新功能

2.**`google-generativeai>=0.8.0`**- Google Generative AI SDK (遗留)

   - 项目中现有代码使用的包
   - 虽然被标记为遗留，但仍需要保持兼容性

3.**`langchain-google-genai>=2.1.5`**- LangChain Google AI 集成

   - 已存在，用于 LangChain 框架集成
   - 项目主要使用的 Google AI 接口

## 🔧 技术细节

### 包的用途

- **`langchain-google-genai`**: 主要用于项目中的 LangChain 集成
- **`google.generativeai`**: 用于直接调用 Google AI API
- **`google.genai`**: 新的统一 SDK，为未来迁移做准备

### 依赖冲突解决

在安装过程中遇到了依赖版本冲突：

- `google-ai-generativelanguage` 版本不兼容
- 通过升级到最新版本解决

## 📋 验证结果

✅ 所有包导入成功
✅ 模型实例创建正常
✅ Web 应用运行正常
✅ 现有功能未受影响

## 🚀 使用建议

1. **当前项目**: 继续使用 `langchain-google-genai`
2. **新功能开发**: 可以考虑使用新的 `google-genai` SDK
3. **API 密钥**: 确保在 `.env` 文件中配置 `GOOGLE_API_KEY`

## 📝 安装命令

如果需要重新安装依赖：

```bash

# 使用 pip

pip install -e .

# 或使用 uv (推荐)

uv pip install -e .

```bash

## 🔗 相关文档

- [Google Gen AI SDK 文档](<https://cloud.google.com/vertex-ai/generative-ai/docs/sdks/overview)>
- [LangChain Google AI 集成](<https://python.langchain.com/docs/integrations/llms/google_ai)>
- [项目 Google 模型指南](./google_models_guide.md)

- --

- 更新时间: 2025-08-02*
- 更新内容: 添加 Google AI 相关依赖包*
