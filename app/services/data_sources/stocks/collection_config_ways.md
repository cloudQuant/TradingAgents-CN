# 股票集合开发完整指南

以 `stock_zh_a_spot_em`（沪深京A股实时行情）为例，记录集合页面涉及的所有文件、函数和配置。

---

## 1. 文件清单

### 1.1 后端文件

| 文件路径 | 职责 | 关键函数/类 |
|---------|------|------------|
| `app/routers/stocks.py` | API路由定义 | `list_stock_collections()`, `get_stock_collection_data()`, `refresh_stock_collection()`, `get_refresh_status()` |
| `app/services/stock_refresh_service.py` | 刷新服务调度 | `StockRefreshService.refresh_collection()` |
| `app/services/data_sources/stocks/services/{collection}_service.py` | 业务逻辑 | `update_single_data()`, `update_batch_data()`, `get_overview()`, `get_data()` |
| `app/services/data_sources/stocks/providers/{collection}_provider.py` | 数据获取 | `fetch_data()` |
| `app/config/stock_update_config.py` | 更新配置 | `STOCK_UPDATE_CONFIGS["{collection}"]` |
| `app/utils/task_manager.py` | 任务状态 | `TaskManager.create_task()`, `update_progress()`, `complete_task()`, `fail_task()` |
| `app/services/database/control_mongodb.py` | 数据去重 | `ControlMongodb.save_dataframe_to_collection()` |

### 1.2 前端文件

| 文件路径 | 职责 | 关键函数/变量 |
|---------|------|--------------|
| `frontend/src/views/Stocks/Collection.vue` | 集合页面 | `handleBatchUpdate()`, `pollBatchTaskStatus()`, `loadData()` |
| `frontend/src/api/stocks.ts` | API调用 | `refreshCollectionData()`, `getRefreshTaskStatus()` |

---

## 2. API 接口

### 2.1 获取集合列表
```
GET /api/stocks/collections
Response: { success: true, data: [{ name, display_name, description, route, fields }] }
```

### 2.2 获取集合数据
```
GET /api/stocks/collections/{collection_name}/data?page=1&page_size=50
Response: { success: true, data: { items, total, page, page_size } }
```

### 2.3 刷新数据
```
POST /api/stocks/collections/{collection_name}/refresh
Body: { update_type: 'batch', symbol?: string, date?: string, concurrency?: number }
Response: { success: true, data: { task_id } }
```

### 2.4 查询任务状态
```
GET /api/stocks/collections/{collection_name}/refresh/status/{task_id}
Response: { success: true, data: { status, progress, total, message, result } }
```

---

## 3. 后端核心代码

### 3.1 路由层 - `app/routers/stocks.py`

```python
@router.post("/collections/{collection_name}/refresh")
async def refresh_stock_collection(
    collection_name: str,
    background_tasks: BackgroundTasks,
    params: Dict[str, Any] = Body(default={}),
    current_user: dict = Depends(get_current_user),
):
    task_id = str(uuid.uuid4())
    task_manager = get_task_manager()
    task_manager.create_task(task_id, f"刷新{collection_name}")
    
    refresh_service = StockRefreshService()
    background_tasks.add_task(
        refresh_service.refresh_collection,
        collection_name,
        task_id,
        params
    )
    
    return ok({"task_id": task_id, "message": "刷新任务已启动"})
```

### 3.2 刷新服务 - `app/services/stock_refresh_service.py`

```python
class StockRefreshService:
    # 前端专用参数，不传给 akshare
    FRONTEND_ONLY_PARAMS = {'batch', 'batch_update', 'update_type', 'concurrency', ...}
    
    def __init__(self, db=None):
        self.db = db if db is not None else get_mongo_db()
        self.task_manager = get_task_manager()
        
        # 初始化所有服务
        self.services = {
            "stock_zh_a_spot_em": StockZhASpotEmService(self.db),
            # ... 其他服务
        }
    
    async def refresh_collection(self, collection_name: str, task_id: str, params: Dict = None):
        # 判断批量/单条更新
        is_batch = params.get("update_type") == "batch" if params else False
        
        # 过滤参数
        api_params = {k: v for k, v in params.items() if k not in self.FRONTEND_ONLY_PARAMS}
        
        # 调用对应方法
        service = self.services[collection_name]
        if is_batch and hasattr(service, "update_batch_data"):
            result = await service.update_batch_data(task_id=task_id, **api_params)
        else:
            result = await service.update_single_data(**api_params)
            if result.get("success"):
                self.task_manager.complete_task(task_id)
            else:
                self.task_manager.fail_task(task_id, result.get("message"))
```

### 3.3 Service层 - `stock_zh_a_spot_em_service.py`

```python
class StockZhASpotEmService:
    def __init__(self, db):
        self.db = db
        self.collection = db["stock_zh_a_spot_em"]
        self.provider = StockZhASpotEmProvider()
    
    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """单条/全量更新"""
        df = self.provider.fetch_data(**kwargs)
        
        unique_keys = ["代码", "日期"]  # 根据实际数据设置
        control_db = ControlMongodb(self.collection, unique_keys)
        result = await control_db.save_dataframe_to_collection(df, extra_fields={
            "数据源": "akshare",
            "接口名称": "stock_zh_a_spot_em",
            "更新时间": datetime.now()
        })
        return result
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """批量更新（适用于需要遍历参数的集合）"""
        task_manager = get_task_manager() if task_id else None
        concurrency = int(kwargs.get("concurrency", 3))
        
        # 1. 获取待更新项目列表
        items = await self._get_items_to_update(**kwargs)
        
        # 2. 并发执行
        semaphore = asyncio.Semaphore(concurrency)
        async def fetch_and_save(item):
            async with semaphore:
                df = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: self.provider.fetch_data(**item)
                )
                # 保存数据...
                # 更新进度...
        
        await asyncio.gather(*[fetch_and_save(item) for item in items])
        
        # 3. 完成任务
        task_manager.complete_task(task_id, result={...}, message="完成")
    
    async def get_overview(self) -> Dict[str, Any]:
        """获取数据概览"""
        total = await self.collection.count_documents({})
        latest = await self.collection.find_one(sort=[("更新时间", -1)])
        return {
            "total_count": total,
            "latest_update": latest.get("更新时间") if latest else None
        }
    
    async def get_data(self, skip=0, limit=100, filters=None) -> Dict[str, Any]:
        """获取分页数据"""
        query = filters or {}
        cursor = self.collection.find(query).skip(skip).limit(limit)
        items = await cursor.to_list(length=limit)
        total = await self.collection.count_documents(query)
        return {"items": items, "total": total, "skip": skip, "limit": limit}
```

### 3.4 Provider层 - `stock_zh_a_spot_em_provider.py`

```python
import akshare as ak
import pandas as pd
from datetime import datetime

class StockZhASpotEmProvider:
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """获取沪深京A股实时行情数据"""
        df = ak.stock_zh_a_spot_em()
        
        if df is not None and not df.empty:
            df['更新时间'] = datetime.now()
        
        return df
```

---

## 4. 配置文件

### 4.1 更新配置 - `app/config/stock_update_config.py`

```python
STOCK_UPDATE_CONFIGS = {
    # 无参数的集合 - 只有批量更新
    "stock_zh_a_spot_em": {
        "display_name": "沪深京A股实时行情",
        "update_description": "获取沪深京A股实时行情数据",
        "single_update": {
            "enabled": False,
            "description": "",
            "params": []
        },
        "batch_update": {
            "enabled": True,
            "description": "一次性获取所有A股实时行情",
            "params": []
        }
    },
    
    # 需要股票代码参数的集合
    "stock_zh_a_hist": {
        "display_name": "A股历史行情",
        "update_description": "获取A股历史K线数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个股票的历史行情",
            "params": [
                {"name": "symbol", "label": "股票代码", "type": "text", "required": True},
                {"name": "period", "label": "周期", "type": "select", "default": "daily",
                 "options": [
                     {"label": "日线", "value": "daily"},
                     {"label": "周线", "value": "weekly"},
                     {"label": "月线", "value": "monthly"}
                 ]},
                {"name": "start_date", "label": "开始日期", "type": "text", "placeholder": "20200101"},
                {"name": "end_date", "label": "结束日期", "type": "text", "placeholder": "20241231"}
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有股票的历史行情",
            "params": [
                {"name": "period", "label": "周期", "type": "select", "default": "daily"},
                {"name": "concurrency", "label": "并发数", "type": "number", "default": 3, "min": 1, "max": 10}
            ]
        }
    },
    
    # 需要日期参数的集合
    "stock_zt_pool_em": {
        "display_name": "涨停股池",
        "update_description": "获取东方财富涨停股池数据",
        "single_update": {
            "enabled": True,
            "description": "获取指定日期的涨停股池",
            "params": [
                {"name": "date", "label": "日期", "type": "text", "placeholder": "20241125", "required": False}
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "获取最新涨停股池数据",
            "params": []
        }
    }
}
```

---

## 5. 数据流向图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              前端 Collection.vue                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  点击"批量更新" → handleBatchUpdate() → refreshCollectionData()              │
│                                           ↓                                  │
│                                     返回 task_id                             │
│                                           ↓                                  │
│  pollBatchTaskStatus() ← 轮询 ← getRefreshTaskStatus()                      │
│         ↓                                                                    │
│  更新 progressPercentage / progressMessage                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                       ↑ ↓ API
┌─────────────────────────────────────────────────────────────────────────────┐
│                              后端路由层 stocks.py                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  POST /refresh → refresh_stock_collection()                                  │
│         ↓                                                                    │
│  TaskManager.create_task() → 返回 task_id                                    │
│         ↓                                                                    │
│  background_tasks.add_task(do_refresh)                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                       ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                          刷新服务 StockRefreshService                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  refresh_collection()                                                        │
│         ↓                                                                    │
│  判断 update_type == 'batch' ?                                               │
│    是 → service.update_batch_data(task_id=task_id, ...)                     │
│    否 → service.update_single_data(...)                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                       ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Service层 StockZhASpotEmService                       │
├─────────────────────────────────────────────────────────────────────────────┤
│  update_batch_data()                                                         │
│    1. provider.fetch_data() 获取数据                                         │
│    2. ControlMongodb.save_dataframe_to_collection() 保存数据                 │
│    3. task_manager.update_progress() 更新进度                                │
│    4. task_manager.complete_task() 完成                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                       ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Provider层 StockZhASpotEmProvider                       │
├─────────────────────────────────────────────────────────────────────────────┤
│  fetch_data()                                                                │
│         ↓                                                                    │
│  ak.stock_zh_a_spot_em() → DataFrame                                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. 集合分类

### 6.1 无参数集合（批量获取全部数据）
- `stock_zh_a_spot_em` - 沪深京A股实时行情
- `stock_sh_a_spot_em` - 沪A股实时行情
- `stock_sz_a_spot_em` - 深A股实时行情
- `stock_hk_spot_em` - 港股实时行情
- `stock_us_spot_em` - 美股实时行情
- `stock_sse_summary` - 上证交易所数据总貌
- `stock_board_industry_name_em` - 行业板块列表

### 6.2 需要股票代码参数的集合
- `stock_zh_a_hist` - A股历史行情
- `stock_individual_info_em` - 个股信息
- `stock_financial_analysis_indicator` - 财务指标
- `stock_gdfx_top_10_em` - 十大股东

### 6.3 需要日期参数的集合
- `stock_zt_pool_em` - 涨停股池
- `stock_szse_summary` - 深证交易所统计
- `stock_lhb_detail_em` - 龙虎榜详情

### 6.4 需要多个参数的集合
- `stock_board_industry_hist_em` - 行业板块历史行情（symbol + period）
- `stock_hsgt_hist_em` - 沪深港通历史数据（symbol + indicator）

---

## 7. 新增集合步骤

### 7.1 后端步骤

1. **创建 Provider** - `providers/{collection_name}_provider.py`
   ```python
   class XxxProvider:
       def fetch_data(self, **kwargs) -> pd.DataFrame:
           # 调用 akshare 获取数据
           pass
   ```

2. **创建 Service** - `services/{collection_name}_service.py`
   ```python
   class XxxService:
       async def update_single_data(self, **kwargs): ...
       async def update_batch_data(self, task_id=None, **kwargs): ...
       async def get_overview(self): ...
       async def get_data(self, skip=0, limit=100, filters=None): ...
   ```

3. **注册 Service** - `app/services/stock_refresh_service.py`
   ```python
   self.services = {
       "xxx": XxxService(self.db),
       ...
   }
   ```

4. **添加集合定义** - `app/routers/stocks.py` 的 `list_stock_collections()`

5. **添加更新配置** - `app/config/stock_update_config.py`

### 7.2 检查清单

- [ ] Provider 的 `fetch_data` 正确获取参数
- [ ] Service 的 `update_batch_data` 接收 `task_id` 参数
- [ ] Service 使用 `ControlMongodb` 处理数据去重
- [ ] Service 调用 `task_manager.update_progress()` 更新进度
- [ ] Service 调用 `task_manager.complete_task()` 传递 result
- [ ] `stock_update_config.py` 配置了 `single_update` 和 `batch_update`
- [ ] `StockRefreshService.services` 字典中注册了新 Service

---

## 8. 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 缺少必须参数 | 未从 kwargs 获取 | `kwargs.get("symbol")` |
| 进度条不更新 | 设置了错误的状态变量 | 使用 `batchUpdating.value` |
| 任务状态重复设置 | service 和 refresh_collection 都调用 complete_task | 批量更新由 service 管理状态 |
| 数据重复 | 未使用 unique_keys | 使用 ControlMongodb |
| API限流 | 并发数过高 | 降低 concurrency 参数 |

---

**更新日期**：2025-11-26  
**集合总数**：380 个（100% 覆盖率）

---

## 9. 重构完成摘要

### 9.1 已完成的文件

| 类型 | 数量 | 路径 |
|-----|------|------|
| Provider | 380 | `app/services/data_sources/stocks/providers/` |
| Service | 380 | `app/services/data_sources/stocks/services/` |
| 配置文件 | 1 | `app/config/stock_update_config.py` |
| 服务工厂 | 1 | `app/services/data_sources/stocks/service_factory.py` |
| 刷新服务 | 1 | `app/services/stock_refresh_service.py` |

### 9.2 架构说明

```
app/
├── config/
│   └── stock_update_config.py      # 更新参数配置（58个显式配置）
├── services/
│   ├── stock_refresh_service.py    # 刷新服务（动态加载）
│   └── data_sources/
│       └── stocks/
│           ├── service_factory.py  # 服务工厂（动态加载所有服务）
│           ├── collection_config_ways.md  # 本文档
│           ├── providers/          # 380 个独立 Provider
│           │   └── {collection}_provider.py
│           └── services/           # 380 个独立 Service
│               └── {collection}_service.py
```

**架构特点**：
- 每个 Provider/Service 是独立实现，不使用继承
- 服务工厂动态扫描加载所有服务类
- 服务统一接口：`refresh_data()`, `get_overview()`, `get_data()`, `clear_data()`

### 9.3 使用方式

```python
# 在路由中使用
from app.services.stock_refresh_service import StockRefreshService

service = StockRefreshService()
result = await service.refresh_collection("stock_zh_a_spot_em", task_id, params)

# 获取支持的集合列表
collections = service.get_supported_collections()  # 返回 380 个

# 获取更新配置
config = StockRefreshService.get_update_config("stock_zh_a_spot_em")
```

### 9.4 验证测试

```bash
# 运行验证测试
python tests/stocks/verify_refactoring.py
python tests/stocks/test_stock_service_factory.py
python tests/stocks/check_coverage.py
```

### 9.5 前端同步更新

**后端 API**：
- 新增 `GET /api/stocks/collections/{collection_name}/update-config`
- 返回集合的更新配置（single_update, batch_update 参数）

**前端文件**：

| 文件 | 更新内容 |
|-----|----------|
| `frontend/src/api/stocks.ts` | 新增 `getUpdateConfig()` 方法 |
| `frontend/src/views/Stocks/collectionRefreshConfig.ts` | 20+ 常用集合配置 + 默认配置 |
| `frontend/src/views/Stocks/Collection.vue` | 简化为从 refreshConfig 动态获取信息 |

**已配置的集合**（20+）：
- 个股信息：`stock_individual_info_em`, `stock_individual_basic_info_xq`
- 历史行情：`stock_zh_a_hist`, `stock_zh_a_hist_min_em`
- 实时行情：`stock_zh_a_spot_em`, `stock_sh_a_spot_em`, `stock_sz_a_spot_em` 等
- 板块数据：`stock_board_industry_name_em`, `stock_board_concept_name_em` 等
- 涨跌停池：`stock_zt_pool_em`, `stock_dt_pool_em`, `stock_strong_pool_em`
- 龙虎榜：`stock_lhb_detail_em`
- 融资融券：`stock_margin_detail_szse`

**默认配置**（未配置的集合自动使用）：
```typescript
{
  uiType: 'none',              // 无参数
  allUpdate: {
    enabled: true,
    buttonText: '更新全部数据'
  }
}
```

### 9.6 测试脚本清单

| 脚本 | 用途 |
|-----|------|
| `tests/stocks/verify_refactoring.py` | 完整重构验证 |
| `tests/stocks/test_stock_service_factory.py` | 服务工厂测试 |
| `tests/stocks/check_coverage.py` | 覆盖率检查 |
| `tests/stocks/generate_missing_services.py` | 生成缺失服务 |
