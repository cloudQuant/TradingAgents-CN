# 债券数据集合测试覆盖率说明

## 概述

`test_collections_requirements_coverage.py` 是一个综合测试文件，用于验证债券数据集合是否按照需求文档完整实现。

## 测试内容

### 1. 需求文档扫描
- 自动扫描 `tests/bonds/requirements/` 目录下的所有 Markdown 文档
- 提取文档中声明的集合路由：`http://localhost:3000/bonds/collections/{collectionName}`
- 建立集合名称与需求文档的映射关系

### 2. API集合列表验证
- 验证 `/api/bonds/collections` API 是否返回所有需求文档中声明的集合
- 支持多种获取方式：
  - **优先**：使用 Playwright 从前端页面 DOM 提取（更真实）
  - **备选**：直接调用后端 API
- 统计已实现、缺失和额外的集合
- 计算实现覆盖率

### 3. 前端页面可访问性测试
- 验证每个集合的详情页 `/bonds/collections/{name}` 是否能正常打开
- 检查 HTTP 状态码和页面路由
- 识别无法打开的页面并输出详细信息

## 运行测试

### 前置条件

1. **安装依赖**：
```bash
pip install pytest httpx playwright
playwright install chromium
```

2. **启动服务**：
   - 后端服务：`http://localhost:8000`（可选，作为备选数据源）
   - 前端服务：`http://localhost:3000`（用于页面访问测试）

3. **认证配置**（可选）：
```bash
# 如果 API 需要认证，设置环境变量
export TEST_AUTH_TOKEN="your_access_token_here"
```

### 执行测试

```bash
# 在项目根目录执行
cd f:\source_code\TradingAgents-CN

# 运行所有测试
pytest tests/bonds/collections/test_collections_requirements_coverage.py -v

# 只运行 API 覆盖测试
pytest tests/bonds/collections/test_collections_requirements_coverage.py::TestBondsCollectionsRequirementsCoverage::test_requirements_collections_covered_by_api -v

# 只运行前端页面测试
pytest tests/bonds/collections/test_collections_requirements_coverage.py::TestBondsCollectionsRequirementsCoverage::test_requirements_collections_frontend_openable -v
```

### 自定义配置

可以通过环境变量自定义配置：

```bash
# 自定义 API 地址
export API_BASE_URL="http://localhost:8000"

# 自定义前端地址
export FRONTEND_BASE_URL="http://localhost:3000"

# 提供认证令牌
export TEST_AUTH_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## 测试输出

### 控制台输出

测试会在控制台实时输出：
- 需求文档扫描结果
- 集合列表获取进度
- 验证结果统计
- 已实现/缺失/额外的集合清单
- 前端页面测试进度和结果

### 日志文件

详细日志自动保存到：
```
tests/bonds/test_coverage_report_YYYYMMDD_HHMMSS.log
```

日志包含：
- 完整的测试执行过程
- 所有集合的验证详情
- 失败的集合及其需求文档路径
- 统计数据和覆盖率计算

## 测试报告示例

```
================================================================================
【需求文档扫描结果】
  从需求文档中解析到 32 个数据集合需要验证
  需求文档目录: f:\source_code\TradingAgents-CN\tests\bonds\requirements
================================================================================

正在获取集合列表...
  方式1: 尝试从前端页面DOM提取数据（使用Playwright）
    启动浏览器...
    访问页面: http://localhost:3000/bonds/collections
    等待数据加载...
    [+] 从页面DOM提取到 16 个集合

【集合列表获取结果】
  成功获取到 16 个数据集合
================================================================================

【验证结果统计】
  [+] 已实现的集合: 16 个
  [x] 缺失的集合:   16 个
  覆盖率: 16/32 (50%)
================================================================================

【已实现的集合列表】(16个)
    1. [+] bond_cash_summary_sse
    2. [+] bond_deal_summary_sse
    ...

【缺失的集合详情】(16个)
    1. [x] bond_cov_comparison
         文档: 17_可转债比价表.md
    ...
```

## 自动登录支持

测试支持自动登录功能：
- 检测到登录页面时自动填写用户名密码（admin/admin123）
- 登录成功后继续执行测试
- 登录失败时给出明确提示

## 故障排查

### 1. 无法获取集合列表

**症状**：测试跳过，提示"无法获取集合列表"

**解决方案**：
- 确认前端服务已启动：`http://localhost:3000`
- 确认后端服务已启动：`http://localhost:8000`（可选）
- 检查防火墙或代理设置
- 如需认证，设置 `TEST_AUTH_TOKEN` 环境变量

### 2. Playwright 相关错误

**症状**：提示 "Playwright未安装"

**解决方案**：
```bash
pip install playwright
playwright install chromium
```

### 3. 前端页面无法访问

**症状**：测试跳过，提示"前端未启动或无法访问"

**解决方案**：
- 确认前端开发服务器已启动
- 检查端口 3000 是否被占用
- 尝试手动访问 `http://localhost:3000/bonds/collections`

### 4. 部分集合详情页打开失败

**症状**：部分集合测试失败，状态码 404 或重定向

**解决方案**：
- 检查对应集合的前端路由配置
- 确认集合名称拼写正确
- 查看详细日志文件中的错误信息
- 参考失败的需求文档修复前端页面

## 持续集成

可以将此测试集成到 CI/CD 流程中：

```yaml
# .github/workflows/test-bonds-collections.yml
name: Bonds Collections Coverage

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install playwright
          playwright install chromium
      - name: Start services
        run: |
          # 启动后端和前端服务的命令
      - name: Run tests
        run: |
          pytest tests/bonds/collections/test_collections_requirements_coverage.py -v
```

## 贡献指南

添加新的债券数据集合时：

1. 在 `tests/bonds/requirements/` 创建需求文档（.md 文件）
2. 文档中包含集合路由：`http://localhost:3000/bonds/collections/{集合名称}`
3. 实现后端 API 和前端页面
4. 运行此测试验证实现完整性

## 相关文件

- 测试文件：`tests/bonds/collections/test_collections_requirements_coverage.py`
- 需求文档：`tests/bonds/requirements/*.md`
- 日志目录：`tests/bonds/`
- 参考实现：`tests/stocks/collections/test_collections_requirements_coverage.py`

## 技术栈

- **测试框架**：pytest
- **HTTP 客户端**：httpx
- **浏览器自动化**：Playwright
- **日志记录**：自定义 Logger 类
- **正则表达式**：用于提取集合路由

## 常见问题

**Q: 为什么优先使用前端 DOM 提取而不是后端 API？**

A: 前端 DOM 提取更真实地反映用户实际看到的内容，可以发现前端配置问题。后端 API 作为备选方案确保测试的鲁棒性。

**Q: 如何手动获取 TEST_AUTH_TOKEN？**

A: 
1. 浏览器登录系统
2. 打开开发者工具 → Application/存储 → Local Storage
3. 查找 `access_token` 或 `token` 字段
4. 复制值设置为环境变量

**Q: 测试失败后如何定位问题？**

A:
1. 查看详细日志文件（路径在测试输出中）
2. 检查失败集合对应的需求文档
3. 手动访问失败的 URL 确认问题
4. 检查浏览器控制台和网络请求

---

**维护者**：TradingAgents-CN Team  
**最后更新**：2024-11-24  
**版本**：1.0
