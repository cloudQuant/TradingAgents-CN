# K 线数据来源说明

## 📊 接口信息

- *接口路径**: `GET /api/stocks/{code}/kline`

- *示例请求**: `GET /api/stocks/600036/kline?period=day&limit=200&adj=none`

- *参数说明**:
- `code`: 股票代码（6 位）
- `period`: K 线周期（day/week/month/5m/15m/30m/60m）
- `limit`: 返回数据条数（默认 120）
- `adj`: 复权方式（none/qfq/hfq）

- --

## 🗄️ 数据来源

### 1. MongoDB 集合（优先级最高）

- *集合名称**: `stock_daily_quotes`

- *查询逻辑**:

```python

# 文件: tradingagents/dataflows/cache/mongodb_cache_adapter.py (第 87 行)

collection = self.db.stock_daily_quotes

# 查询条件

query = {
    "symbol": "600036",      # 6 位股票代码
    "period": "daily",       # 周期（daily/weekly/monthly）
    "trade_date": {          # 日期范围
        "$gte": start_date,
        "$lte": end_date
    }
}

# 排序

cursor = collection.find(query, {"_id": 0}).sort("trade_date", 1)

```bash

- *周期映射**:

| 前端参数 | MongoDB 字段值 |

|---------|--------------|

| day     | daily        |

| week    | weekly       |

| month   | monthly      |

| 5m      | 5min         |

| 15m     | 15min        |

| 30m     | 30min        |

| 60m     | 60min        |

- *数据字段**:

```json
{
  "symbol": "600036",
  "period": "daily",
  "trade_date": "20251016",
  "open": 45.23,
  "high": 46.78,
  "low": 45.01,
  "close": 46.50,
  "volume": 12345678,
  "amount": 567890123.45
}

```bash

- --

### 2. 外部 API（降级方案）

如果 MongoDB 中没有数据，系统会自动降级到外部 API：

- *降级顺序**:
1. **Tushare**(如果已配置 `TUSHARE_TOKEN`)

2.**AKShare**(免费，无需 Token)
3.**BaoStock** (免费，无需 Token)

- *实现代码**:

```python

# 文件: app/routers/stocks.py (第 242-259 行)

if not items:
    logger.info(f"📡 MongoDB 无数据，降级到外部 API")
    try:
        import asyncio
        from app.services.data_sources.manager import DataSourceManager

        mgr = DataSourceManager()

# 添加 10 秒超时保护
        items, source = await asyncio.wait_for(
            asyncio.to_thread(mgr.get_kline_with_fallback, code_padded, period, limit, adj_norm),
            timeout=10.0
        )
    except asyncio.TimeoutError:
        logger.error(f"❌ 外部 API 获取 K 线超时（10 秒）")
        raise HTTPException(status_code=504, detail="获取 K 线数据超时，请稍后重试")

```bash

- --

## 📈 数据流程图

```bash
前端请求 /api/stocks/600036/kline?period=day&limit=200
         ↓
app/routers/stocks.py (第 180 行)
         ↓
    ┌────┴────┐
    ↓         ↓
MongoDB    外部 API
(优先)     (降级)
    ↓         ↓
stock_daily_quotes
    ↓
查询条件:

- symbol: "600036"
- period: "daily"
- trade_date: 范围查询

    ↓
返回 DataFrame
    ↓
转换为 JSON 格式
    ↓
返回给前端

```bash

- --

## 🔍 如何验证数据来源

### 方法 1：查看后端日志

```bash

# 从 MongoDB 获取

2025-10-17 10:31:26 | app.routers.stocks | INFO | 🔍 尝试从 MongoDB 获取 K 线数据: 600036, period=day (MongoDB: daily), limit=200

2025-10-17 10:31:26 | app.routers.stocks | INFO | ✅ 从 MongoDB 获取到 200 条 K 线数据

# 从外部 API 获取

2025-10-17 10:31:26 | app.routers.stocks | INFO | 📡 MongoDB 无数据，降级到外部 API

2025-10-17 10:31:27 | app.services.data_sources.manager | INFO | Trying to fetch kline from akshare

```bash

### 方法 2：查看接口返回的 `source` 字段

```json
{
  "success": true,
  "data": {
    "code": "600036",
    "period": "day",
    "limit": 200,
    "adj": "none",
    "source": "mongodb",  // 数据来源：mongodb/tushare/akshare/baostock
    "items": [...]
  }
}

```bash

### 方法 3：直接查询 MongoDB

```bash

# 连接 MongoDB

mongo mongodb://admin:tradingagents123@localhost:27017/tradingagents

# 查询数据

db.stock_daily_quotes.find({
  "symbol": "600036",
  "period": "daily"
}).sort({"trade_date": -1}).limit(5)

```bash

- --

## 📊 MongoDB 集合结构

### stock_daily_quotes 集合

- *用途**: 存储多周期 K 线数据（日线、周线、月线、分钟线）

- *索引**:

```javascript
// 复合索引（查询优化）
db.stock_daily_quotes.createIndex({ "symbol": 1, "period": 1, "trade_date": 1 })

// 单字段索引
db.stock_daily_quotes.createIndex({ "symbol": 1 })
db.stock_daily_quotes.createIndex({ "trade_date": -1 })

```bash

- *数据示例**:

```json
{
  "_id": ObjectId("..."),
  "symbol": "600036",
  "period": "daily",
  "trade_date": "20251016",
  "open": 45.23,
  "high": 46.78,
  "low": 45.01,
  "close": 46.50,
  "volume": 12345678,
  "amount": 567890123.45,
  "pct_chg": 2.35,
  "turnover_rate": 1.23,
  "created_at": ISODate("2025-10-17T02:31:26.000Z"),
  "updated_at": ISODate("2025-10-17T02:31:26.000Z")
}

```bash

- *数据来源**:
- 定时任务同步（每日 16:00 后）
- 手动触发同步
- 实时行情入库（30 秒间隔）

- --

## 🔄 数据同步机制

### 1. 定时任务同步

- *配置文件**: `.env`

```bash

# AKShare 历史数据同步

SYNC_AKSHARE_HISTORICAL_ENABLED=true
SYNC_AKSHARE_HISTORICAL_CRON=0 17 * *1-5  # 每个交易日 17:00

# BaoStock 日 K 线同步

SYNC_BAOSTOCK_DAILY_QUOTES_ENABLED=true
SYNC_BAOSTOCK_DAILY_QUOTES_CRON=0 16* *1-5  # 每个交易日 16:00

```bash

- *同步逻辑**:
1. 从外部 API 获取最新数据
2. 标准化数据格式
3. 写入 `stock_daily_quotes` 集合
4. 更新 `sync_status` 集合记录同步状态

### 2. 手动触发同步

- *接口**: `POST /api/multi-source-sync/historical`

- *请求示例**:

```bash
curl -X POST "<http://localhost:8000/api/multi-source-sync/historical"> \

  - H "Authorization: Bearer YOUR_TOKEN" \
  - H "Content-Type: application/json" \
  - d '{

    "source": "akshare",
    "symbols": ["600036", "000001"],
    "start_date": "2024-01-01",
    "end_date": "2025-10-17"
  }'

```bash

- --

## 🛠️ 故障排查

### 问题 1：K 线数据为空

- *可能原因**:
1. MongoDB 中没有该股票的数据
2. 外部 API 请求失败
3. 股票代码不存在

- *解决方案**:

```bash

# 1. 检查 MongoDB 数据

db.stock_daily_quotes.find({"symbol": "600036"}).count()

# 2. 手动触发同步

curl -X POST "<http://localhost:8000/api/multi-source-sync/historical"> \

  - H "Authorization: Bearer YOUR_TOKEN" \
  - d '{"source": "akshare", "symbols": ["600036"]}'

# 3. 检查后端日志

tail -f logs/app.log | grep "600036"

```bash

### 问题 2：数据不是最新的

- *可能原因**:
1. 定时任务未执行
2. 同步任务失败
3. 非交易时间（无新数据）

- *解决方案**:

```bash

# 1. 检查同步状态

curl "<http://localhost:8000/api/sync/status"> \

  - H "Authorization: Bearer YOUR_TOKEN"

# 2. 手动触发同步

curl -X POST "<http://localhost:8000/api/multi-source-sync/historical"> \

  - H "Authorization: Bearer YOUR_TOKEN"

# 3. 检查定时任务状态

curl "<http://localhost:8000/api/scheduler/jobs"> \

  - H "Authorization: Bearer YOUR_TOKEN"

```bash

### 问题 3：接口响应慢

- *可能原因**:
1. MongoDB 查询慢（缺少索引）
2. 外部 API 响应慢
3. 数据量过大

- *解决方案**:

```bash

# 1. 检查索引

db.stock_daily_quotes.getIndexes()

# 2. 创建索引（如果缺失）

db.stock_daily_quotes.createIndex({ "symbol": 1, "period": 1, "trade_date": 1 })

# 3. 减少 limit 参数

# 从 limit=200 改为 limit=120

# 4. 检查慢查询日志

db.setProfilingLevel(2)
db.system.profile.find().sort({ts: -1}).limit(5)

```bash

- --

## 📚 相关文件

### 后端代码

- `app/routers/stocks.py` (第 180-288 行) - K 线接口实现
- `tradingagents/dataflows/cache/mongodb_cache_adapter.py` (第 70-114 行) - MongoDB 缓存适配器
- `app/services/data_sources/manager.py` - 数据源管理器

### 配置文件

- `.env` - 环境配置
- `config/settings.json` - 系统配置

### 数据库脚本

- `scripts/mongo-init.js` - MongoDB 初始化脚本
- `scripts/setup/init_database.py` - 数据库初始化脚本

- --

## 💡 最佳实践

### 1. 数据预热

在系统启动后，建议预先同步常用股票的历史数据：

```bash

# 同步沪深 300 成分股

curl -X POST "<http://localhost:8000/api/multi-source-sync/historical"> \

  - H "Authorization: Bearer YOUR_TOKEN" \
  - d '{

    "source": "akshare",
    "symbols": ["600036", "000001", ...],
    "start_date": "2024-01-01"
  }'

```bash

### 2. 定期清理旧数据

```javascript
// 删除 1 年前的分钟线数据（节省存储空间）
db.stock_daily_quotes.deleteMany({
  "period": { $in: ["5min", "15min", "30min", "60min"] },
  "trade_date": { $lt: "20240101" }
})

```bash

### 3. 监控数据质量

```javascript
// 检查数据完整性
db.stock_daily_quotes.aggregate([
  { $match: { "period": "daily" } },
  { $group: {
      _id: "$symbol",
      count: { $sum: 1 },
      latest: { $max: "$trade_date" }
  }},
  { $match: { count: { $lt: 200 } } }  // 找出数据不足 200 条的股票
])

```bash

- --

## 🎯 总结

- *K 线数据获取流程**:
1. ✅ **优先**: 从 MongoDB `stock_daily_quotes` 集合获取
2. ⚠️ **降级**: 如果 MongoDB 无数据，从外部 API 获取（Tushare > AKShare > BaoStock）
3. 🔄 **同步**: 定时任务每日同步最新数据到 MongoDB
4. 📊 **返回**: 接口返回 JSON 格式数据，包含 `source` 字段标识数据来源

- *优势**:
- 🚀 **快速**: MongoDB 查询速度快，响应时间 < 100ms
- 🔄 **可靠**: 多数据源降级，保证数据可用性
- 💾 **缓存**: 减少外部 API 调用，节省配额
- 📈 **完整**: 支持多周期（日/周/月/分钟线）
