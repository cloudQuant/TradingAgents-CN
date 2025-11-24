# 基金数据集合测试

## 测试目的

验证 funds/collections 页面与需求文档的一致性：
1. 从需求文档中提取所有数据集合定义
2. 验证后端 API 是否返回所有需要的集合
3. 测试前端详情页能否正常打开

## 测试文件

- `test_collections_requirements_coverage.py` - 主测试文件

## 运行测试

### 前提条件

1. 安装测试依赖：
```bash
pip install pytest httpx playwright
playwright install chromium
```

2. 启动后端服务：
```bash
cd F:\source_code\TradingAgents-CN
# 启动 FastAPI 后端（默认 http://localhost:8000）
python -m uvicorn app.main:app --reload
```

3. 启动前端服务：
```bash
cd F:\source_code\TradingAgents-CN\frontend
# 启动 Vue 前端（默认 http://localhost:3000）
npm run dev
```

### 运行测试命令

```bash
# 进入项目根目录
cd F:\source_code\TradingAgents-CN

# 运行所有测试
pytest tests\funds\collections\test_collections_requirements_coverage.py -v

# 只运行 API 覆盖测试
pytest tests\funds\collections\test_collections_requirements_coverage.py::TestFundsCollectionsRequirementsCoverage::test_requirements_collections_covered_by_api -v

# 只运行前端页面可访问性测试
pytest tests\funds\collections\test_collections_requirements_coverage.py::TestFundsCollectionsRequirementsCoverage::test_requirements_collections_frontend_openable -v

# 显示详细输出
pytest tests\funds\collections\test_collections_requirements_coverage.py -v -s
```

### 环境变量配置（可选）

```bash
# Windows PowerShell
$env:API_BASE_URL="http://localhost:8000"
$env:FRONTEND_BASE_URL="http://localhost:3000"
$env:TEST_AUTH_TOKEN="your_token_here"  # 如果需要认证

# 然后运行测试
pytest tests\funds\collections\test_collections_requirements_coverage.py -v
```

## 测试内容

### 测试1: API 覆盖测试 (`test_requirements_collections_covered_by_api`)

**验证内容：**
- 扫描 `tests/funds/*.md` 需求文档，提取所有集合定义
- 支持两种格式：
  - 前端路由格式：`http://localhost:3000/funds/collections/{name}`
  - 接口定义格式：`接口: {name}`
- 调用 `/api/funds/collections` API
- 验证所有需求文档中的集合都在 API 返回中

**成功标准：**
- ✅ 所有需求文档中定义的集合都在 API 返回列表中
- ✅ 生成详细的测试报告，包括：
  - 已实现的集合列表
  - 缺失的集合（如果有）
  - 额外的集合（未在需求文档中声明）

### 测试2: 前端页面可访问性测试 (`test_requirements_collections_frontend_openable`)

**验证内容：**
- 访问每个集合的详情页：`/funds/collections/{name}`
- 验证页面返回 200 状态码
- 验证页面未被重定向（如重定向到登录页）

**成功标准：**
- ✅ 所有集合详情页都能正常打开
- ✅ 页面未被重定向到其他路径
- ✅ 返回 HTTP 200 状态码

## 测试报告

测试完成后会生成详细报告：
- 报告位置：`tests/funds/test_coverage_report_{timestamp}.log`
- 包含内容：
  - 需求文档扫描结果
  - 集合列表获取结果
  - 验证结果统计
  - 已实现/缺失/额外的集合列表
  - 前端页面测试结果

## 测试特性

### 智能数据获取

测试会尝试多种方式获取集合列表：

1. **前端页面 DOM 提取（优先）**
   - 使用 Playwright 自动化浏览器
   - 支持自动登录（用户名：admin，密码：admin123）
   - 从页面 DOM 提取集合链接
   - 调用前端 API 获取数据

2. **后端 API 调用（备选）**
   - 直接调用 `/api/funds/collections`
   - 支持 Bearer Token 认证

### 自动登录

如果检测到需要登录，测试会：
1. 自动填写登录表单（admin/admin123）
2. 点击登录按钮
3. 等待跳转完成
4. 重新访问目标页面

### 多种提取策略

从前端页面提取集合时，支持：
1. 查找包含 `/funds/collections/` 的链接
2. 查找 `data-collection-name` 属性
3. 调用前端 API `/api/funds/collections`
4. 监听网络响应

## 常见问题

### Q1: 测试提示"需要认证"

**解决方案：**
1. 确保后端已启动
2. 尝试手动登录前端，确认账号密码正确
3. 如果需要 Token，设置环境变量：
   ```bash
   $env:TEST_AUTH_TOKEN="your_token"
   ```

### Q2: 测试提示"前端未启动"

**解决方案：**
```bash
cd frontend
npm run dev
```
确保前端在 http://localhost:3000 运行

### Q3: Playwright 相关错误

**解决方案：**
```bash
# 安装 Playwright
pip install playwright

# 安装浏览器
playwright install chromium
```

### Q4: 发现缺失的集合

**处理步骤：**
1. 查看测试报告中的缺失集合列表
2. 找到对应的需求文档
3. 在后端 `app/routers/funds.py` 中添加集合定义：
   ```python
   {
       "name": "collection_name",
       "display_name": "集合显示名称",
       "description": "集合描述",
       "route": "/funds/collections/collection_name",
       "fields": ["字段1", "字段2", ...],
   }
   ```
4. 重新运行测试验证

### Q5: 详情页打开失败

**处理步骤：**
1. 检查前端路由配置
2. 检查 Vue 组件是否存在
3. 查看测试报告中的具体错误信息
4. 手动访问 URL 进行调试

## 需求文档格式

测试支持两种格式的需求文档：

### 格式1: 前端路由格式
```markdown
# 集合名称

集合路由：http://localhost:3000/funds/collections/fund_name_em

...
```

### 格式2: 接口定义格式（基金常用）
```markdown
# 集合名称

### 获取数据的API接口、字段等

接口: fund_name_em

...
```

## 测试维护

### 添加新集合时

1. 在 `tests/funds/` 创建需求文档（使用上述任一格式）
2. 在后端添加集合定义
3. 运行测试验证：
   ```bash
   pytest tests\funds\collections\test_collections_requirements_coverage.py -v
   ```

### 定期运行

建议：
- 每次发布前运行完整测试
- 每周运行一次验证
- 添加新集合后必须运行

## 相关文档

- [基金投研功能实现总结](../基金投研功能实现总结.md)
- [测试摘要](../TEST_SUMMARY.md)
- [详细报告](../collections_test_report.md)

---

**创建时间**: 2025-11-24  
**维护者**: TradingAgents-CN Team
