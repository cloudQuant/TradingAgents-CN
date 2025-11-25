# 外汇数据集合开发指南

参考基金数据集合实现方式，记录外汇集合涉及的所有文件、函数和配置。

---

## 1. 文件清单

### 1.1 后端文件

| 文件路径 | 职责 | 关键函数/类 |
|---------|------|------------|
| `app/routers/currencies.py` | API路由定义 | `list_currencies_collections()`, `refresh_currency_collection()`, `get_currency_refresh_task_status()` |
| `app/services/currency_refresh_service.py` | 刷新服务调度 | `CurrencyRefreshService.refresh_collection()` |
| `app/services/data_sources/currencies/services/*_service.py` | 业务逻辑 | `update_single_data()`, `update_batch_data()`, `get_overview()`, `get_data()` |
| `app/services/data_sources/currencies/providers/*_provider.py` | 数据获取 | `fetch_data()` |
| `app/config/currency_update_config.py` | 更新配置 | `CURRENCY_UPDATE_CONFIGS` |
| `app/utils/task_manager.py` | 任务状态 | `TaskManager.create_task()`, `update_progress()`, `complete_task()` |

### 1.2 数据集合

| 集合名称 | 显示名称 | AKShare 接口 | 唯一标识字段 |
|---------|---------|-------------|-------------|
| `currency_latest` | 货币报价最新数据 | `ak.currency_latest()` | currency, base, date |
| `currency_history` | 货币报价历史数据 | `ak.currency_history()` | currency, base, date |
| `currency_time_series` | 货币报价时间序列 | `ak.currency_time_series()` | date |
| `currency_currencies` | 货币基础信息 | `ak.currency_currencies()` | id |
| `currency_convert` | 货币转换 | `ak.currency_convert()` | date, base, to, amount |

---

## 2. API 接口

### 2.1 获取集合列表
```
GET /api/currencies/collections
Response: { success: true, data: [{ name, display_name, description, route, fields }] }
```

### 2.2 获取集合数据
```
GET /api/currencies/collections/{collection_name}/data?page=1&page_size=50
Response: { success: true, data: { items, total, page, page_size } }
```

### 2.3 刷新数据
```
POST /api/currencies/collections/{collection_name}/refresh
Body: { update_type: 'batch', api_key: '...', ... }
Response: { success: true, data: { task_id } }
```

### 2.4 查询任务状态
```
GET /api/currencies/collections/{collection_name}/refresh/status/{task_id}
Response: { success: true, data: { status, progress, total, message, result } }
```

### 2.5 获取更新配置
```
GET /api/currencies/collections/{collection_name}/update-config
Response: { success: true, data: { display_name, single_update, batch_update } }
```

---

## 3. 数据流向图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              前端 Collection.vue                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  点击"更新" → handleUpdate() → refreshCollectionData()                       │
│                                           ↓                                  │
│                                     返回 task_id                             │
│                                           ↓                                  │
│  pollTaskStatus() ← 轮询 ← getRefreshTaskStatus()                           │
│         ↓                                                                    │
│  更新 progressPercentage / progressMessage                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                       ↑ ↓ API
┌─────────────────────────────────────────────────────────────────────────────┐
│                              后端路由层 currencies.py                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  POST /refresh → refresh_currency_collection()                               │
│         ↓                                                                    │
│  TaskManager.create_task() → 返回 task_id                                    │
│         ↓                                                                    │
│  background_tasks.add_task(do_refresh)                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                       ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                          刷新服务 CurrencyRefreshService                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  refresh_collection()                                                        │
│         ↓                                                                    │
│  判断 update_type == 'batch' ?                                               │
│    是 → service.update_batch_data(task_id=task_id, ...)                     │
│    否 → service.update_single_data(...)                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                       ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Service层 CurrencyLatestService 等                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  update_batch_data()                                                         │
│    1. 获取参数（api_key 等）                                                  │
│    2. provider.fetch_data() 获取数据                                         │
│    3. bulk_write() 保存到 MongoDB                                            │
│    4. task_manager.update_progress() 更新进度                                │
│    5. task_manager.complete_task() 完成                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                       ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                   Provider层 CurrencyLatestProvider 等                       │
├─────────────────────────────────────────────────────────────────────────────┤
│  fetch_data(base, symbols, api_key)                                          │
│         ↓                                                                    │
│  ak.currency_latest(base, symbols, api_key) → DataFrame                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. 目录结构

```
app/services/data_sources/currencies/
├── __init__.py
├── README.md
├── providers/
│   ├── __init__.py
│   ├── currency_latest_provider.py
│   ├── currency_history_provider.py
│   ├── currency_time_series_provider.py
│   ├── currency_currencies_provider.py
│   └── currency_convert_provider.py
└── services/
    ├── __init__.py
    ├── currency_latest_service.py
    ├── currency_history_service.py
    ├── currency_time_series_service.py
    ├── currency_currencies_service.py
    └── currency_convert_service.py
```

---

## 5. 新增集合步骤

### 5.1 后端步骤

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
       async def get_data(self, skip, limit, filters): ...
   ```

3. **注册 Service** - `app/services/currency_refresh_service.py`
   ```python
   self.services = {
       "xxx": XxxService(self.db),
       ...
   }
   ```

4. **添加集合定义** - `app/routers/currencies.py` 的 `list_currencies_collections()`

5. **添加更新配置** - `app/config/currency_update_config.py`

### 5.2 检查清单

- [ ] Provider 的 `fetch_data` 正确获取参数
- [ ] Service 的 `update_batch_data` 接收 `task_id` 参数
- [ ] Service 调用 `task_manager.update_progress()` 更新进度
- [ ] Service 调用 `task_manager.complete_task()` 传递 result
- [ ] `currency_update_config.py` 配置了 `single_update` 和 `batch_update`
- [ ] `CurrencyRefreshService.services` 字典中注册了新 Service

---

## 6. 注意事项

1. **API Key 必须**: 所有外汇接口都需要 CurrencyScoop API Key
2. **参数过滤**: 前端特有参数（如 `update_type`, `batch`）会被自动过滤
3. **进度更新**: 批量更新时，Service 层负责更新进度和完成任务
4. **错误处理**: 单条更新失败时，由 RefreshService 处理任务状态

---

**更新日期**：2025-11-25
**数据集合**：currency_latest, currency_history, currency_time_series, currency_currencies, currency_convert
**数据去重**：使用 `ControlMongodb` 类，根据 `UNIQUE_KEYS` 进行数据去重
