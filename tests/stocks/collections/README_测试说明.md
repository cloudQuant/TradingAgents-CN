# 股票数据集合测试说明

## test_collections_requirements_coverage.py

### 功能
验证 stocks/collections 页面与需求文档的一致性：
1. 从 `tests/stocks/requirements/*.md` 解析需求文档中声明的集合（约365个）
2. 校验后端 API `/api/stocks/collections` 是否返回这些集合
3. 测试前端页面 `/stocks/collections/{name}` 是否可以正常打开
4. 生成详细的测试报告日志文件

**重要说明：**
- 需求文档中可能声明了365个集合，但 API 可能只实现了其中一部分（如91个）
- **第一个测试**会验证 API 是否返回了需求文档中声明的所有集合，如果有缺失会显示详细列表
- **第二个测试**只会测试那些**既在需求文档中声明又在 API 中实现**的集合（如91个）
- 不会测试那些尚未在 API 中实现的集合，因为前端无法访问不存在的数据

### 快速检查（推荐先运行）

在运行完整测试之前，建议先运行快速检查，了解当前状态：

```powershell
cd f:\source_code\TradingAgents-CN\tests\stocks

# 快速检查当前覆盖率
python quick_check.py
```

这会快速显示：
- 需求文档中声明了多少个集合
- API 实际返回了多少个集合
- 缺少了多少个集合
- 覆盖率百分比

### 运行完整测试

```powershell
# 在 tests/stocks 目录下运行
cd f:\source_code\TradingAgents-CN\tests\stocks

# 方式1：显示详细输出（推荐）
pytest .\collections\test_collections_requirements_coverage.py -v -s

# 方式2：静默运行
pytest .\collections\test_collections_requirements_coverage.py

# 方式3：只运行 API 覆盖测试
pytest .\collections\test_collections_requirements_coverage.py::TestStocksCollectionsRequirementsCoverage::test_requirements_collections_covered_by_api -v -s

# 方式4：只运行前端页面测试
pytest .\collections\test_collections_requirements_coverage.py::TestStocksCollectionsRequirementsCoverage::test_requirements_collections_frontend_openable -v -s
```

### 环境变量（可选）

```powershell
# 设置后端 API 地址（默认 http://localhost:8000）
$env:API_BASE_URL="http://localhost:8000"

# 设置前端地址（默认 http://localhost:3000）
$env:FRONTEND_BASE_URL="http://localhost:3000"

# 设置认证 Token（可选，如果后端需要认证）
$env:TEST_AUTH_TOKEN="your_token_here"
```

### 测试输出

#### 控制台输出
显示实时测试进度和摘要统计：
- 需求文档中声明的集合数量
- API 返回的集合数量
- 已实现/缺失的集合列表
- 前端页面测试进度
- 成功/失败的统计

#### 日志文件
详细的测试日志会自动保存到：
```
tests/stocks/test_coverage_report_YYYYMMDD_HHMMSS.log
```

日志文件包含：
- 完整的集合列表（已实现和缺失）
- 每个集合的测试结果
- 失败集合的详细信息（状态码、错误信息、对应需求文档）

### 输出示例

```
================================================================================
【需求文档扫描结果】
  从需求文档中解析到 300 个数据集合需要验证
  需求文档目录: f:\source_code\TradingAgents-CN\tests\stocks\requirements
================================================================================

【API 接口返回结果】
  API 接口 /api/stocks/collections 返回 90 个数据集合
  API 地址: http://localhost:8000/api/stocks/collections
================================================================================

【验证结果统计】
  ✓ 已实现的集合: 90 个
  ✗ 缺失的集合:   210 个
  覆盖率: 90/300 (30%)
================================================================================

【已实现的集合列表】(90个)
    1. ✓ market_quotes
    2. ✓ stock_basic_info
    3. ✓ stock_daily
    ...

【缺失的集合详情】(210个)
    1. ✗ stock_zh_a_hist
         文档: 05_A股历史行情-东财.md
    2. ✗ stock_individual_info_em
         文档: 12_个股信息查询-东财-完成.md
    ...
================================================================================

✓ 详细日志已保存到: f:\source_code\TradingAgents-CN\tests\stocks\test_coverage_report_20241123_195530.log
```

### 如何使用测试结果

1. **查看缺失的集合**
   - 日志文件会列出所有缺失的集合名称
   - 每个缺失集合会标注对应的需求文档
   - 按照需求文档实现对应的后端接口和前端页面

2. **查看失败的页面**
   - 日志会显示哪些集合详情页打开失败
   - 包含 HTTP 状态码和最终跳转路径
   - 根据对应的需求文档修复前端路由或页面

3. **追踪进度**
   - 运行测试可以看到当前实现的覆盖率
   - 每次实现新集合后重新运行测试验证

### 注意事项

1. **pytest 输出被截断问题**
   - 使用 `-s` 参数：`pytest ... -s`
   - 查看日志文件获取完整信息

2. **后端未启动**
   - 测试会自动跳过并提示
   - 启动后端后重新运行

3. **前端未启动**
   - 前端页面测试会跳过
   - 启动前端后重新运行

4. **需要认证**
   - 设置 `TEST_AUTH_TOKEN` 环境变量
   - 或者在测试时跳过认证测试
