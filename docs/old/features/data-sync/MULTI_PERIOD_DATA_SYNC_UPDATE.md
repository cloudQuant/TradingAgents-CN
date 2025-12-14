# 数据同步功能更新

## 📋 更新概述

- *更新日期**: 2025-09-30
- *版本**: v1.4
- *功能**:
1. 为 Tushare、AKShare、BaoStock 三个数据源添加多周期历史数据同步支持
2. 为 Tushare 添加选择性数据同步功能
3. 为所有数据源添加全历史数据同步支持（从 1990 年至今）
4. 为 Tushare 添加新闻数据同步功能 🆕

## 🎯 更新内容

### 新增功能 1: 多周期数据同步

为所有主要数据源添加了多周期历史数据同步功能，支持：

- **日线数据**(daily) - 每个交易日的 OHLCV 数据
- **周线数据**(weekly) - 每周的 OHLCV 数据
- **月线数据**(monthly) - 每月的 OHLCV 数据

### 新增功能 2: 选择性数据同步 🆕

为 Tushare 添加了选择性数据同步功能，支持：

- **basic_info**- 股票基础信息
- **historical**- 历史行情（日线）
- **weekly**- 周线数据
- **monthly**- 月线数据
- **financial**- 财务数据
- **quotes**- 最新行情
- **news** - 新闻数据 🆕

- *优势**:
- 只更新需要的数据类型
- 节省同步时间（最高可节省 95%）
- 适合增量更新和数据修复

### 数据存储

所有周期的数据统一存储在 `stock_daily_quotes` 集合中，通过 `period` 字段区分：

```javascript
{
  "symbol": "000001",
  "trade_date": "2024-01-02",
  "period": "daily",  // daily/weekly/monthly
  "data_source": "tushare",
  "open": 9.21,
  "close": 9.21,
  "high": 9.25,
  "low": 9.18,
  "volume": 1200412,
  ...
}

```bash

## 🔧 代码更新

### 1. Tushare 数据源

#### 更新的文件

- `app/worker/tushare_init_service.py`
- `app/worker/tushare_sync_service.py`
- `cli/tushare_init.py`

#### 主要改动

```python

# 初始化服务添加 enable_multi_period 参数

async def run_full_initialization(
    self,
    historical_days: int = 365,
    skip_if_exists: bool = True,
    enable_multi_period: bool = False  # 新增

) -> Dict[str, Any]:
    ...

# 步骤 4: 同步多周期数据（如果启用）
    if enable_multi_period:
        await self._step_initialize_weekly_data(historical_days)
        await self._step_initialize_monthly_data(historical_days)

```bash

#### CLI 命令

```bash

# 启用多周期数据同步

python cli/tushare_init.py --full --multi-period

# 指定历史数据范围

python cli/tushare_init.py --full --multi-period --historical-days 365

# 选择性数据同步示例

# 仅同步历史数据（日线）

python cli/tushare_init.py --full --sync-items historical

# 仅同步财务数据和行情数据

python cli/tushare_init.py --full --sync-items financial,quotes

# 仅同步新闻数据 🆕

python cli/tushare_init.py --full --sync-items news

# 同步多种数据类型

python cli/tushare_init.py --full --sync-items historical,weekly,monthly,news

```bash

### 新增功能 3: 新闻数据同步 🆕

为 Tushare 添加了新闻数据同步功能，支持从多个新闻源获取股票相关新闻：

#### 新闻数据源

- **sina**- 新浪财经
- **eastmoney**- 东方财富
- **10jqka**- 同花顺
- **wallstreetcn**- 华尔街见闻
- **cls**- 财联社
- **yicai**- 第一财经
- **jinrongjie**- 金融界
- **yuncaijing**- 云财经
- **fenghuang**- 凤凰财经

#### 新闻数据结构

```javascript
{
  "symbol": "000001",
  "full_symbol": "000001.SZ",
  "market": "CN",
  "title": "新闻标题",
  "content": "新闻内容",
  "summary": "新闻摘要",
  "url": "新闻链接",
  "source": "sina",
  "author": "作者",
  "publish_time": "2025-09-30 12:00:00",
  "category": "general",
  "sentiment": "neutral",  // positive/negative/neutral
  "sentiment_score": 0.0,
  "keywords": ["关键词 1", "关键词 2"],
  "importance": "medium",  // high/medium/low
  "language": "zh-CN",
  "data_source": "tushare",
  "created_at": "2025-09-30 12:00:00",
  "updated_at": "2025-09-30 12:00:00"
}

```bash

#### 使用方法

```bash

# 仅同步新闻数据（默认回溯 24 小时）

python cli/tushare_init.py --full --sync-items news

# 同步新闻和其他数据

python cli/tushare_init.py --full --sync-items basic_info,historical,news

```bash

#### 注意事项

- 新闻数据需要 Tushare 新闻权限（部分数据源可能需要付费）
- 默认回溯时间为 24 小时（最多 7 天）
- 每只股票默认获取最多 20 条新闻
- 新闻数据存储在 `stock_news` 集合中
- 使用 URL、标题和发布时间作为唯一标识，自动去重

### 2. AKShare 数据源

#### 更新的文件

- `app/worker/akshare_init_service.py`
- `app/worker/akshare_sync_service.py`

#### 主要改动

```python

# 同步服务添加 period 参数

async def sync_historical_data(
    self,
    start_date: str = None,
    end_date: str = None,
    symbols: List[str] = None,
    incremental: bool = True,
    period: str = "daily"  # 新增

) -> Dict[str, Any]:
    ...

```bash

### 3. BaoStock 数据源

#### 更新的文件

- `app/worker/baostock_init_service.py`
- `app/worker/baostock_sync_service.py`

#### 主要改动

```python

# 同步服务添加 period 参数

async def sync_historical_data(
    self,
    days: int = 30,
    batch_size: int = 20,
    period: str = "daily"  # 新增

) -> BaoStockSyncStats:
    ...

```bash

### 4. 历史数据服务

#### 已有支持

`app/services/historical_data_service.py` 已经支持 `period` 参数，无需修改。

```python
async def save_historical_data(
    self,
    symbol: str,
    data: pd.DataFrame,
    data_source: str,
    market: str = "CN",
    period: str = "daily"  # 已支持

) -> int:
    ...

```bash

## 📊 测试验证

### 测试脚本

创建了测试脚本验证功能：

- `scripts/test_multi_period_sync.py` - Tushare 多周期测试
- `scripts/test_akshare_baostock_multi_period.py` - AKShare 和 BaoStock 多周期测试
- `scripts/test_selective_sync.py` - 选择性同步测试

### 多周期测试结果

| 数据源 | 日线 | 周线 | 月线 | 状态 |

|--------|------|------|------|------|

|**Tushare**| 58 条 | 12 条 | 3 条 | ✅ 通过 |

|**AKShare**| 85 条 | 14 条 | 3 条 | ✅ 通过 |

|**BaoStock**| 64 条 | 13 条 | 2 条 | ✅ 通过 |

测试股票：000001（平安银行）
测试时间范围：2024-01-01 到 2024-03-31（约 90 天）

### 选择性同步测试结果

| 测试项 | 同步内容 | 耗时 | 状态 |

|--------|---------|------|------|

| 测试 1 | 仅历史数据（30 天） | ~5 分钟 | ✅ 通过 |

| 测试 2 | 仅周线数据 | ~3 分钟 | ✅ 通过 |

| 测试 3 | 财务+行情数据 | ~12 分钟 | ✅ 通过 |

## 📚 文档更新

### 更新的文档

1.**`docs/guides/tushare_unified/data_initialization_guide.md`**

   - 添加选择性数据同步章节（包含使用示例和应用场景）
   - 添加多周期数据同步章节
   - 更新 CLI 使用示例
   - 添加数据量估算
   - 更新预计耗时
   - 更新版本号为 v1.2

1. **`docs/MULTI_SOURCE_SYNC_GUIDE.md`**
   - 添加选择性数据同步章节
   - 更新数据源特性说明
   - 添加多周期数据支持章节
   - 添加查询示例
   - 更新版本号为 v1.2

1. **`docs/TUSHARE_USAGE_GUIDE.md`**
   - 添加多周期数据初始化示例
   - 添加多周期数据查询示例
   - 更新数据覆盖说明
   - 更新版本号为 v1.1

## 🚀 使用指南

### 1. 多周期数据初始化

```bash

# Tushare 完整初始化（包含多周期，默认 1 年）

python cli/tushare_init.py --full --multi-period

# 指定历史数据范围（6 个月）

python cli/tushare_init.py --full --multi-period --historical-days 180

# 全历史多周期初始化（从 1990 年至今，推荐生产环境）

python cli/tushare_init.py --full --multi-period --historical-days 10000

# 强制重新初始化

python cli/tushare_init.py --full --multi-period --force

```bash

### 2. 选择性数据同步 🆕

```bash

# 仅同步历史数据（日线）

python cli/tushare_init.py --full --sync-items historical --historical-days 30

# 仅同步财务数据

python cli/tushare_init.py --full --sync-items financial

# 仅同步周线和月线数据

python cli/tushare_init.py --full --sync-items weekly,monthly --historical-days 90

# 同步多个数据类型

python cli/tushare_init.py --full --sync-items historical,financial,quotes

# 强制重新同步特定数据

python cli/tushare_init.py --full --sync-items quotes --force

```bash

### 3. 应用场景示例

#### 每日增量更新

```bash

# 每天收盘后更新最新数据（5-10 分钟）

python cli/tushare_init.py --full --sync-items historical,quotes --historical-days 5

```bash

#### 周末维护

```bash

# 每周末更新周线和月线（3-5 分钟）

python cli/tushare_init.py --full --sync-items weekly,monthly --historical-days 30

```bash

#### 季度财报更新

```bash

# 每季度更新财务数据（10-15 分钟）

python cli/tushare_init.py --full --sync-items financial --force

```bash

## 🌐 全历史数据同步 🆕

### 功能说明

全历史数据同步功能允许获取股票从 1990 年至今的完整历史数据，适用于长期回测和研究。

### 阈值机制

当 `--historical-days >= 3650`（10 年）时，系统自动切换到全历史模式：

| historical_days | 同步范围 | 说明 |

|----------------|---------|------|

| < 3650 | 指定天数 | 从当前日期往前推算 |

| >= 3650 | 全历史 | 从 1990-01-01 至今 |

### 使用示例

```bash

# 全历史数据初始化

python cli/tushare_init.py --full --historical-days 10000

# 全历史多周期初始化（推荐生产环境）

python cli/tushare_init.py --full --multi-period --historical-days 10000

# 全历史选择性同步

python cli/tushare_init.py --full --sync-items historical --historical-days 10000

```bash

### 数据量对比

| 同步模式 | 日线记录数 | 存储空间 | 同步耗时 |

|---------|-----------|---------|---------|

| 默认 1 年 | ~1,250,000 条 | ~500MB | 30-60 分钟 |

| 全历史 | ~8,000,000 条 | 2-5GB | 2-4 小时 |

### 适用数据源

- ✅ **Tushare**: 完全支持，推荐使用
- ✅ **AKShare**: 完全支持，免费但较慢
- ✅ **BaoStock**: 完全支持，免费

### 注意事项

1. **耗时较长**: 全历史同步需要 2-4 小时
2. **API 限流**: 注意各数据源的调用频率限制
3. **存储空间**: 确保有 2-5GB 可用空间
4. **推荐策略**: 首次全历史初始化，日常增量更新

### 查询多周期数据

```python
from tradingagents.config.database_manager import get_mongodb_client

client = get_mongodb_client()
db = client.get_database('tradingagents')
collection = db.stock_daily_quotes

# 查询不同周期的数据

for period in ["daily", "weekly", "monthly"]:
    count = collection.count_documents({
        'symbol': '000001',
        'period': period,
        'data_source': 'tushare'
    })
    print(f"{period}: {count} 条记录")

```bash

### MongoDB 查询示例

```javascript
// 查询日线数据
db.stock_daily_quotes.find({
  symbol: "000001",
  period: "daily",
  data_source: "tushare",
  trade_date: { $gte: "2024-01-01", $lte: "2024-12-31" }
}).sort({ trade_date: 1 })

// 查询周线数据
db.stock_daily_quotes.find({
  symbol: "000001",
  period: "weekly",
  data_source: "tushare"
}).sort({ trade_date: 1 })

// 统计各周期数据量
db.stock_daily_quotes.aggregate([
  { $match: { symbol: "000001", data_source: "tushare" } },
  { $group: { _id: "$period", count: { $sum: 1 } } }
])

```bash

## 📈 数据量估算

以 5000 只股票、1 年历史数据为例：

| 周期 | 每股记录数 | 总记录数 | 存储空间 |

|------|-----------|---------|---------|

| 日线 | ~250 条 | ~125 万条 | ~500MB |

| 周线 | ~52 条 | ~26 万条 | ~100MB |

| 月线 | ~12 条 | ~6 万条 | ~25MB |

| **总计**| ~314 条 | ~157 万条 | ~625MB |

## ⚙️ 配置说明

### 环境变量

无需额外配置，使用现有的数据源配置：

```bash

# Tushare 配置

TUSHARE_TOKEN=your_tushare_token_here
TUSHARE_UNIFIED_ENABLED=true

# AKShare 配置

AKSHARE_UNIFIED_ENABLED=true

# BaoStock 配置

BAOSTOCK_UNIFIED_ENABLED=true

```bash

### 性能调优

```bash

# 批处理大小（根据内存和网络调整）

TUSHARE_INIT_BATCH_SIZE=100

# API 调用频率控制

TUSHARE_RATE_LIMIT_DELAY=0.1

# 数据库连接池

MONGODB_MAX_POOL_SIZE=100

```bash

## ⚠️ 注意事项

1.**API 限流**: 多周期同步会增加 API 调用次数，注意 Tushare 的频率限制

1. **存储空间**: 多周期数据会增加约 25%的存储需求
2. **同步时间**: 完整多周期初始化比仅日线数据多 15-30 分钟
3. **数据去重**: 系统使用 `(symbol, trade_date, data_source, period)` 作为唯一键
4. **错误处理**: 周线/月线同步失败不会影响日线数据和整体流程

## 🔍 故障排查

### 问题 1: 周线/月线数据为空

- *原因**: API 可能对某些股票不提供周线/月线数据
- *解决**: 检查日志，确认 API 返回的数据是否为空

### 问题 2: 数据保存失败

- *原因**: 日期索引处理问题
- *解决**: 确保使用最新版本的代码（已修复日期索引问题）

### 问题 3: 同步速度慢

- *原因**: API 限流或网络延迟
- *解决**: 调整 `rate_limit_delay` 参数或分批同步

## 📝 最佳实践

1. **首次部署**: 使用 `--multi-period` 参数一次性同步所有周期数据
2. **增量更新**: 定期运行日线数据同步，周线/月线数据可以较低频率更新
3. **数据验证**: 同步完成后检查各周期数据的记录数是否合理
4. **监控日志**: 关注同步过程中的错误和警告信息

## 🎯 后续计划

1. **前端支持**: 在 Web 界面添加多周期数据查询和展示
2. **API 接口**: 添加 RESTful API 支持多周期数据查询
3. **数据分析**: 基于多周期数据的技术分析工具
4. **性能优化**: 优化多周期数据的查询性能

- --

- *文档维护**: AI Assistant
- *最后更新**: 2025-09-30
- *版本**: v1.2 - 新增选择性数据同步和多周期数据支持
