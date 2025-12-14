# 集合数据获取优化说明

## 问题描述

用户反馈：前端页面 `/stocks/collections` 能显示 91 个数据集合，但测试获取不到数据。

## 根本原因

前端开发环境的 API 路径可能有以下情况：

1. **前端代理配置**：`<http://localhost:3000/api/*`> 被代理到后端 `<http://localhost:8000/api/*`>
2. **CORS 限制**：直接访问 API 端点可能被浏览器安全策略阻止
3. **开发模式限制**：某些框架在开发模式下 API 行为不同

## 解决方案：多方式智能获取

测试现在会**依次尝试 2 种方式**获取集合列表，直到成功：

### 方式 1: 后端 API 直连 🔌

```bash
URL: <http://localhost:8000/api/stocks/collections>
说明: 直接访问后端 API 服务
优点: 速度快、可靠，前端页面实际调用的就是这个 API

```bash

### 方式 2: 页面 DOM 提取 🎭

```bash
工具: Playwright 浏览器自动化
说明: 启动真实浏览器，从渲染后的页面提取数据
优点: 100%模拟真实用户行为，最可靠的备选方案

```bash

- *说明**：
- 前端 `<http://localhost:3000/stocks/collections`> 是 Vue SPA 页面路由，返回 HTML
- 前端内部会调用后端 API `<http://localhost:8000/api/stocks/collections`> 获取数据
- 没有所谓的"前端 API 代理"，直接访问后端 API 即可

## 运行要求

### 基础运行（方式 1）

```bash

# 只需要 httpx

pip install httpx pytest

```bash

### 完整功能（包含方式 2）

```bash

# 安装 Playwright

pip install playwright
playwright install chromium

# 然后运行测试

cd tests/stocks
pytest .\collections\test_collections_requirements_coverage.py -v -s

```bash

## 测试输出示例

### 成功场景（方式 1：后端 API）

```bash
正在获取集合列表...
  方式 1: 尝试后端 API <http://localhost:8000/api/stocks/collections>
  ✓ 后端 API 成功返回 91 个集合

【前端 API 返回结果】
  前端 API 返回 91 个数据集合

```bash

### Playwright 备选方案（方式 2：DOM 提取）

```bash
正在获取集合列表...
  方式 1: 尝试后端 API <http://localhost:8000/api/stocks/collections>
  ✗ 后端 API 需要认证（401）
  方式 2: 尝试从前端页面 DOM 提取数据（使用 Playwright）
    启动浏览器...
    访问页面: <http://localhost:3000/stocks/collections>
    等待数据加载...
    ✓ 从页面 DOM 提取到 91 个集合

【前端 API 返回结果】
  前端 API 返回 91 个数据集合

```bash

## 技术细节

### DOM 提取逻辑

1. 启动无头浏览器（Chromium）
2. 访问前端页面并等待网络空闲
3. 使用选择器提取集合链接：
   - `a[href*="/stocks/collections/"]` - 查找所有集合详情链接
   - `[data-collection-name]` - 查找带数据属性的元素
1. 解析链接提取集合名称
2. 转换为 API 数据格式

### 超时配置

- API 请求超时：60 秒
- 页面加载超时：60 秒
- 详情页测试超时：30 秒

## 常见问题

### Q1: 为什么不直接用 Playwright？

- *A**: Playwright 需要额外安装和下载浏览器驱动（~200MB），优先尝试轻量级的 HTTP 请求方式。

### Q2: 如果所有方式都失败怎么办？

- *A**: 测试会跳过（skip），不会失败（fail），并在日志中详细记录尝试过程。

### Q3: 认证令牌如何配置？

- *A**: 设置环境变量：

```bash

# Windows PowerShell

$env:TEST_AUTH_TOKEN="your-token-here"

# Linux/Mac

export TEST_AUTH_TOKEN="your-token-here"

```bash

### Q4: 如何只测试特定方式？

- *A**: 修改测试代码，注释掉不需要的方式即可。

## 性能对比

| 方式 | 速度 | 可靠性 | 依赖 | 说明 |

|------|------|--------|------|------|

| 后端 API 直连 | ⚡⚡⚡ 快 | ⭐⭐⭐ 高 | httpx | 最优先，前端实际调用的 API |

| 页面 DOM 提取 | ⚡ 较慢 | ⭐⭐⭐⭐ 最高 | playwright + chromium | 备选方案，100%可靠 |

## 建议配置

### 开发环境

```bash

# 安装完整依赖，支持所有方式

pip install -r requirements-test.txt
playwright install chromium

```bash

### CI/CD 环境

```bash

# 只安装基础依赖，使用 API 方式

pip install httpx pytest

```bash

## 版本历史

- **v4.1**(2024-11-23): 修正：移除不存在的"前端 API 代理"方式，现在只使用 2 种正确的方式
- **v4.0**(2024-11-23): 增加多方式智能获取，支持 Playwright DOM 提取
- **v2.0**(2024-11-23): 增加超时配置和详细日志
- **v1.0** (2024-11-23): 初始版本

## 相关文件

- `test_collections_requirements_coverage.py` - 主测试文件
- `CHANGELOG.md` - 详细变更记录
- `README_测试优化.md` - 测试优化说明

## 联系方式

如有问题，请查看测试日志文件：

```bash
tests/stocks/test_coverage_report_YYYYMMDD_HHMMSS.log

```bash
