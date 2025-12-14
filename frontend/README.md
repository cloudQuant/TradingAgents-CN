# 云子量化 前端应用

现代化的 Vue3 前端界面，为云子量化提供优秀的用户体验。

## 🚀 快速开始

### 环境要求

- Node.js >= 18.0.0
- npm >= 8.0.0

### 安装依赖

```bash
npm install

```bash

### 启动开发服务器

```bash
npm run dev

```bash
访问 <http://localhost:3000>

### 构建生产版本

```bash
npm run build

```bash

### 预览生产版本

```bash
npm run preview

```bash

## 📁 项目结构

```bash
frontend/
├── public/                 # 静态资源

├── src/
│   ├── api/               # API 接口

│   ├── components/        # 组件

│   │   ├── Global/       # 全局组件

│   │   └── Layout/       # 布局组件

│   ├── layouts/          # 页面布局

│   ├── router/           # 路由配置

│   ├── stores/           # 状态管理

│   ├── styles/           # 样式文件

│   ├── types/            # 类型定义

│   ├── utils/            # 工具函数

│   ├── views/            # 页面组件

│   ├── App.vue           # 根组件

│   └── main.ts           # 应用入口

├── index.html            # HTML 模板

├── package.json          # 项目配置

├── tsconfig.json         # TypeScript 配置

├── vite.config.ts        # Vite 配置

└── README.md             # 说明文档

```bash

## 🎨 主要功能

### 📊 仪表板

- 数据概览和统计
- 快速操作入口
- 系统状态监控
- 最近分析记录

### 🔍 股票筛选

- 多维度筛选条件
- 实时结果展示
- 批量操作支持
- 筛选结果导出

### 📈 股票分析

- 单股深度分析
- 批量分析处理
- 分析历史查看
- 进度实时跟踪

### 📋 队列管理

- 任务队列监控
- 实时状态更新
- 任务优先级管理
- 批量操作支持

### 📄 分析报告

- 报告生成和管理
- 多格式导出支持
- 报告分享功能
- 历史报告查看

### ⚙️ 系统设置

- 个人偏好配置
- 主题和外观设置
- 分析参数配置
- 安全设置管理

## 🛠️ 技术栈

### 核心框架

- **Vue 3**- 渐进式 JavaScript 框架
- **TypeScript**- 类型安全的 JavaScript
- **Vite**- 现代化构建工具

### UI 组件库

- **Element Plus**- 企业级 Vue 组件库
- **@element-plus/icons-vue**- 图标组件

### 状态管理

- **Pinia**- Vue 官方状态管理库
- **@vueuse/core**- Vue 组合式 API 工具集

### 路由和网络

- **Vue Router 4**- 官方路由管理器
- **Axios**- HTTP 客户端

### 开发工具

- **ESLint**- 代码质量检查
- **Prettier**- 代码格式化
- **unplugin-auto-import**- 自动导入
- **unplugin-vue-components**- 组件自动导入

## 🎯 特色功能

### 🌈 现代化设计

- 响应式布局设计
- 明暗主题切换
- 流畅的动画效果
- 移动端适配

### 🔧 开发体验

- TypeScript 类型安全
- 组件自动导入
- 热模块替换
- 代码分割优化

### 🚀 性能优化

- 路由懒加载
- 组件按需加载
- 图片懒加载
- 缓存策略优化

### 🔒 安全特性

- JWT 认证集成
- 权限路由守卫
- XSS 防护
- CSRF 保护

## 📱 响应式设计

支持多种设备尺寸：

- **桌面端**: >= 1200px
- **平板端**: 768px - 1199px
- **手机端**: < 768px

## 🎨 主题定制

支持多种主题模式：

- **浅色主题**: 适合白天使用
- **深色主题**: 适合夜间使用
- **自动模式**: 跟随系统设置

## 🔧 配置说明

### 环境变量

创建 `.env.local` 文件：

```env

# API 基础 URL

VITE_API_BASE_URL=<http://localhost:8000/api>

# 应用标题

VITE_APP_TITLE=云子量化

```bash

### 代理配置

开发环境自动代理 API 请求到后端服务：

```typescript
// vite.config.ts
server: {
  proxy: {
    '/api': {
      target: '<http://localhost:8000',>
      changeOrigin: true
    }
  }
}

```bash

## 🚀 部署指南

### 构建应用

```bash
npm run build

```bash

### 部署到 Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass <http://localhost:8000;>
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

```bash

## 🤝 开发指南

### 添加新页面

1. 在 `src/views/` 创建页面组件
2. 在 `src/router/index.ts` 添加路由
3. 在侧边栏菜单中添加导航

### 添加新 API

1. 在 `src/types/` 定义类型
2. 在 `src/api/` 创建 API 模块
3. 在组件中使用 API

### 状态管理

使用 Pinia 进行状态管理：

```typescript
// 定义 store
export const useExampleStore = defineStore('example', {
  state: () => ({
    data: []
  }),
  actions: {
    async fetchData() {
      // 获取数据逻辑
    }
  }
})

// 在组件中使用
const exampleStore = useExampleStore()

```bash

## 📝 代码规范

### 命名规范

- 组件名：PascalCase
- 文件名：kebab-case
- 变量名：camelCase
- 常量名：UPPER_SNAKE_CASE

### 提交规范

- feat: 新功能
- fix: 修复 bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 代码重构
- test: 测试相关
- chore: 构建过程或辅助工具的变动

## 🐛 问题排查

### 常见问题

1. **依赖安装失败**

   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

1. **端口被占用**

   ```bash

# 修改端口
   npm run dev -- --port 3001
   ```

1. **类型错误**

   ```bash

# 重新生成类型文件
   npm run type-check
   ```

## 📞 技术支持

如有问题，请通过以下方式联系：

- 📧 邮箱: hsliup@163.com
- 💬 微信群: 扫描 README 中的二维码
- 🐛 问题反馈: GitHub Issues

- --

- *云子量化 Frontend v1.0.0-preview** - 现代化的股票分析平台前端
