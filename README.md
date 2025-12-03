# TradingAgents 中文增强版

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/Version-cn--0.1.15-green.svg)](./VERSION)
[![Documentation](https://img.shields.io/badge/docs-中文文档-green.svg)](./docs/)
[![Original](https://img.shields.io/badge/基于-TauricResearch/TradingAgents-orange.svg)](https://github.com/TauricResearch/TradingAgents)

>
> 🎯 **核心功能**: 原生OpenAI支持 | Google AI全面集成 | 自定义端点配置 | 智能模型选择 | 多LLM提供商支持 | 模型选择持久化 | Docker容器化部署 | 专业报告导出 | 完整A股支持 | 中文本地化

基于多智能体大语言模型的**中文金融交易决策框架**。专为中文用户优化，提供完整的A股/港股/美股分析能力。

## 🙏 致敬源项目

感谢 [Tauric Research](https://github.com/TauricResearch) 团队创造的革命性多智能体交易框架 [TradingAgents](https://github.com/TauricResearch/TradingAgents)！

**🎯 我们的使命**: 为中国用户提供完整的中文化体验，支持A股/港股市场，集成国产大模型，推动AI金融技术在中文社区的普及应用。

## 🎉 v1.0.0-preview 版本上线 - 全新架构升级

> 🚀 **重磅发布**: v1.0.0-preview 版本现已正式！全新的 FastAPI + Vue 3 架构，带来企业级的性能和体验！

### ✨ 核心特性

#### 🏗️ **全新技术架构**
- **后端升级**: 从 Streamlit 迁移到 FastAPI，提供更强大的 RESTful API
- **前端重构**: 采用 Vue 3 + Element Plus，打造现代化的单页应用
- **数据库优化**: MongoDB + Redis 双数据库架构，性能提升 10 倍
- **容器化部署**: 完整的 Docker 多架构支持（amd64 + arm64）

#### 🎯 **企业级功能**
- **用户权限管理**: 完整的用户认证、角色管理、操作日志系统
- **配置管理中心**: 可视化的大模型配置、数据源管理、系统设置
- **缓存管理系统**: 智能缓存策略，支持 MongoDB/Redis/文件多级缓存
- **实时通知系统**: SSE+WebSocket 双通道推送，实时跟踪分析进度和系统状态
- **批量分析功能**: 支持多只股票同时分析，提升工作效率
- **智能股票筛选**: 基于多维度指标的股票筛选和排序系统
- **自选股管理**: 个人自选股收藏、分组管理和跟踪功能
- **个股详情页**: 完整的个股信息展示和历史分析记录
- **模拟交易系统**: 虚拟交易环境，验证投资策略效果

#### 🤖 **智能分析增强**
- **动态供应商管理**: 支持动态添加和配置 LLM 供应商
- **模型能力管理**: 智能模型选择，根据任务自动匹配最佳模型
- **多数据源同步**: 统一的数据源管理，支持 Tushare、AkShare、BaoStock
- **报告导出功能**: 支持 Markdown/Word/PDF 多格式专业报告导出

#### � **重大Bug修复**
- **技术指标计算修复**: 彻底解决市场分析师技术指标计算不准确问题
- **基本面数据修复**: 修复基本面分析师PE、PB等关键财务数据计算错误
- **死循环问题修复**: 解决部分用户在分析过程中触发的无限循环问题
- **数据一致性优化**: 确保所有分析师使用统一、准确的数据源

#### �🐳 **Docker 多架构支持**
- **跨平台部署**: 支持 x86_64 和 ARM64 架构（Apple Silicon、树莓派、AWS Graviton）
- **GitHub Actions**: 自动化构建和发布 Docker 镜像
- **一键部署**: 完整的 Docker Compose 配置，5 分钟快速启动

### 📊 技术栈升级

| 组件 | v0.1.x | v1.0.0-preview |
|------|--------|----------------|
| **后端框架** | Streamlit | FastAPI + Uvicorn |
| **前端框架** | Streamlit | Vue 3 + Vite + Element Plus |
| **数据库** | 可选 MongoDB | MongoDB + Redis |
| **API 架构** | 单体应用 | RESTful API + WebSocket |
| **部署方式** | 本地/Docker | Docker 多架构 + GitHub Actions |



#### 📥 安装部署

**三种部署方式，任选其一**：

| 部署方式 | 适用场景 | 难度 | 文档链接 |
|---------|---------|------|---------|
| 🟢 **绿色版** | Windows 用户、快速体验 | ⭐ 简单 | [绿色版安装指南](https://mp.weixin.qq.com/s/uAk4RevdJHMuMvlqpdGUEw) |
| 🐳 **Docker版** | 生产环境、跨平台 | ⭐⭐ 中等 | [Docker 部署指南](https://mp.weixin.qq.com/s/JkA0cOu8xJnoY_3LC5oXNw) |
| 💻 **本地代码版** | 开发者、定制需求 | ⭐⭐⭐ 较难 | [本地安装指南](https://mp.weixin.qq.com/s/cqUGf-sAzcBV19gdI4sYfA) |

⚠️ **重要提醒**：在分析股票之前，请按相关文档要求，将股票数据同步完成，否则分析结果将会出现数据错误。



#### 📚 使用指南

在使用前，建议先阅读详细的使用指南：

- **[1、📘 TradingAgents-CN v1.0.0-preview 使用指南](https://mp.weixin.qq.com/s/ppsYiBncynxlsfKFG8uEbw)**
- **[2、📘 使用 Docker Compose 部署TradingAgents-CN v1.0.0-preview（完全版）](https://mp.weixin.qq.com/s/JkA0cOu8xJnoY_3LC5oXNw)**
- **[3、📘 从 Docker Hub 更新 TradingAgents‑CN 镜像](https://mp.weixin.qq.com/s/WKYhW8J80Watpg8K6E_dSQ)**
- **[4、📘 TradingAgents-CN v1.0.0-preview绿色版（目前只支持windows）简单使用手册](https://mp.weixin.qq.com/s/uAk4RevdJHMuMvlqpdGUEw)**
- **[5、📘 TradingAgents-CN v1.0.0-preview绿色版端口配置说明](https://mp.weixin.qq.com/s/o5QdNuh2-iKkIHzJXCj7vQ)**
- **[6、📘 TradingAgents v1.0.0-preview 源码版安装手册（修订版）](https://mp.weixin.qq.com/s/cqUGf-sAzcBV19gdI4sYfA)**
- **[7、📘 TradingAgents v1.0.0-preview 源码安装视频教程](https://www.bilibili.com/video/BV1FxCtBHEte/?vd_source=5d790a5b8d2f46d2c10fd4e770be1594)**


使用指南包含：
- ✅ 完整的功能介绍和操作演示
- ✅ 详细的配置说明和最佳实践
- ✅ 常见问题解答和故障排除
- ✅ 实际使用案例和效果展示

### 🔄 数据同步功能使用指南

#### 1. 启用与前提条件

- **后端版本要求**：需要使用包含 `app/routers/sync.py` 的版本，并确保后端已正确加载该路由（`app.include_router(sync_router.router)`）。
- **端口与网络**：本地与远程节点之间必须能通过 HTTP 访问 `/api/sync/*` 接口（通常是 `http://IP:PORT/api/sync/...`），而 **不需要直接暴露 MongoDB 端口**。
- **认证与安全**：生产环境推荐在反向代理层（Nginx 等）使用 HTTPS，并在节点中为远程地址配置 API Key（后续版本会增强认证校验）。

#### 2. 同步节点管理（Sync Nodes）

- **入口路径**：前端顶部菜单 → `设置 → 数据同步 → 同步节点`，或直接访问 `/#/sync/nodes`。
- **使用步骤**：
  1. 点击右上角 **「添加节点」**，配置：
     - **节点ID**：用于标识节点（如 `server_main`、`home_pc`），可留空自动生成。
     - **名称**：展示用名称（如「主服务器」「家里电脑」）。
     - **地址(URL)**：远程 TradingAgents‑CN WebAPI 地址，例如：`http://192.168.1.10:8000` 或 `https://your-server.com`，**不需要带 `/api` 前缀**。
     - **API Key**：可选，用于后续扩展认证。
     - **状态**：启用/禁用（只在启用状态的节点会出现在同步对话框的下拉列表中）。
  2. 保存后，在列表中点击 **「测试连接」**，确认网络连通性与后端版本正常（后端会调用 `/api/sync/ping`）。

#### 3. 集合级别远程同步（Remote Sync）

- **入口路径**：
  - 股票集合：`股票 → 数据集合 → 选择某个集合`；
  - 债券/基金/期货/外汇集合：对应菜单下的「数据集合」详情页；
  - 页面顶部都包含统一的集合头部组件 `更新数据` 按钮。
- **打开方式**：
  1. 在集合详情页顶部点击 **「更新数据」按钮 → 选择「远程同步」**。
  2. 将弹出「远程同步」对话框，默认展示 **「节点同步」** 模式，底部还有保留的 **「直连同步」** 旧模式。

#### 4. 节点同步模式：Pull / Push / Sync

在 `RemoteSyncDialog` 的「节点同步」页签中，可以通过三个选项控制同步方向：

- **从远程拉取（Pull）**：
  - 方向：远程节点 ➜ 本地节点。
  - 适用场景：本地刚部署完成，需要从服务器拉一份已有数据；或长期以服务器为权威数据源的场景。
  - 操作步骤：
    1. 在「同步方向」选择 **「从远程拉取（Pull）」**。
    2. 在「源节点」下拉中选择事先配置好的远程节点（例如 `server_main`）。
    3. 选择同步策略：
       - **增量同步**：只同步比本地更新的数据（推荐日常使用）。
       - **全量同步**：清空本地后再全部拉取（适合初始化或重建数据）。
    4. 点击 **「开始从远程拉取（Pull）」**，在对话框中可实时查看任务进度。

- **推送到远程（Push）**：
  - 方向：本地节点 ➜ 远程节点。
  - 适用场景：本地整理/修正数据后，需要覆盖或更新远程服务器上的数据。
  - 操作步骤类似 Pull，只是：
    - 在「同步方向」选择 **「推送到远程（Push）」**；
    - 在「目标节点」选择要推送的节点；
    - 点击 **「开始推送到远程（Push）」**。

- **双向同步（Sync）**：
  - 方向：本地 ↔ 远程（前端会连续发起一次 Pull 和一次 Push）。
  - 适用场景：希望本地与远程都尽量保持一致，而不特别强调哪一端是“权威源”。
  - 当前实现策略（简单版）：
    - 先执行一次 **拉取（Pull）**，把远程较新的数据拉到本地；
    - 再执行一次 **推送（Push）**，把本地合并后的数据推回远程；
    - 前端会以最后一个任务（Push）的进度作为跟踪主任务，所有任务明细可在“同步任务”页面查看。
  - 操作步骤：
    1. 在「同步方向」选择 **「双向同步（Sync）」**；
    2. 选择对应节点与同步策略；
    3. 点击 **「开始双向同步（Sync）」**。

> 💡 **最佳实践**：  
> - 初次上线或重建数据时，建议先在目标端做备份，然后使用 **全量 Pull 或全量 Push**。  
> - 日常运行使用 **增量 Pull / Push** 或 **双向 Sync**，避免频繁全量重写导致长时间锁表或占用大量带宽。

#### 5. 查看同步任务与历史

- **入口路径**：顶部菜单 → `设置 → 数据同步 → 同步任务`，或直接访问 `/#/sync/tasks`。
- 在该页面可以：
  - 查看最近的同步任务列表（方向、集合、节点、状态、进度、统计信息等）；
  - 实时刷新运行中的任务进度（页面会自动轮询运行中/排队中的任务）。

#### 6. 常见问题排查（FAQ）

- **打开远程同步对话框时提示「请求的资源不存在」**：
  - 通常是 `GET /api/sync/nodes` 返回了 404；
  - 请确认后端已加载 `sync` 路由并重启服务，前端 Network 面板中该接口应返回 `{ success: true, data: [...] }`。
- **节点下拉列表为空**：
  - 检查是否已经在「同步节点管理」页面添加并启用了至少一个节点；
  - 只会显示 `status = active` 的节点。
- **同步任务长时间无进度**：
  - 检查服务器端日志（`logs/webapi.log`、`logs/tradingagents.log` 等）是否有超时或数据库连接错误；
  - 确认远程节点的 `/api/sync/data/export` / `/api/sync/data/import` 没有被防火墙或代理阻断。

#### 关注公众号

1. **关注公众号**: 微信搜索 **"TradingAgents-CN"** 并关注
2. 公众号每天推送项目最新进展和使用教程


- **微信公众号**: TradingAgents-CN（推荐）

  <img src="assets/wexin.png" alt="微信公众号" width="200"/>


## 🆚 中文增强特色

**相比原版新增**: 智能新闻分析 | 多层次新闻过滤 | 新闻质量评估 | 统一新闻工具 | 多LLM提供商集成 | 模型选择持久化 | 快速切换按钮 | | 实时进度显示 | 智能会话管理 | 中文界面 | A股数据 | 国产LLM | Docker部署 | 专业报告导出 | 统一日志管理 | Web配置界面 | 成本优化



## 🤝 贡献指南

我们欢迎各种形式的贡献：

### 贡献类型

- 🐛 **Bug修复** - 发现并修复问题
- ✨ **新功能** - 添加新的功能特性
- 📚 **文档改进** - 完善文档和教程
- 🌐 **本地化** - 翻译和本地化工作
- 🎨 **代码优化** - 性能优化和代码重构

### 贡献流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 📋 查看贡献者

查看所有贡献者和详细贡献内容：**[🤝 贡献者名单](CONTRIBUTORS.md)**

## 📄 许可证

本项目采用**混合许可证**模式，详见 [LICENSE](LICENSE) 文件：

### 🔓 开源部分（Apache 2.0）
- **适用范围**：除 `app/` 和 `frontend/` 外的所有文件
- **权限**：商业使用 ✅ | 修改分发 ✅ | 私人使用 ✅ | 专利使用 ✅
- **条件**：保留版权声明 ❗ | 包含许可证副本 ❗

### 🔒 专有部分（需商业授权）
- **适用范围**：`app/`（FastAPI后端）和 `frontend/`（Vue前端）目录
- **商业使用**：需要单独许可协议
- **联系授权**：[hsliup@163.com](mailto:hsliup@163.com)

### 📋 许可证选择建议
- **个人学习/研究**：可自由使用全部功能
- **商业应用**：请联系获取专有组件授权
- **定制开发**：欢迎咨询商业合作方案

## 🙏 致谢与感恩

### 🌟 向源项目开发者致敬

我们向 [Tauric Research](https://github.com/TauricResearch) 团队表达最深的敬意和感谢：

- **🎯 愿景领导者**: 感谢您们在AI金融领域的前瞻性思考和创新实践
- **💎 珍贵源码**: 感谢您们开源的每一行代码，它们凝聚着无数的智慧和心血
- **🏗️ 架构大师**: 感谢您们设计了如此优雅、可扩展的多智能体框架
- **💡 技术先驱**: 感谢您们将前沿AI技术与金融实务完美结合
- **🔄 持续贡献**: 感谢您们持续的维护、更新和改进工作

### 🤝 社区贡献者致谢

感谢所有为TradingAgents-CN项目做出贡献的开发者和用户！

详细的贡献者名单和贡献内容请查看：**[📋 贡献者名单](CONTRIBUTORS.md)**

包括但不限于：

- 🐳 **Docker容器化** - 部署方案优化
- 📄 **报告导出功能** - 多格式输出支持
- 🐛 **Bug修复** - 系统稳定性提升
- 🔧 **代码优化** - 用户体验改进
- 📝 **文档完善** - 使用指南和教程
- 🌍 **社区建设** - 问题反馈和推广
- **🌍 开源贡献**: 感谢您们选择Apache 2.0协议，给予开发者最大的自由
- **📚 知识分享**: 感谢您们提供的详细文档和最佳实践指导

**特别感谢**：[TradingAgents](https://github.com/TauricResearch/TradingAgents) 项目为我们提供了坚实的技术基础。虽然Apache 2.0协议赋予了我们使用源码的权利，但我们深知每一行代码的珍贵价值，将永远铭记并感谢您们的无私贡献。

### 🇨🇳 推广使命的初心

创建这个中文增强版本，我们怀着以下初心：

- **🌉 技术传播**: 让优秀的TradingAgents技术在中国得到更广泛的应用
- **🎓 教育普及**: 为中国的AI金融教育提供更好的工具和资源
- **🤝 文化桥梁**: 在中西方技术社区之间搭建交流合作的桥梁
- **🚀 创新推动**: 推动中国金融科技领域的AI技术创新和应用

### 🌍 开源社区

感谢所有为本项目贡献代码、文档、建议和反馈的开发者和用户。正是因为有了大家的支持，我们才能更好地服务中文用户社区。

### 🤝 合作共赢

我们承诺：

- **尊重原创**: 始终尊重源项目的知识产权和开源协议
- **反馈贡献**: 将有价值的改进和创新反馈给源项目和开源社区
- **持续改进**: 不断完善中文增强版本，提供更好的用户体验
- **开放合作**: 欢迎与源项目团队和全球开发者进行技术交流与合作

## 📈 版本历史

- **v0.1.13** (2025-08-02): 🤖 原生OpenAI支持与Google AI生态系统全面集成 ✨ **最新版本**
- **v0.1.12** (2025-07-29): 🧠 智能新闻分析模块与项目结构优化
- **v0.1.11** (2025-07-27): 🤖 多LLM提供商集成与模型选择持久化
- **v0.1.10** (2025-07-18): 🚀 Web界面实时进度显示与智能会话管理
- **v0.1.9** (2025-07-16): 🎯 CLI用户体验重大优化与统一日志管理
- **v0.1.8** (2025-07-15): 🎨 Web界面全面优化与用户体验提升
- **v0.1.7** (2025-07-13): 🐳 容器化部署与专业报告导出
- **v0.1.6** (2025-07-11): 🔧 阿里百炼修复与数据源升级
- **v0.1.5** (2025-07-08): 📊 添加Deepseek模型支持
- **v0.1.4** (2025-07-05): 🏗️ 架构优化与配置管理重构
- **v0.1.3** (2025-06-28): 🇨🇳 A股市场完整支持
- **v0.1.2** (2025-06-15): 🌐 Web界面和配置管理
- **v0.1.1** (2025-06-01): 🧠 国产LLM集成

📋 **详细更新日志**: [CHANGELOG.md](./docs/releases/CHANGELOG.md)

## 📞 联系方式

- **GitHub Issues**: [提交问题和建议](https://github.com/hsliuping/TradingAgents-CN/issues)
- **邮箱**: hsliup@163.com
- 项目ＱＱ群：187537480
- 项目微信公众号：TradingAgents-CN

  <img src="assets/wexin.png" alt="微信公众号" width="200"/>

- **原项目**: [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents)
- **文档**: [完整文档目录](docs/)

## ⚠️ 风险提示

**重要声明**: 本框架仅用于研究和教育目的，不构成投资建议。

- 📊 交易表现可能因多种因素而异
- 🤖 AI模型的预测存在不确定性
- 💰 投资有风险，决策需谨慎
- 👨‍💼 建议咨询专业财务顾问

---

<div align="center">

**🌟 如果这个项目对您有帮助，请给我们一个 Star！**

[⭐ Star this repo](https://github.com/hsliuping/TradingAgents-CN) | [🍴 Fork this repo](https://github.com/hsliuping/TradingAgents-CN/fork) | [📖 Read the docs](./docs/)

</div>
