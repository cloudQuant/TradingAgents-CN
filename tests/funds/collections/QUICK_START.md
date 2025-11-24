# 快速开始 - 基金集合测试

## 🚀 一分钟快速测试

### 1. 安装依赖（首次运行）

```bash
pip install pytest httpx playwright
playwright install chromium
```

### 2. 启动服务

```bash
# Terminal 1 - 启动后端
cd F:\source_code\TradingAgents-CN
python -m uvicorn app.main:app --reload

# Terminal 2 - 启动前端  
cd F:\source_code\TradingAgents-CN\frontend
npm run dev
```

### 3. 运行测试

```bash
# Terminal 3 - 运行测试
cd F:\source_code\TradingAgents-CN
pytest tests\funds\collections\test_collections_requirements_coverage.py -v
```

## 📊 预期结果

### ✅ 测试通过示例

```
【需求文档扫描结果】
  从需求文档中解析到 70 个数据集合需要验证

【集合列表获取结果】
  成功获取到 72 个数据集合

【验证结果统计】
  [+] 已实现的集合: 70 个
  [x] 缺失的集合:   0 个
  覆盖率: 70/70 (100%)

【前端页面测试结果统计】
  [+] 成功打开的集合: 70 个
  [x] 打开失败的集合: 0 个

PASSED
```

### ⚠️ 如果测试失败

测试会生成详细报告：
- 位置：`tests/funds/test_coverage_report_{timestamp}.log`
- 包含：缺失集合列表、失败原因、对应需求文档

## 🎯 测试内容

### 测试 1: API 覆盖测试
- ✅ 扫描需求文档（支持两种格式）
- ✅ 调用 `/api/funds/collections`
- ✅ 验证所有集合都在 API 返回中

### 测试 2: 前端页面测试  
- ✅ 访问每个集合详情页
- ✅ 验证返回 200 状态码
- ✅ 确认未被重定向

## 🔧 需求文档格式

**格式 1: 前端路由**
```markdown
路由：http://localhost:3000/funds/collections/fund_name_em
```

**格式 2: 接口定义**
```markdown
接口: fund_name_em
```

## 📝 测试报告示例

```
================================================================================
【已实现的集合列表】(72个)
  1. [+] fund_announcement_dividend_em
  2. [+] fund_announcement_personnel_em
  3. [+] fund_announcement_report_em
  ...

【缺失的集合详情】(0个)
  无缺失

【额外集合】(2个)
  fund_net_value
  fund_ranking
================================================================================
```

## ⚡ 快速命令

```bash
# 只测试 API 覆盖
pytest tests\funds\collections\test_collections_requirements_coverage.py::TestFundsCollectionsRequirementsCoverage::test_requirements_collections_covered_by_api -v

# 只测试前端页面
pytest tests\funds\collections\test_collections_requirements_coverage.py::TestFundsCollectionsRequirementsCoverage::test_requirements_collections_frontend_openable -v

# 显示详细输出
pytest tests\funds\collections\test_collections_requirements_coverage.py -v -s

# 生成 HTML 报告
pytest tests\funds\collections\test_collections_requirements_coverage.py --html=report.html
```

## 🐛 常见问题速查

| 问题 | 解决方案 |
|------|---------|
| 后端未启动 | `python -m uvicorn app.main:app --reload` |
| 前端未启动 | `cd frontend && npm run dev` |
| 需要登录 | 测试会自动登录 (admin/admin123) |
| Playwright 未安装 | `pip install playwright && playwright install chromium` |
| 发现缺失集合 | 查看报告，在后端添加集合定义 |

## 📚 更多信息

- 详细说明：[README.md](README.md)
- 测试文件：[test_collections_requirements_coverage.py](test_collections_requirements_coverage.py)
- 需求文档：`tests/funds/*.md`

---

**提示**: 首次运行可能需要 1-2 分钟（浏览器启动、页面加载）  
**建议**: 定期运行测试，确保集合列表与需求文档保持同步
