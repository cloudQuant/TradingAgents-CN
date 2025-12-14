# TradingAgents-CN v0.1.16 部署与运维指南

## 架构组件

- Nginx: 静态文件和反向代理
- FastAPI: 后端服务 (Uvicorn/Gunicorn)
- Redis: 队列与缓存
- MongoDB: 数据存储
- Worker: 任务执行进程

## 参考拓扑

```bash
[Internet] -> [Nginx] -> [FastAPI] -> [Redis/MongoDB]
                           |-> [Worker x N]

```bash

## 部署步骤

1. 准备环境
- Python 3.10+
- Node.js 18+
- Redis 6+
- MongoDB 5+

1. 后端部署
- 创建虚拟环境并安装依赖
- 配置环境变量(.env)
- 启动 Uvicorn 服务

1. 前端部署
- 构建 Vue3 应用
- 将 dist 目录部署到 Nginx

1. Worker 部署
- 配置并启动 worker 进程
- 建议使用 supervisor/systemd 进行守护

1. Nginx 配置
- 静态文件缓存
- 反代 /api 与 /api/stream
- SSE 的缓存与连接保持配置

## 运行维护

- 监控指标：队列长度、任务成功率、API 延迟
- 日志归集：后端、Worker、Nginx
- 备份策略：MongoDB 定期备份
- 故障演练：Redis/MongoDB 节点故障切换

## 灰度与回滚

- 蓝绿部署或金丝雀发布
- 保留 Streamlit 回退入口
- 回滚流程预案
