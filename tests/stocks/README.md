# 股票投研功能测试

## 功能概述

本测试套件用于验证股票投研功能的实现，包括：
1. ✅ 侧边栏菜单显示"股票投研"
2. ✅ 概览页面
3. ✅ 数据集合页面
4. ✅ 数据集合API接口

## 测试文件

```
tests/stocks/
├── pytest.ini                           # pytest配置
├── run_tests.bat                        # Windows运行脚本
├── README.md                           # 本文档
├── 股票需求01.md                        # 原始需求
├── 验收说明.md                          # 验收指南
├── verify_collections_api.py            # 独立验收脚本
└── collections/
    └── test_collections_page.py        # 数据集合测试用例
```

## 运行测试

### 方式1：使用批处理脚本（推荐）

```bash
cd f:\source_code\TradingAgents-CN\tests\stocks
.\run_tests.bat
```

### 方式2：直接使用pytest

```bash
cd f:\source_code\TradingAgents-CN\tests\stocks
pytest collections\test_collections_page.py -v
```

### 方式3：运行所有测试

```bash
cd f:\source_code\TradingAgents-CN\tests\stocks
pytest -v
```

## 前提条件

### 1. 后端服务运行

确保后端服务在端口8000运行：

```bash
cd f:\source_code\TradingAgents-CN
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

检查服务状态：
```bash
curl http://localhost:8000/api/health
```

### 2. 认证Token（可选）

如果测试需要认证，设置环境变量：

```bash
# PowerShell
$env:TEST_AUTH_TOKEN = "your_token_here"

# CMD
set TEST_AUTH_TOKEN=your_token_here
```

## 测试说明

### 测试1：接口存在性测试

**测试方法**: `test_collections_endpoint_exists`

**测试内容**:
- 访问 `/api/stocks/collections` 接口
- 验证返回状态码为 200 或 401（未认证）

**通过条件**:
- ✅ 状态码为 200（成功）或 401（需要认证）
- ❌ 状态码为 404（接口不存在）或 500（服务器错误）

### 测试2：数据结构测试

**测试方法**: `test_collections_list_structure`

**测试内容**:
- 验证返回数据是列表
- 验证列表不为空
- 验证每个集合包含必需字段：
  - name（集合名称）
  - display_name（显示名称）
  - description（描述）
  - route（路由）
  - fields（字段列表）

**通过条件**:
- ✅ 所有字段都存在且类型正确
- ❌ 缺少字段或类型错误

### 测试3：集合完整性测试

**测试方法**: `test_expected_collections_present`

**测试内容**:
- 验证6个期望的数据集合都存在：
  1. stock_basic_info（股票基础信息）
  2. market_quotes（实时行情数据）
  3. stock_financial_data（财务数据）
  4. stock_daily（日线行情）
  5. stock_weekly（周线行情）
  6. stock_monthly（月线行情）

**通过条件**:
- ✅ 所有6个集合都在返回数据中
- ❌ 缺少任何一个集合

## 常见问题

### Q1: 编码错误（UnicodeDecodeError）

**问题**:
```
UnicodeDecodeError: 'gbk' codec can't decode byte 0xaa in position 14
```

**解决方案**:
1. 不要使用 `python test_collections_page.py` 运行
2. 使用 `pytest test_collections_page.py` 或运行脚本

### Q2: 401 未授权错误

**问题**: 测试返回 401 状态码

**解决方案**:
1. 设置环境变量 `TEST_AUTH_TOKEN`
2. 或者测试会自动跳过需要认证的部分

### Q3: 连接错误

**问题**: 
```
Connection refused 或 Network Error
```

**解决方案**:
1. 确认后端服务正在运行
2. 检查端口8000没有被占用
3. 检查防火墙设置

### Q4: 测试超时

**问题**: 测试运行时间过长

**解决方案**:
- 检查网络连接
- 检查后端服务是否正常响应
- 可以在测试中增加timeout参数

## 验收标准

### 完全通过 ✅

所有3个测试都通过：
```
test_collections_endpoint_exists PASSED
test_collections_list_structure PASSED  
test_expected_collections_present PASSED
```

### 部分通过 ⚠️

测试1通过，测试2和3因为401跳过：
```
test_collections_endpoint_exists PASSED
test_collections_list_structure SKIPPED (需要认证)
test_expected_collections_present SKIPPED (需要认证)
```

这表示接口存在但需要认证，功能正常。

### 失败 ❌

任何测试失败表示功能有问题，需要修复。

## 相关文档

- **需求文档**: `股票需求01.md`
- **验收说明**: `验收说明.md`
- **后端代码**: `app/routers/stocks.py` (第663-712行)
- **前端页面**: `frontend/src/views/Stocks/Collections.vue`
- **路由配置**: `frontend/src/router/index.ts`
- **侧边栏**: `frontend/src/components/Layout/SidebarMenu.vue`

## 联系方式

如有问题，请查看项目文档或提交Issue。

---

**最后更新**: 2025-11-18  
**测试版本**: v1.0
