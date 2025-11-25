# 基金集合开发完整指南

以 `fund_portfolio_hold_em`（基金股票持仓）为例，记录集合页面涉及的所有文件、函数和配置。

---

## 1. 文件清单

### 1.1 后端文件

| 文件路径 | 职责 | 关键函数/类 |
|---------|------|------------|
| `app/routers/funds.py` | API路由定义 | `list_fund_collections()`, `get_fund_collection_data()`, `refresh_fund_collection()`, `get_refresh_task_status()` |
| `app/services/fund_refresh_service.py` | 刷新服务调度 | `FundRefreshService.refresh_collection()` |
| `app/services/data_sources/funds/services/fund_portfolio_hold_em_service.py` | 业务逻辑 | `update_single_data()`, `update_batch_data()`, `get_overview()`, `get_data()` |
| `app/services/data_sources/funds/providers/fund_portfolio_hold_em_provider.py` | 数据获取 | `fetch_data()` |
| `app/config/fund_update_config.py` | 更新配置 | `FUND_UPDATE_CONFIG["fund_portfolio_hold_em"]` |
| `app/utils/task_manager.py` | 任务状态 | `TaskManager.create_task()`, `update_progress()`, `complete_task()`, `fail_task()` |
| `app/services/database/control_mongodb.py` | 数据去重 | `ControlMongodb.save_dataframe_to_collection()` |

### 1.2 前端文件

| 文件路径 | 职责 | 关键函数/变量 |
|---------|------|--------------|
| `frontend/src/views/Funds/Collection.vue` | 集合页面 | `handleBatchUpdate()`, `pollBatchTaskStatus()`, `loadData()` |
| `frontend/src/api/funds.ts` | API调用 | `refreshCollectionData()`, `getRefreshTaskStatus()` |

---

## 2. API 接口

### 2.1 获取集合列表
```
GET /api/funds/collections
Response: { success: true, data: [{ name, display_name, description, route, fields }] }
```

### 2.2 获取集合数据
```
GET /api/funds/collections/{collection_name}?page=1&page_size=50
Response: { success: true, data: { items, total, page, page_size, fields } }
```

### 2.3 刷新数据
```
POST /api/funds/collections/{collection_name}/refresh
Body: { update_type: 'batch', year?: string, concurrency?: number }
Response: { success: true, data: { task_id } }
```

### 2.4 查询任务状态
```
GET /api/funds/collections/{collection_name}/refresh/status/{task_id}
Response: { success: true, data: { status, progress, total, message, result } }
```

---

## 3. 后端核心代码

### 3.1 路由层 - `app/routers/funds.py`

```python
@router.post("/collections/{collection_name}/refresh")
async def refresh_fund_collection(
    collection_name: str,
    background_tasks: BackgroundTasks,
    params: Dict[str, Any] = Body(default={}),
):
    task_manager = get_task_manager()
    task_id = task_manager.create_task(
        task_type=f"refresh_{collection_name}",
        description=f"更新基金集合: {collection_name}"
    )
    
    async def do_refresh():
        refresh_service = FundRefreshService(db)
        await refresh_service.refresh_collection(collection_name, task_id, params)
    
    background_tasks.add_task(do_refresh)
    return {"success": True, "data": {"task_id": task_id}}

@router.get("/collections/{collection_name}/refresh/status/{task_id}")
async def get_refresh_task_status(collection_name: str, task_id: str):
    task_manager = get_task_manager()
    task = task_manager.get_task(task_id)
    return {"success": True, "data": task}
```

### 3.2 刷新服务 - `app/services/fund_refresh_service.py`

```python
class FundRefreshService:
    # 前端专用参数，不传给 akshare
    FRONTEND_ONLY_PARAMS = {'batch', 'batch_update', 'update_type', 'concurrency', ...}
    
    async def refresh_collection(self, collection_name: str, task_id: str, params: Dict = None):
        # 判断批量/单条更新
        is_batch = params.get("update_type") == "batch" if params else False
        
        # 过滤参数
        api_params = {k: v for k, v in params.items() if k not in self.FRONTEND_ONLY_PARAMS}
        if is_batch and "concurrency" in params:
            api_params["concurrency"] = params["concurrency"]
        
        # 调用对应方法
        if is_batch and hasattr(service, "update_batch_data"):
            result = await service.update_batch_data(task_id=task_id, **api_params)
        else:
            result = await service.update_single_data(**api_params)
            # 单条更新在这里处理任务状态
            if result.get("success"):
                self.task_manager.complete_task(task_id)
            else:
                self.task_manager.fail_task(task_id, result.get("message"))
```

### 3.3 Service层 - `fund_portfolio_hold_em_service.py`

```python
class FundPortfolioHoldEmService:
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = db["fund_portfolio_hold_em"]
        self.provider = FundPortfolioHoldEmProvider()
    
    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """单条更新（需要 fund_code 和 year）"""
        fund_code = kwargs.get("fund_code")
        year = kwargs.get("year")
        
        if not fund_code:
            return {"success": False, "message": "缺少必须参数: fund_code"}
        if not year:
            return {"success": False, "message": "缺少必须参数: year"}
        
        df = self.provider.fetch_data(fund_code=fund_code, year=year)
        
        unique_keys = ["基金代码", "股票代码", "季度"]
        control_db = ControlMongodb(self.collection, unique_keys)
        result = await control_db.save_dataframe_to_collection(df, extra_fields={...})
        return result
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """批量更新"""
        task_manager = get_task_manager() if task_id else None
        year = kwargs.get("year")
        concurrency = int(kwargs.get("concurrency", 3))
        
        # 1. 获取基金代码列表
        fund_codes = []
        cursor = self.db["fund_name_em"].find({}, {"基金代码": 1})
        async for doc in cursor:
            fund_codes.append(doc.get("基金代码"))
        
        # 2. 获取已存在组合（增量更新）
        existing = set()
        async for doc in self.collection.find({}, {"基金代码": 1, "季度": 1}):
            existing.add((doc["基金代码"], doc["季度"][:4]))
        
        # 3. 生成待更新组合
        combinations = [(c, y) for c in fund_codes for y in years if (c, y) not in existing]
        
        # 4. 并发执行
        semaphore = asyncio.Semaphore(concurrency)
        async def fetch_and_save(code, y):
            async with semaphore:
                df = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: self.provider.fetch_data(fund_code=code, year=y)
                )
                # 保存数据...
                # 更新进度...
        
        await asyncio.gather(*[fetch_and_save(c, y) for c, y in combinations])
        
        # 5. 完成任务
        task_manager.complete_task(task_id, result={...}, message="完成")
```

### 3.4 Provider层 - `fund_portfolio_hold_em_provider.py`

```python
class FundPortfolioHoldEmProvider:
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        symbol = kwargs.get("fund_code") or kwargs.get("symbol")
        date = kwargs.get("year") or kwargs.get("date")
        
        if not symbol:
            raise ValueError("缺少必须参数: fund_code/symbol")
        if not date:
            raise ValueError("缺少必须参数: year/date")
        
        df = ak.fund_portfolio_hold_em(symbol=str(symbol), date=str(date))
        
        if '基金代码' not in df.columns:
            df['基金代码'] = symbol
        df['更新时间'] = datetime.now()
        
        return df
```

---

## 4. 前端核心代码

### 4.1 状态变量

```typescript
// Collection.vue
const batchUpdating = ref(false)           // 批量更新中
const progressPercentage = ref(0)           // 进度百分比
const progressStatus = ref('')              // 进度状态: success/exception/warning
const progressMessage = ref('')             // 进度消息
const currentTaskId = ref('')               // 当前任务ID
let batchProgressTimer: ReturnType<typeof setInterval> | null = null
```

### 4.2 批量更新处理

```typescript
const handleBatchUpdate = async () => {
  batchUpdating.value = true
  progressPercentage.value = 0
  progressStatus.value = ''
  progressMessage.value = '正在创建批量更新任务...'
  
  const res = await fundsApi.refreshCollectionData(collectionName.value, {
    update_type: 'batch',  // 关键：标识批量更新
    ...batchUpdateParams.value
  })
  
  if (res.success && res.data?.task_id) {
    currentTaskId.value = res.data.task_id
    pollBatchTaskStatus()
  }
}
```

### 4.3 轮询任务状态

```typescript
const pollBatchTaskStatus = async () => {
  batchProgressTimer = setInterval(async () => {
    const res = await fundsApi.getRefreshTaskStatus(collectionName.value, currentTaskId.value)
    
    if (res.success && res.data) {
      const task = res.data
      
      // 更新进度
      if (task.progress !== undefined && task.total !== undefined) {
        progressPercentage.value = Math.round((task.progress / task.total) * 100)
      }
      progressMessage.value = task.message || '正在批量更新...'
      
      // 完成
      if (task.status === 'success') {
        clearInterval(batchProgressTimer)
        progressStatus.value = 'success'
        progressPercentage.value = 100
        await loadData()
        batchUpdating.value = false
        
      } else if (task.status === 'failed') {
        clearInterval(batchProgressTimer)
        progressStatus.value = 'exception'
        batchUpdating.value = false
      }
    }
  }, 1000)
}
```

### 4.4 进度条模板

```vue
<div v-if="batchUpdating" style="margin-top: 16px;">
  <el-progress :percentage="progressPercentage" :status="progressStatus" :stroke-width="15" />
  <p style="margin-top: 10px; text-align: center;">{{ progressMessage }}</p>
</div>
```

---

## 5. 配置文件

### 5.1 更新配置 - `app/config/fund_update_config.py`

```python
FUND_UPDATE_CONFIG = {
    "fund_portfolio_hold_em": {
        "display_name": "基金股票持仓",
        "update_description": "获取基金股票持仓数据",
        "single_update": {
            "enabled": True,
            "description": "更新单个基金指定年份的股票持仓",
            "params": [
                {"name": "fund_code", "label": "基金代码", "type": "text", "required": True},
                {"name": "year", "label": "年份", "type": "text", "required": True}
            ]
        },
        "batch_update": {
            "enabled": True,
            "description": "批量更新所有基金的股票持仓数据",
            "params": [
                {"name": "year", "label": "年份（可选）", "type": "text", "required": False},
                {"name": "concurrency", "label": "并发数", "type": "number", "default": 3, "min": 1, "max": 10}
            ]
        }
    }
}
```

### 5.2 集合字段定义 - `app/routers/funds.py`

```python
# list_fund_collections() 函数中
{
    "name": "fund_portfolio_hold_em",
    "display_name": "基金持仓-东财",
    "description": "东方财富网-数据中心-基金持仓",
    "route": "/funds/collections/fund_portfolio_hold_em",
    "fields": [
        "基金代码", "股票代码", "股票名称", "季度",
        "持仓占比", "持仓数量", "持仓市值",
        "数据源", "接口名称", "更新时间"
    ]
}
```

---

## 6. 数据流向图

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
│                              后端路由层 funds.py                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  POST /refresh → refresh_fund_collection()                                   │
│         ↓                                                                    │
│  TaskManager.create_task() → 返回 task_id                                    │
│         ↓                                                                    │
│  background_tasks.add_task(do_refresh)                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                       ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                          刷新服务 FundRefreshService                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  refresh_collection()                                                        │
│         ↓                                                                    │
│  判断 update_type == 'batch' ?                                               │
│    是 → service.update_batch_data(task_id=task_id, ...)                     │
│    否 → service.update_single_data(...)                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                       ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Service层 FundPortfolioHoldEmService                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  update_batch_data()                                                         │
│    1. 从 fund_name_em 获取基金代码                                            │
│    2. 获取已存在组合 → 增量更新                                               │
│    3. asyncio.Semaphore 并发控制                                             │
│    4. provider.fetch_data() → ControlMongodb.save_dataframe_to_collection() │
│    5. task_manager.update_progress() 更新进度                                │
│    6. task_manager.complete_task() 完成                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                       ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                   Provider层 FundPortfolioHoldEmProvider                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  fetch_data(fund_code, year)                                                 │
│         ↓                                                                    │
│  ak.fund_portfolio_hold_em(symbol, date) → DataFrame                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

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
   ```

3. **注册 Service** - `app/services/fund_refresh_service.py`
   ```python
   self.services = {
       "xxx": XxxService(self.db),
       ...
   }
   ```

4. **添加集合定义** - `app/routers/funds.py` 的 `list_fund_collections()`

5. **添加更新配置** - `app/config/fund_update_config.py`

### 7.2 检查清单

- [ ] Provider 的 `fetch_data` 正确获取参数
- [ ] Service 的 `update_batch_data` 接收 `task_id` 参数
- [ ] Service 使用 `ControlMongodb` 处理数据去重
- [ ] Service 调用 `task_manager.update_progress()` 更新进度
- [ ] Service 调用 `task_manager.complete_task()` 传递 result
- [ ] `fund_update_config.py` 配置了 `single_update` 和 `batch_update`
- [ ] `FundRefreshService.services` 字典中注册了新 Service

---

## 8. 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 缺少必须参数 | 未从 kwargs 获取 | `kwargs.get("year")` |
| 进度条不更新 | 设置了错误的状态变量 | 使用 `batchUpdating.value` |
| 任务状态重复设置 | service 和 refresh_collection 都调用 complete_task | 批量更新由 service 管理状态 |
| 数据重复 | 未使用 unique_keys | 使用 ControlMongodb |
| API限流 | 并发数过高 | 降低 concurrency 参数 |

---

**更新日期**：2025-11-25  
**示例集合**：fund_portfolio_hold_em, fund_portfolio_bond_hold_em
