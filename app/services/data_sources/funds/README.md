# 基金数据模块重构说明

## 目录结构

```
funds/
├── providers/          # 数据提供者（调用AKShare获取原始数据）
│   ├── __init__.py
│   ├── fund_name_em_provider.py
│   ├── fund_etf_spot_em_provider.py
│   └── ...（共31个provider）
├── services/           # 数据服务（数据库读写操作）
│   ├── __init__.py
│   ├── fund_name_em_service.py
│   ├── fund_etf_spot_em_service.py
│   └── ...（共31个service）
└── README.md
```

## 架构说明

### Provider层
- **职责**：调用AKShare API获取原始数据
- **特点**：纯数据获取，不涉及数据库操作
- **方法**：
  - `fetch_data(**kwargs)`: 获取数据并返回DataFrame
  - `get_field_info()`: 返回字段信息

### Service层
- **职责**：数据库CRUD操作
- **特点**：依赖Provider获取数据，负责存储和查询
- **方法**：
  - `get_overview()`: 获取数据概览
  - `get_data()`: 查询数据
  - `refresh_data()`: 刷新数据（调用Provider并保存）
  - `clear_data()`: 清空数据

## 使用示例

### 1. 直接使用Service

```python
from app.core.database import get_mongo_db
from app.services.data_sources.funds.services.fund_name_em_service import FundNameEmService

# 初始化服务
db = get_mongo_db()
service = FundNameEmService(db)

# 刷新数据
result = await service.refresh_data()
print(f"插入了 {result['inserted']} 条数据")

# 获取概览
overview = await service.get_overview()
print(f"总数据量: {overview['total_count']}")

# 查询数据
data = await service.get_data(skip=0, limit=100)
print(f"查询到 {len(data['data'])} 条数据")
```

### 2. 使用统一的刷新服务

```python
from app.services.fund_refresh_service_v2 import FundRefreshServiceV2

# 初始化刷新服务
refresh_service = FundRefreshServiceV2()

# 刷新指定集合
result = await refresh_service.refresh_collection(
    collection_name="fund_name_em",
    task_id="task_001",
    params={}
)
```

### 3. 仅使用Provider获取数据（不保存）

```python
from app.services.data_sources.funds.providers.fund_name_em_provider import FundNameEmProvider

# 初始化Provider
provider = FundNameEmProvider()

# 获取数据
df = provider.fetch_data()
print(f"获取到 {len(df)} 条数据")
```

## 已支持的数据集合

共31个数据集合：

### 基本信息类
- `fund_name_em`: 基金基本信息-东财
- `fund_basic_info`: 基金基本信息-雪球
- `fund_info_index_em`: 指数型基金基本信息-东财
- `fund_purchase_status`: 基金申购状态-东财

### 实时行情类
- `fund_etf_spot_em`: ETF实时行情-东财
- `fund_etf_spot_ths`: ETF实时行情-同花顺
- `fund_lof_spot_em`: LOF实时行情-东财
- `fund_spot_sina`: 基金实时行情-新浪
- `fund_open_fund_daily_em`: 开放式基金实时行情-东财
- `fund_money_fund_daily_em`: 货币型基金实时行情-东财
- `fund_etf_fund_daily_em`: 场内交易基金实时数据-东财

### 历史行情类
- `fund_etf_hist_min_em`: ETF分时行情-东财
- `fund_lof_hist_min_em`: LOF分时行情-东财
- `fund_etf_hist_em`: ETF历史行情-东财
- `fund_lof_hist_em`: LOF历史行情-东财
- `fund_hist_sina`: 基金历史行情-新浪
- `fund_open_fund_info_em`: 开放式基金历史行情-东财
- `fund_money_fund_info_em`: 货币型基金历史行情-东财
- `fund_hk_hist_em`: 香港基金历史数据-东财
- `fund_etf_fund_info_em`: 场内交易基金历史行情-东财

### 分红拆分类
- `fund_etf_dividend_sina`: 基金累计分红-新浪
- `fund_fh_em`: 基金分红-东财
- `fund_cf_em`: 基金拆分-东财

### 排行榜类
- `fund_fh_rank_em`: 基金分红排行-东财
- `fund_open_fund_rank_em`: 开放式基金排行-东财
- `fund_exchange_rank_em`: 场内基金排行-东财
- `fund_money_rank_em`: 货币型基金排行-东财

## 迁移指南

### 从旧版本迁移

旧代码：
```python
from app.services.fund_refresh_service import FundRefreshService

service = FundRefreshService(db)
await service._refresh_fund_name_em(task_id, params)
```

新代码：
```python
from app.services.fund_refresh_service_v2 import FundRefreshServiceV2

service = FundRefreshServiceV2(db)
await service.refresh_collection("fund_name_em", task_id, params)
```

### 路由层迁移

旧代码：
```python
from app.services.fund_refresh_service import FundRefreshService
from app.services.fund_data_service import FundDataService

refresh_service = FundRefreshService(db)
data_service = FundDataService(db)
```

新代码：
```python
from app.services.fund_refresh_service_v2 import FundRefreshServiceV2
from app.services.fund_data_service_v2 import FundDataServiceV2

refresh_service = FundRefreshServiceV2(db)
data_service = FundDataServiceV2(db)
```

## 优势

1. **模块化**：每个数据集合都有独立的provider和service
2. **可维护性**：代码结构清晰，易于定位和修改
3. **可扩展性**：添加新数据源只需添加对应的provider和service
4. **可测试性**：每个模块都可以独立测试
5. **统一接口**：所有service都有相同的方法签名

## 开发指南

### 添加新的数据集合

1. 创建Provider类：
```python
# providers/new_fund_provider.py
class NewFundProvider:
    def __init__(self):
        self.collection_name = "new_fund_collection"
        self.display_name = "新基金数据"
    
    def fetch_data(self, **kwargs):
        # 调用AKShare API
        import akshare as ak
        df = ak.new_fund_api(**kwargs)
        df['scraped_at'] = datetime.now()
        return df
```

2. 创建Service类：
```python
# services/new_fund_service.py
class NewFundService:
    def __init__(self, db):
        self.db = db
        self.collection = db.funds.new_fund_collection
        self.provider = NewFundProvider()
    
    # 实现标准方法：get_overview, get_data, refresh_data, clear_data
```

3. 在FundRefreshServiceV2中注册：
```python
self.services = {
    ...
    "new_fund_collection": NewFundService(self.db),
}
```

## 测试

运行测试：
```bash
python tests/test_fund_services_v2.py
```

## 注意事项

1. 所有Provider的`fetch_data`方法都应该添加`scraped_at`字段
2. Service的数据库集合应该统一放在`funds`数据库下
3. 错误处理应该在Provider和Service层都有
4. 建议使用进度回调来跟踪长时间运行的任务
