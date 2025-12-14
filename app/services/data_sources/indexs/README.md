# 指数数据模块 (Indexs)

本模块提供全球主要指数的实时行情和历史数据服务。

## 目录结构

```
app/services/data_sources/indexs/
├── __init__.py
├── README.md
├── collection_metadata.py      # 集合元信息配置
├── provider_registry.py        # Provider 注册与发现
├── service_registry.py         # Service 注册与发现
├── providers/                  # 数据提供者
│   ├── __init__.py
│   ├── stock_zh_index_spot_em_provider.py      # A股指数实时行情-东财
│   ├── stock_zh_index_spot_sina_provider.py    # A股指数实时行情-新浪
│   ├── stock_zh_index_daily_provider.py        # A股指数历史行情-新浪
│   ├── stock_zh_index_daily_em_provider.py     # A股指数历史行情-东财
│   ├── index_zh_a_hist_provider.py             # A股指数历史行情-通用
│   ├── index_zh_a_hist_min_em_provider.py      # A股指数分时行情-东财
│   ├── stock_hk_index_spot_sina_provider.py    # 港股指数实时行情-新浪
│   ├── stock_hk_index_daily_sina_provider.py   # 港股指数历史行情-新浪
│   ├── stock_hk_index_spot_em_provider.py      # 港股指数实时行情-东财
│   ├── stock_hk_index_daily_em_provider.py     # 港股指数历史行情-东财
│   ├── index_us_stock_sina_provider.py         # 美股指数行情-新浪
│   ├── index_global_spot_em_provider.py        # 全球指数实时行情-东财
│   └── index_global_hist_em_provider.py        # 全球指数历史行情-东财
└── services/                   # 数据服务（可选，用于自定义批量更新逻辑）
    └── __init__.py
```

## 支持的数据集合

### A股指数 (7个)
| 集合名称 | 显示名称 | AKShare接口 | 说明 |
|---------|---------|------------|------|
| stock_zh_index_spot_em | A股指数实时行情-东财 | stock_zh_index_spot_em | 需要symbol参数（指数类型） |
| stock_zh_index_spot_sina | A股指数实时行情-新浪 | stock_zh_index_spot_sina | 无参数 |
| stock_zh_index_daily | A股指数历史行情-新浪 | stock_zh_index_daily | 需要symbol参数 |
| stock_zh_index_daily_em | A股指数历史行情-东财 | stock_zh_index_daily_em | 需要symbol参数 |
| index_zh_a_hist | A股指数历史行情-通用 | index_zh_a_hist | 支持日/周/月周期 |
| index_zh_a_hist_min_em | A股指数分时行情-东财 | index_zh_a_hist_min_em | 支持1/5/15/30/60分钟 |

### 港股指数 (4个)
| 集合名称 | 显示名称 | AKShare接口 | 说明 |
|---------|---------|------------|------|
| stock_hk_index_spot_sina | 港股指数实时行情-新浪 | stock_hk_index_spot_sina | 无参数 |
| stock_hk_index_daily_sina | 港股指数历史行情-新浪 | stock_hk_index_daily_sina | 需要symbol参数 |
| stock_hk_index_spot_em | 港股指数实时行情-东财 | stock_hk_index_spot_em | 无参数 |
| stock_hk_index_daily_em | 港股指数历史行情-东财 | stock_hk_index_daily_em | 需要symbol参数 |

### 美股指数 (1个)
| 集合名称 | 显示名称 | AKShare接口 | 说明 |
|---------|---------|------------|------|
| index_us_stock_sina | 美股指数行情-新浪 | index_us_stock_sina | 支持.IXIC/.DJI/.INX/.NDX |

### 全球指数 (2个)
| 集合名称 | 显示名称 | AKShare接口 | 说明 |
|---------|---------|------------|------|
| index_global_spot_em | 全球指数实时行情-东财 | index_global_spot_em | 无参数 |
| index_global_hist_em | 全球指数历史行情-东财 | index_global_hist_em | 需要symbol参数（指数名称） |

## API 端点

所有 API 端点前缀: `/api/indexs`

| 端点 | 方法 | 说明 |
|------|------|------|
| /collections | GET | 获取所有集合列表 |
| /collections/{name} | GET | 获取集合数据（分页） |
| /collections/{name}/stats | GET | 获取集合统计信息 |
| /collections/{name}/update-config | GET | 获取更新配置 |
| /collections/{name}/refresh | POST | 刷新集合数据 |
| /collections/{name}/refresh/status/{task_id} | GET | 获取刷新任务状态 |
| /collections/{name}/clear | DELETE | 清空集合数据 |
| /collections/{name}/export | POST | 导出数据 |
| /collections/{name}/upload | POST | 上传数据文件 |
| /collections/{name}/sync | POST | 远程同步数据 |

## 前端路由

| 路由 | 页面 |
|------|------|
| /indexs/overview | 指数概览 |
| /indexs/collections | 数据集合列表 |
| /indexs/collections/:collectionName | 集合详情 |

## 添加新集合

1. 在 `providers/` 目录下创建新的 Provider 文件
2. 在 `collection_metadata.py` 中添加元信息（可选）
3. 在 `app/config/index_update_config.py` 中添加更新配置（可选）
4. 重启后端服务，新集合会自动注册

## 参考文档

- [数据集合实现指南](../../../../docs/数据集合实现指南.md)
- [AKShare 指数数据文档](https://akshare.akfamily.xyz/data/index/index.html)
