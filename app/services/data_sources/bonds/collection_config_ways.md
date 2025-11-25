# 债券数据集合配置开发指南

## 概述

本文档描述了债券数据集合的实现架构，参考了基金模块（fund_portfolio_hold_em）的设计模式。

## 目录结构

```
app/
├── config/
│   └── bond_update_config.py      # 34个债券集合的更新参数配置
├── services/
│   ├── bond_refresh_service.py    # 债券数据刷新服务（调度层）
│   └── data_sources/
│       └── bonds/
│           ├── __init__.py
│           ├── collection_config_ways.md  # 本文档
│           ├── providers/                  # 数据提供者（负责从AKShare获取数据）
│           │   ├── __init__.py
│           │   ├── bond_info_cm_provider.py
│           │   ├── bond_zh_hs_spot_provider.py
│           │   └── ... (共34个provider文件)
│           └── services/                   # 服务层（负责业务逻辑和数据存储）
│               ├── __init__.py
│               ├── base_bond_service.py    # 服务基类
│               ├── bond_info_cm_service.py
│               ├── bond_zh_hs_spot_service.py
│               └── ... (共34个service文件)
└── routers/
    └── bonds.py                   # API路由
```

## 架构分层

### 1. Provider层（数据提供者）

负责从AKShare获取原始数据。

```python
# 示例：bond_info_cm_provider.py
class BondInfoCmProvider:
    def __init__(self):
        self.collection_name = "bond_info_cm"
        self.display_name = "债券信息查询"
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """调用AKShare接口获取数据"""
        df = ak.bond_info_cm(**kwargs)
        # 添加元数据
        df['数据源'] = 'akshare'
        df['更新时间'] = datetime.now()
        return df
    
    def get_field_info(self) -> List[Dict]:
        """返回字段说明"""
        return [...]
```

### 2. Service层（服务层）

负责业务逻辑、数据处理和MongoDB存储。

```python
# 示例：使用基类
class BondZhHsSpotService(BaseBondService):
    def __init__(self, db):
        super().__init__(
            db, 
            "bond_zh_hs_spot",           # 集合名称
            BondZhHsSpotProvider(),       # 对应的Provider
            unique_keys=["代码"]          # 唯一键，用于去重
        )
```

**服务基类 (BaseBondService)** 提供以下方法：
- `get_overview()` - 获取数据概览
- `get_data(skip, limit, filters)` - 分页查询数据
- `clear_data()` - 清空集合数据
- `update_single_data(**kwargs)` - 单条更新
- `update_batch_data(task_id, **kwargs)` - 批量更新（支持进度跟踪）

### 3. Refresh Service层（调度层）

负责路由刷新请求到对应的服务。

```python
# bond_refresh_service.py
class BondRefreshService:
    def __init__(self, db):
        self._services = {
            "bond_info_cm": BondInfoCmService(db),
            "bond_zh_hs_spot": BondZhHsSpotService(db),
            # ... 其他34个服务
        }
    
    async def refresh_collection(self, collection_name, task_id, params):
        service = self.services[collection_name]
        if is_batch:
            return await service.update_batch_data(task_id=task_id, **params)
        else:
            return await service.update_single_data(**params)
```

### 4. 配置层

定义每个集合的更新参数。

```python
# bond_update_config.py
BOND_UPDATE_CONFIGS = {
    "bond_info_cm": {
        "display_name": "债券信息查询",
        "update_description": "从中国外汇交易中心获取债券信息",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "bond_name", "label": "债券名称", "type": "text"},
                {"name": "bond_code", "label": "债券代码", "type": "text"},
            ]
        },
        "batch_update": {
            "enabled": True,
            "params": [
                {"name": "concurrency", "label": "并发数", "type": "number", "default": 3}
            ]
        }
    },
    # ... 其他集合配置
}
```

## API接口

### 获取更新配置
```
GET /bonds/collections/{collection_name}/update-config
```

### 刷新集合数据
```
POST /bonds/collections/{collection_name}/refresh
```

### 查询刷新任务状态
```
GET /bonds/collections/refresh/task/{task_id}
```

## 34个债券数据集合清单

| 序号 | 集合名称 | 显示名称 | 类别 |
|------|----------|----------|------|
| 01 | bond_info_cm | 债券信息查询 | 基础数据 |
| 02 | bond_info_detail_cm | 债券基础信息 | 基础数据 |
| 03 | bond_zh_hs_spot | 沪深债券实时行情 | 沪深债券 |
| 04 | bond_zh_hs_daily | 沪深债券历史行情 | 沪深债券 |
| 05 | bond_zh_hs_cov_spot | 可转债实时行情 | 可转债 |
| 06 | bond_zh_hs_cov_daily | 可转债历史行情 | 可转债 |
| 07 | bond_zh_cov | 可转债数据一览表 | 可转债 |
| 08 | bond_cash_summary_sse | 债券现券市场概览 | 市场概览 |
| 09 | bond_deal_summary_sse | 债券成交概览 | 市场概览 |
| 10 | bond_debt_nafmii | 银行间市场债券发行 | 银行间市场 |
| 11 | bond_spot_quote | 现券市场做市报价 | 银行间市场 |
| 12 | bond_spot_deal | 现券市场成交行情 | 银行间市场 |
| 13 | bond_zh_hs_cov_min | 可转债分时行情 | 可转债分时 |
| 14 | bond_zh_hs_cov_pre_min | 可转债盘前分时 | 可转债分时 |
| 15 | bond_zh_cov_info | 可转债详情-东财 | 可转债详细 |
| 16 | bond_zh_cov_info_ths | 可转债详情-同花顺 | 可转债详细 |
| 17 | bond_cov_comparison | 可转债比价表 | 可转债详细 |
| 18 | bond_zh_cov_value_analysis | 可转债价值分析 | 可转债详细 |
| 19 | bond_sh_buy_back_em | 上证质押式回购 | 质押回购 |
| 20 | bond_sz_buy_back_em | 深证质押式回购 | 质押回购 |
| 21 | bond_buy_back_hist_em | 质押式回购历史 | 质押回购 |
| 22 | bond_cb_jsl | 可转债实时-集思录 | 集思录 |
| 23 | bond_cb_redeem_jsl | 可转债强赎-集思录 | 集思录 |
| 24 | bond_cb_index_jsl | 可转债等权指数-集思录 | 集思录 |
| 25 | bond_cb_adj_logs_jsl | 转股价调整-集思录 | 集思录 |
| 26 | bond_china_close_return | 收益率曲线历史 | 收益率 |
| 27 | bond_zh_us_rate | 中美国债收益率 | 收益率 |
| 28 | bond_treasure_issue_cninfo | 国债发行 | 债券发行 |
| 29 | bond_local_government_issue_cninfo | 地方债发行 | 债券发行 |
| 30 | bond_corporate_issue_cninfo | 企业债发行 | 债券发行 |
| 31 | bond_cov_issue_cninfo | 可转债发行 | 债券发行 |
| 32 | bond_cov_stock_issue_cninfo | 可转债转股 | 债券发行 |
| 33 | bond_new_composite_index_cbond | 中债新综合指数 | 中债指数 |
| 34 | bond_composite_index_cbond | 中债综合指数 | 中债指数 |

## 添加新集合的步骤

1. **创建Provider文件**
   - 在 `providers/` 目录创建 `bond_xxx_provider.py`
   - 实现 `fetch_data()` 和 `get_field_info()` 方法

2. **创建Service文件**
   - 在 `services/` 目录创建 `bond_xxx_service.py`
   - 继承 `BaseBondService` 或自定义实现

3. **更新配置文件**
   - 在 `bond_update_config.py` 中添加集合配置

4. **注册到BondRefreshService**
   - 在 `bond_refresh_service.py` 的 `_init_services()` 中添加服务

5. **更新bonds.py路由**
   - 在 `list_bond_collections()` 中添加集合元数据

## 数据去重机制

使用 `ControlMongodb` 类进行数据去重：

```python
control_db = ControlMongodb(collection, unique_keys=["债券代码", "日期"])
result = await control_db.save_dataframe_to_collection(df, extra_fields={...})
```

- 根据 `unique_keys` 判断记录是否已存在
- 存在则更新，不存在则插入
- 返回 `inserted` 和 `updated` 计数

## 任务进度跟踪

批量更新支持进度跟踪：

```python
async def update_batch_data(self, task_id: str, **kwargs):
    task_manager = get_task_manager()
    task_manager.update_progress(task_id, current, total, message)
    # ... 处理逻辑
    task_manager.complete_task(task_id, result={...})
```

前端可通过 `/bonds/collections/refresh/task/{task_id}` 查询进度。
