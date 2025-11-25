# 期货数据集合重构说明

## 概述

本次重构将期货模块的52个数据集合按照基金模块（funds）的架构模式进行了统一改造，建立了规范化的Provider-Service-RefreshService三层结构。

## 架构设计

### 1. 目录结构

```
app/services/data_sources/futures/
├── __init__.py                          # 模块初始化
├── collection_config_ways.md            # 本文档
├── providers/                           # Provider层（数据获取）
│   ├── __init__.py
│   ├── futures_fees_info_provider.py
│   ├── futures_comm_info_provider.py
│   ├── ...                              # 其他52个provider文件
│   └── futures_news_shmet_provider.py
└── services/                            # Service层（业务逻辑）
    ├── __init__.py
    ├── base_futures_service.py          # 基类服务
    ├── futures_fees_info_service.py
    ├── futures_comm_info_service.py
    ├── ...                              # 其他52个service文件
    └── futures_news_shmet_service.py
```

### 2. 核心组件

#### Provider层 (`providers/`)
- **职责**: 负责从AKShare获取原始数据
- **方法**:
  - `fetch_data(**kwargs)`: 获取数据，返回pandas DataFrame
  - `get_unique_keys()`: 返回唯一键字段列表
  - `get_field_info()`: 返回字段信息列表

#### Service层 (`services/`)
- **职责**: 负责业务逻辑处理，包括数据存储、查询、更新
- **基类**: `BaseFuturesService` 提供通用实现
- **方法**:
  - `get_overview()`: 获取数据概览
  - `get_data(skip, limit, filters)`: 获取数据列表
  - `update_single_data(**kwargs)`: 单条更新
  - `update_batch_data(task_id, **kwargs)`: 批量更新
  - `clear_data()`: 清空数据

#### RefreshService (`app/services/futures_refresh_service.py`)
- **职责**: 统一调度所有期货集合的刷新操作
- **特点**:
  - 注册所有45个服务实例
  - 支持任务进度跟踪
  - 参数过滤（前端参数 vs API参数）
  - 单条/批量更新判断

### 3. 配置文件

#### 更新配置 (`app/config/futures_update_config.py`)
定义每个集合的更新参数配置：

```python
FUTURES_UPDATE_CONFIGS = {
    "futures_fees_info": {
        "display_name": "期货交易费用参照表",
        "update_description": "从openctp获取期货交易费用数据",
        "single_update": {"enabled": False, "description": "", "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有数据", "params": []}
    },
    # ... 其他集合配置
}
```

## API接口

### 新增接口

1. **获取更新配置**
   ```
   GET /api/futures/collections/{collection_name}/update-config
   ```

2. **刷新集合数据（新版）**
   ```
   POST /api/futures/collections/{collection_name}/refresh
   Body: { "params": { "symbol": "...", "date": "..." } }
   ```

3. **获取刷新任务状态**
   ```
   GET /api/futures/refresh/task/{task_id}
   ```

4. **获取支持刷新的集合列表**
   ```
   GET /api/futures/refresh/supported-collections
   ```

## 数据集合列表

### 无参数集合（6个）
| 集合名 | 显示名称 | AKShare接口 |
|--------|----------|-------------|
| futures_fees_info | 期货交易费用参照表 | futures_fees_info |
| futures_contract_info_dce | 大连商品交易所合约信息 | futures_contract_info_dce |
| futures_contract_info_gfex | 广州期货交易所合约信息 | futures_contract_info_gfex |
| futures_hq_subscribe_exchange_symbol | 外盘品种代码表 | futures_hq_subscribe_exchange_symbol |
| futures_global_spot_em | 外盘实时行情数据-东财 | futures_global_spot_em |
| index_hog_spot_price | 生猪市场价格指数 | index_hog_spot_price |

### 日期参数集合（12个）
| 集合名 | 参数 |
|--------|------|
| futures_rule | date (YYYYMMDD) |
| futures_dce_position_rank | date, vars_list |
| futures_gfex_position_rank | date, vars_list |
| futures_warehouse_receipt_czce | date |
| futures_warehouse_receipt_dce | date |
| futures_shfe_warehouse_receipt | date |
| futures_gfex_warehouse_receipt | date |
| futures_to_spot_dce | date (YYYYMM) |
| futures_to_spot_czce | date |
| futures_to_spot_shfe | date (YYYYMM) |
| futures_contract_info_shfe | date |
| futures_contract_info_cffex | date |

### 品种代码参数集合（27+个）
包括库存数据、行情数据、合约详情等，需要symbol参数

## 使用示例

### 1. 刷新无参数集合
```python
# 刷新期货交易费用表
POST /api/futures/collections/futures_fees_info/refresh
Body: { "params": {} }
```

### 2. 刷新日期参数集合
```python
# 刷新大连商品交易所持仓排名
POST /api/futures/collections/futures_dce_position_rank/refresh
Body: { "params": { "date": "20241125" } }
```

### 3. 刷新品种参数集合
```python
# 刷新库存数据
POST /api/futures/collections/futures_inventory_99/refresh
Body: { "params": { "symbol": "豆一" } }
```

## 与基金模块的对比

| 特性 | 基金模块 | 期货模块 |
|------|----------|----------|
| Provider层 | ✅ | ✅ |
| Service层 | ✅ | ✅ |
| RefreshService | FundRefreshService | FuturesRefreshService |
| 配置文件 | fund_update_config.py | futures_update_config.py |
| 基类服务 | 无（各自实现） | BaseFuturesService |
| 集合数量 | ~40 | 52 |

## 注意事项

1. **原有更新任务**: `futures_update_tasks.py` 保留作为兼容层，新代码使用服务层
2. **参数过滤**: 前端特有参数（如 batch, page, limit）会自动过滤
3. **错误处理**: 所有异常会被捕获并通过任务管理器报告
4. **日志**: 使用 logging 模块记录所有操作

## 后续优化

1. 添加更多批量更新支持
2. 优化并发控制
3. 添加数据验证层
4. 添加缓存机制
