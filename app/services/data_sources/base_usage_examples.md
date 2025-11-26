# BaseProvider 和 BaseService 使用指南

## 概述

`BaseProvider` 和 `BaseService` 提供了通用的数据获取和服务功能，让子类只需要关注核心业务逻辑。

## 目录结构

```
app/services/data_sources/
├── base_provider.py    # 数据提供者基类
├── base_service.py     # 数据服务基类
├── funds/
│   ├── providers/
│   │   └── fund_xxx_provider.py
│   └── services/
│       └── fund_xxx_service.py
```

---

## 示例1：简单无参数接口（如 fund_name_em）

### Provider（约10行代码）

```python
from app.services.data_sources.base_provider import SimpleProvider

class FundNameEmProvider(SimpleProvider):
    """基金基本信息提供者"""
    collection_name = "fund_name_em"
    display_name = "基金基本信息"
    akshare_func = "fund_name_em"
    unique_keys = ["基金代码"]
    
    field_info = [
        {"name": "基金代码", "type": "string", "description": "基金代码"},
        {"name": "基金简称", "type": "string", "description": "基金简称"},
        {"name": "基金类型", "type": "string", "description": "基金类型"},
    ]
```

### Service（约5行代码）

```python
from app.services.data_sources.base_service import SimpleService
from .providers.fund_name_em_provider import FundNameEmProvider

class FundNameEmService(SimpleService):
    """基金基本信息服务"""
    collection_name = "fund_name_em"
    provider_class = FundNameEmProvider
```

---

## 示例2：需要参数的接口（如 fund_etf_fund_info_em）

### Provider（约20行代码）

```python
from app.services.data_sources.base_provider import BaseProvider

class FundEtfFundInfoEmProvider(BaseProvider):
    """ETF历史行情提供者"""
    collection_name = "fund_etf_fund_info_em"
    display_name = "ETF基金历史行情"
    akshare_func = "fund_etf_fund_info_em"
    unique_keys = ["基金代码", "净值日期"]
    
    # 参数映射：前端 fund_code -> akshare fund
    param_mapping = {
        "fund_code": "fund",
        "code": "fund",
    }
    
    # 必填参数
    required_params = ["fund"]
    
    # 将参数值添加到数据列
    add_param_columns = {"fund": "基金代码"}
    
    field_info = [
        {"name": "基金代码", "type": "string", "description": "基金代码"},
        {"name": "净值日期", "type": "string", "description": "净值日期"},
        {"name": "单位净值", "type": "float", "description": "单位净值"},
    ]
```

### Service（约15行代码）

```python
from app.services.data_sources.base_service import BaseService
from .providers.fund_etf_fund_info_em_provider import FundEtfFundInfoEmProvider

class FundEtfFundInfoEmService(BaseService):
    """ETF基金历史行情服务"""
    collection_name = "fund_etf_fund_info_em"
    provider_class = FundEtfFundInfoEmProvider
    
    # 批量更新配置：从 fund_etf_fund_daily_em 获取基金代码
    batch_source_collection = "fund_etf_fund_daily_em"
    batch_source_field = "基金代码"
    
    # 增量更新：按基金代码检查
    incremental_check_fields = ["基金代码"]
```

---

## 示例3：需要年份的复杂批量更新（如 fund_portfolio_hold_em）

### Provider

```python
from app.services.data_sources.base_provider import BaseProvider

class FundPortfolioHoldEmProvider(BaseProvider):
    """基金持仓股票提供者"""
    collection_name = "fund_portfolio_hold_em"
    display_name = "基金持仓股票"
    akshare_func = "fund_portfolio_hold_em"
    unique_keys = ["基金代码", "股票代码", "季度"]
    
    param_mapping = {
        "fund_code": "symbol",
        "code": "symbol",
        "year": "date",
    }
    
    required_params = ["symbol", "date"]
    add_param_columns = {"symbol": "基金代码"}
```

### Service

```python
from app.services.data_sources.base_service import BaseService
from .providers.fund_portfolio_hold_em_provider import FundPortfolioHoldEmProvider

class FundPortfolioHoldEmService(BaseService):
    """基金持仓股票服务"""
    collection_name = "fund_portfolio_hold_em"
    provider_class = FundPortfolioHoldEmProvider
    
    # 批量更新配置
    batch_source_collection = "fund_name_em"
    batch_source_field = "基金代码"
    batch_use_year = True
    batch_years_range = (2010, None)  # 2010年到今年
    
    # 增量更新：按基金代码+年份检查（从季度字段提取年份）
    incremental_check_fields = ["基金代码", "季度"]
    
    # 自定义参数构建
    def get_batch_params(self, code, year):
        return {"fund_code": code, "year": year}
    
    # 自定义已存在数据检查（从季度提取年份）
    async def _get_existing_combinations(self):
        existing = set()
        cursor = self.collection.find({}, {"基金代码": 1, "季度": 1})
        async for doc in cursor:
            fund_code = doc.get("基金代码")
            quarter = str(doc.get("季度", ""))
            if fund_code and len(quarter) >= 4:
                year = quarter[:4]
                existing.add((fund_code, year))
        return existing
```

---

## 示例4：年份遍历接口（如 fund_fh_em）

### Provider

```python
from app.services.data_sources.base_provider import BaseProvider

class FundFhEmProvider(BaseProvider):
    """基金分红数据提供者"""
    collection_name = "fund_fh_em"
    display_name = "基金分红数据"
    akshare_func = "fund_fh_em"
    unique_keys = ["基金代码", "年份"]
    
    param_mapping = {"year": "date"}
    required_params = ["date"]
    add_param_columns = {"date": "年份"}
```

### Service

```python
from app.services.data_sources.base_service import BaseService

class FundFhEmService(BaseService):
    """基金分红数据服务"""
    collection_name = "fund_fh_em"
    provider_class = FundFhEmProvider
    
    # 不需要源集合，直接遍历年份
    batch_use_year = True
    batch_years_range = (1999, None)
    incremental_check_fields = ["年份"]
    
    # 重写获取任务列表（只有年份，没有代码）
    async def _get_tasks_to_process(self, codes, years):
        existing = await self._get_existing_combinations()
        return [(year,) for year in years if (year,) not in existing]
    
    def get_batch_params(self, year):
        return {"year": year}
```

---

## 对比：使用基类前后代码量

| 类型 | 原代码行数 | 使用基类后 | 减少 |
|------|-----------|-----------|------|
| 简单Provider | ~50行 | ~10行 | 80% |
| 简单Service | ~100行 | ~5行 | 95% |
| 复杂Provider | ~70行 | ~25行 | 65% |
| 复杂Service | ~300行 | ~30行 | 90% |

---

## 基类提供的功能

### BaseProvider

- ✅ 参数名称映射（`param_mapping`）
- ✅ 必填参数验证（`required_params`）
- ✅ 通用 akshare 调用封装
- ✅ 自动添加元数据时间戳
- ✅ 将参数值写入数据列（`add_param_columns`）
- ✅ 唯一键定义（`unique_keys`）
- ✅ 字段信息定义（`field_info`）

### BaseService

- ✅ `get_overview()` - 数据概览
- ✅ `get_data()` - 分页查询
- ✅ `clear_data()` - 清空数据
- ✅ `update_single_data()` - 单条更新（使用 ControlMongodb）
- ✅ `update_batch_data()` - 批量更新
  - 自动从源集合获取代码列表
  - 年份范围配置
  - 增量更新（跳过已存在数据）
  - 并发控制（`asyncio.Semaphore`）
  - 任务进度更新（`TaskManager`）
- ✅ 元数据自动添加

---

## 迁移步骤

1. **创建新 Provider**：继承 `BaseProvider`，定义类属性
2. **创建新 Service**：继承 `BaseService`，关联 Provider
3. **测试**：验证单条和批量更新功能
4. **替换**：更新服务工厂中的引用
5. **删除旧代码**：移除旧的 Provider 和 Service
