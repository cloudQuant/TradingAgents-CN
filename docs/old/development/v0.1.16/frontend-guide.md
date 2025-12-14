# TradingAgents-CN v0.1.16 前端开发指南 (Vue3)

## 概述

本指南面向前端开发者，介绍如何基于 Vue3+Vite 构建 TradingAgents-CN 的 SPA 前端，连接 FastAPI 后端与 SSE 进度流。

## 技术栈

- Vue3 + Composition API
- Vite
- Pinia
- Vue Router
- Axios
- Element Plus
- EventSource (SSE)

## 开发环境

1. 安装 Node.js >= 18
2. 初始化项目

```bash
npm create vite@latest tradingagents-web -- --template vue
cd tradingagents-web
npm install element-plus pinia vue-router axios
npm install -D eslint prettier @vitejs/plugin-vue

```bash

1. 环境配置

```bash

# .env.development

VITE_API_BASE=<http://localhost:8000>
VITE_SSE_BASE=<http://localhost:8000>

```bash

## 目录结构建议

```bash
src/
├── main.ts
├── router/
├── stores/
├── components/
├── views/
├── services/
└── utils/

```bash

## 鉴权与路由守卫

- 登录成功后存储 JWT 到 HttpOnly Cookie 或内存
- 路由守卫检查登录态，未登录跳转登录页

## API 与 SSE 封装

- axios 实例添加拦截器，统一错误处理
- EventSource 封装，自动重连与心跳

## 关键页面

- Dashboard: 概览与快捷入口
- Screening: 选股与多选
- BatchAnalysis: 批量提交与参数配置
- QueuePanel: 队列状态与任务操作
- History: 历史记录与报告

## 组件建议

- StockSelector: 股票搜索与多选
- BatchUploader: 文本域+CSV 上传
- ProgressBar: 可订阅 SSE 的进度条
- TaskList: 任务列表

## 联调与调试

- 本地同时启动 Vite 与 FastAPI，配置 CORS
- 使用网络面板观察 SSE 事件流

## 构建与部署

- 生产环境打包：`npm run build`
- Nginx 静态托管，反代 /api 与 /api/stream

## 最佳实践

- 统一的 Loading 与空状态
- 表单校验与错误提示
- 状态最小化，跨页数据下沉到 Pinia
- 组件解耦，复用性优先
