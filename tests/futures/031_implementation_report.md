# 031号需求完整实现报告

**需求名称**: 内盘-分时行情数据 (futures_zh_minute_sina)
**实施日期**: 2024年11月23日
**状态**: ✅ 已完成

## 📊 实施内容

### 1. 后端实现 ✅

#### Update任务函数
**文件**: `app/services/futures_update_tasks.py`
**函数**: `update_futures_zh_minute_sina_task`

**功能特性**:
- **必需参数**: symbol（合约代码，如"IF2008"）
- **可选参数**: period（分钟周期，默认"1"）
- 支持多种周期: "1", "5", "15", "30", "60"分钟
- 自动添加更新时间和查询参数
- 使用 symbol + period + datetime 作为唯一键
- 完整的错误处理和日志记录

**关键参数**:
```python
async def update_futures_zh_minute_sina_task(
    symbol: str,         # 合约代码（必需）
    period: str = "1"    # 分钟周期（可选，默认1分钟）
)
```

#### API路由增强
**文件**: `app/routers/futures.py`

**新增参数**:
- `period`: Query参数，默认值"1"

**支持两种调用方式**:
1. **独立参数**（推荐）: `symbol=IF2008&period=5`
2. **组合格式**（兼容）: `symbol=IF2008:5`

### 2. 前端实现 ✅

**复用Collection.vue组件** - 在029号实现中创建，完全兼容本需求

### 3. 测试验证 ✅

**测试文件**: `tests/futures/collections/031_futures_zh_minute_sina_collection.py`

**测试结果**:
```
✓ test_collection_info_exists  - 集合信息存在性测试
✓ test_get_data                - 数据获取测试  
✓ test_update_data             - 数据更新测试

3 passed in 5.46s
```

## 🎯 核心功能

### 数据更新流程
1. 用户输入合约代码和周期（如"IF2008", "5"）
2. 前端调用API发送更新请求
3. 后端验证symbol参数
4. 调用akshare获取指定合约的分时数据
5. 数据清洗和标准化
6. 批量更新到MongoDB（使用upsert）
7. 返回任务状态

### 与前两个需求的对比

| 特性 | 029: futures_zh_spot | 030: futures_zh_realtime | 031: futures_zh_minute_sina |
|------|---------------------|-------------------------|----------------------------|
| symbol参数 | 可选 | **必需** | **必需** |
| 额外参数 | market, adjust | 无 | **period** |
| 数据类型 | 实时快照 | 品种所有合约 | 历史分时K线 |
| 唯一键 | symbol + time | symbol + tradedate | symbol + period + datetime |

## 📋 数据字段

| 字段名 | 类型 | 描述 |
|--------|------|------|
| datetime | string | 时间戳 |
| open | float | 开盘价 |
| high | float | 最高价 |
| low | float | 最低价 |
| close | float | 收盘价 |
| volume | int | 成交量 |
| hold | int | 持仓量 |
| update_time | datetime | 更新时间（自动添加） |
| query_symbol | string | 查询合约代码（自动添加） |
| query_period | string | 查询周期（自动添加） |

## 🔧 技术实现

**后端核心逻辑**:
```python
# 1. 参数验证
if not symbol:
    logger.error("必需提供symbol参数")
    return

# 2. 调用API
df = ak.futures_zh_minute_sina(symbol=symbol, period=period)

# 3. 数据处理
for item in data:
    item["update_time"] = datetime.now()
    item["query_symbol"] = symbol
    item["query_period"] = period
    
    # 唯一键：symbol + period + datetime
    key = {
        "query_symbol": symbol,
        "query_period": period,
        "datetime": item.get("datetime")
    }
    
    await collection.update_one(key, {"$set": item}, upsert=True)
```

**路由灵活性**:
```python
# 支持两种格式
if ":" in symbol:
    # 格式1: symbol:period
    sym, per = symbol.split(":", 1)
else:
    # 格式2: 独立参数（推荐）
    sym, per = symbol, period
```

## ✅ 验收标准完成情况

- [x] 测试用例全部通过（3/3）
- [x] 数据能够正确获取、存储和展示
- [x] 支持多种周期选择
- [x] 支持两种参数传递方式
- [x] 完整的错误处理
- [x] 日志记录完善
- [x] 复用前端组件

## 🚀 使用示例

### 1. 访问集合页面
```
http://localhost:3000/futures/collections/futures_zh_minute_sina
```

### 2. API调用示例

**方式1：独立参数（推荐）**
```bash
# 获取IF2008的1分钟K线
curl -X POST "http://localhost:8000/api/futures/collections/futures_zh_minute_sina/update?symbol=IF2008&period=1"

# 获取IF2008的5分钟K线
curl -X POST "http://localhost:8000/api/futures/collections/futures_zh_minute_sina/update?symbol=IF2008&period=5"

# 获取IF2008的15分钟K线
curl -X POST "http://localhost:8000/api/futures/collections/futures_zh_minute_sina/update?symbol=IF2008&period=15"
```

**方式2：组合格式（兼容）**
```bash
# symbol:period格式
curl -X POST "http://localhost:8000/api/futures/collections/futures_zh_minute_sina/update?symbol=IF2008:5"
```

### 3. Python调用示例
```python
import requests

# 使用独立参数
response = requests.post(
    "http://localhost:8000/api/futures/collections/futures_zh_minute_sina/update",
    params={
        "symbol": "IF2008",
        "period": "5"  # 5分钟K线
    }
)
print(response.json())

# 使用组合格式
response = requests.post(
    "http://localhost:8000/api/futures/collections/futures_zh_minute_sina/update",
    params={"symbol": "IF2008:5"}
)
print(response.json())
```

### 4. 获取不同周期的数据
```python
import requests

periods = ["1", "5", "15", "30", "60"]
symbol = "IF2008"

for period in periods:
    response = requests.post(
        "http://localhost:8000/api/futures/collections/futures_zh_minute_sina/update",
        params={"symbol": symbol, "period": period}
    )
    print(f"{period}分钟K线: {response.json()}")
```

## 📝 注意事项

1. **必需参数**: symbol参数为必需，不提供将导致更新失败
2. **合约代码格式**: 期货品种符号需要**大写**（如"IF2008"而非"if2008"）
3. **周期选择**: period支持 "1", "5", "15", "30", "60" 五种周期
4. **唯一标识**: 使用 query_symbol + query_period + datetime 组合
5. **数据量**: 不同周期数据量不同，1分钟数据量最大
6. **合约查询**: 可通过 `ak.match_main_contract(symbol="cffex")` 获取主力合约

## 🎉 总结

031号需求已完整实现，包括：
- ✅ 完整的后端数据更新逻辑
- ✅ 灵活的参数传递方式（两种格式）
- ✅ 多周期支持（1/5/15/30/60分钟）
- ✅ 复用前端Collection组件
- ✅ 完善的测试覆盖
- ✅ 详细的文档说明

**实施时间**: 约20分钟
**代码质量**: 测试通过率100%
**API灵活性**: 高（支持两种参数格式）

**创新点**:
- 路由支持多种参数传递方式
- 向后兼容性好
- RESTful风格优化

---

**进度总结**:
- ✅ 029号: futures_zh_spot（实时行情）
- ✅ 030号: futures_zh_realtime（品种行情）
- ✅ 031号: futures_zh_minute_sina（分时K线）

**下一步建议**:
继续实现032号需求：内盘-历史行情数据-东财 - futures_hist_em
