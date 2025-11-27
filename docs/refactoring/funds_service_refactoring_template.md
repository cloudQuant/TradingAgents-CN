# Funds服务重构模板

## 概述

本文档说明如何将 `app/services/data_sources/funds/services` 目录下的服务类重构为继承 `BaseService`，以简化代码并提高可维护性。

## 参考实现

已完成重构的参考实现：`fund_portfolio_hold_em_service.py`

## 重构步骤

### 步骤1：修改类定义

**原代码**：
```python
class FundXxxService:
    """基金XXX服务"""
    
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.collection = db["fund_xxx"]
        self.provider = FundXxxProvider()
```

**重构后**：
```python
from app.services.data_sources.base_service import BaseService
from app.services.data_sources.funds.providers.fund_xxx_provider import FundXxxProvider

class FundXxxService(BaseService):
    """基金XXX服务"""
    
    # ===== 必须定义的属性 =====
    collection_name = "fund_xxx"
    provider_class = FundXxxProvider
```

### 步骤2：配置类属性

根据服务的特点配置以下属性：

```python
# 时间字段名（用于排序和概览）
time_field = "scraped_at"  # 或 "更新时间" 等

# 批量更新配置（如果需要批量更新）
batch_source_collection = "fund_name_em"  # 从哪个集合获取代码列表
batch_source_field = "基金代码"  # 从源集合获取的字段名
batch_years_range = (2010, None)  # 年份范围，None表示到今年
batch_use_year = True  # 是否需要年份参数
batch_concurrency = 3  # 默认并发数
batch_progress_interval = 100  # 进度更新间隔

# 增量更新检查字段（用于检查已存在的数据）
incremental_check_fields = ["基金代码", "季度"]  # 根据实际情况配置

# 额外的元数据字段
extra_metadata = {
    "数据源": "akshare",
    "接口名称": "fund_xxx",
}
```

### 步骤3：处理查询方法

**原代码**（通常可以删除，基类已提供）：
```python
async def get_overview(self) -> Dict[str, Any]:
    """获取数据概览"""
    # ... 实现代码

async def get_data(self, skip: int = 0, limit: int = 100, filters: Optional[Dict] = None):
    """获取数据列表"""
    # ... 实现代码
```

**重构后**：
- 如果逻辑与基类相同，直接删除，使用基类方法
- 如果需要自定义，重写相应方法

### 步骤4：重构 update_single_data 方法

**原代码**：
```python
async def update_single_data(self, **kwargs) -> Dict[str, Any]:
    """更新单条数据"""
    try:
        # 参数验证
        # 调用 provider
        # 保存数据
        # 返回结果
    except Exception as e:
        # 错误处理
```

**重构后**（根据实际情况选择）：

#### 选项A：如果参数验证逻辑简单，直接使用基类
```python
# 不需要重写，直接使用基类的实现
```

#### 选项B：如果需要自定义参数验证
```python
async def update_single_data(self, **kwargs) -> Dict[str, Any]:
    """更新单条数据（需要自定义参数验证）"""
    try:
        # 参数解析和验证
        param1 = kwargs.get("param1") or kwargs.get("alias1")
        if not param1:
            return {
                "success": False,
                "message": "缺少必须参数: param1",
                "inserted": 0,
            }
        
        # 调用基类方法
        return await super().update_single_data(param1=param1, **kwargs)
    except Exception as e:
        # 错误处理
```

#### 选项C：如果 provider 没有 get_unique_keys 方法（旧 provider）
```python
async def update_single_data(self, **kwargs) -> Dict[str, Any]:
    """更新单条数据"""
    try:
        # 参数验证
        # 调用 provider
        df = self.provider.fetch_data(**kwargs)
        
        if df is None or df.empty:
            return {"success": True, "message": "No data available", "inserted": 0}
        
        # 手动指定唯一键（因为旧 provider 没有 get_unique_keys 方法）
        from app.services.database.control_mongodb import ControlMongodb
        unique_keys = ["字段1", "字段2"]  # 根据实际情况配置
        extra_fields = self._get_extra_fields()
        
        control_db = ControlMongodb(self.collection, unique_keys)
        result = await control_db.save_dataframe_to_collection(df, extra_fields=extra_fields)
        
        return {
            "success": result["success"],
            "message": result["message"],
            "inserted": result.get("inserted", 0) + result.get("updated", 0),
        }
    except Exception as e:
        # 错误处理
```

### 步骤5：重构 update_batch_data 方法

**原代码**（通常很长，包含大量重复逻辑）：
```python
async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
    """批量更新数据"""
    # 1. 获取代码列表
    # 2. 确定年份范围
    # 3. 检查已有数据
    # 4. 生成任务列表
    # 5. 并发执行
    # 6. 返回结果
```

**重构后**（大多数情况下可以直接使用基类）：
```python
# 如果配置了 batch_source_collection，基类会自动处理批量更新
# 不需要重写 update_batch_data 方法
```

**如果需要自定义批量更新逻辑**：
```python
async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
    """批量更新数据（自定义逻辑）"""
    # 重写基类方法以实现自定义逻辑
    # 参考 fund_portfolio_hold_em_service.py 的实现
```

### 步骤6：实现必要的方法

根据服务的特点，可能需要重写以下方法：

#### get_batch_params
```python
def get_batch_params(self, code: str, year: str = None) -> Dict[str, Any]:
    """构建批量任务的参数"""
    if year:
        return {"fund_code": code, "year": year}
    return {"fund_code": code}
```

#### _get_existing_combinations（如果需要特殊逻辑）
```python
async def _get_existing_combinations(self) -> Set[Tuple]:
    """获取已存在的数据组合（特殊逻辑）"""
    # 例如：从"季度"字段中提取年份
    existing: Set[Tuple[str, str]] = set()
    cursor = self.collection.find({}, {"基金代码": 1, "季度": 1})
    async for doc in cursor:
        # 特殊处理逻辑
        existing.add((code, year))
    return existing
```

#### _get_extra_fields（如果 provider 没有 akshare_func 属性）
```python
def _get_extra_fields(self) -> Dict[str, str]:
    """获取额外的元数据字段"""
    fields = dict(self.extra_metadata)
    # 旧 provider 可能没有 akshare_func 属性
    return fields
```

#### _get_unique_keys_for_batch（如果 provider 没有 get_unique_keys 方法）
```python
def _get_unique_keys_for_batch(self) -> List[str]:
    """获取批量更新时使用的唯一键"""
    return ["字段1", "字段2"]  # 根据实际情况配置
```

#### _execute_batch_tasks（如果 provider 没有 get_unique_keys 方法）
```python
async def _execute_batch_tasks(self, tasks, task_id, task_manager, concurrency):
    """并发执行批量任务（重写以支持旧 provider）"""
    # 参考 fund_portfolio_hold_em_service.py 的实现
    # 使用 _get_unique_keys_for_batch() 而不是 provider.get_unique_keys()
```

## 常见模式

### 模式1：简单服务（无参数或简单参数）

```python
class FundXxxService(BaseService):
    collection_name = "fund_xxx"
    provider_class = FundXxxProvider
    
    # 不需要批量更新
    # 不需要重写任何方法
```

### 模式2：需要年份参数的批量更新

```python
class FundXxxService(BaseService):
    collection_name = "fund_xxx"
    provider_class = FundXxxProvider
    
    batch_source_collection = "fund_name_em"
    batch_source_field = "基金代码"
    batch_years_range = (2010, None)
    batch_use_year = True
    incremental_check_fields = ["基金代码", "年份"]
    
    def get_batch_params(self, code: str, year: str) -> Dict[str, Any]:
        return {"fund_code": code, "year": year}
```

### 模式3：需要从季度字段提取年份

```python
class FundXxxService(BaseService):
    # ... 配置 ...
    incremental_check_fields = ["基金代码", "季度"]
    
    async def _get_existing_combinations(self) -> Set[Tuple]:
        """从季度字段中提取年份"""
        existing: Set[Tuple[str, str]] = set()
        cursor = self.collection.find({}, {"基金代码": 1, "季度": 1})
        async for doc in cursor:
            fund_code = doc.get("基金代码")
            quarter = str(doc.get("季度", ""))
            if fund_code and len(quarter) >= 4 and quarter[:4].isdigit():
                year = quarter[:4]
                existing.add((fund_code, year))
        return existing
```

### 模式4：旧 provider（没有 get_unique_keys 方法）

```python
class FundXxxService(BaseService):
    # ... 配置 ...
    
    def _get_unique_keys_for_batch(self) -> List[str]:
        return ["字段1", "字段2"]
    
    def _get_extra_fields(self) -> Dict[str, str]:
        return dict(self.extra_metadata)
    
    async def _execute_batch_tasks(self, tasks, task_id, task_manager, concurrency):
        # 参考 fund_portfolio_hold_em_service.py 的实现
        # 使用 _get_unique_keys_for_batch() 而不是 provider.get_unique_keys()
```

## 检查清单

重构完成后，检查以下项目：

- [ ] 类继承自 `BaseService`
- [ ] 定义了 `collection_name` 和 `provider_class`
- [ ] 配置了必要的批量更新属性（如果需要）
- [ ] 删除了与基类重复的方法（`get_overview`, `get_data` 等）
- [ ] 重写了需要自定义的方法（`update_single_data`, `get_batch_params` 等）
- [ ] 处理了旧 provider 的兼容性问题（`get_unique_keys`, `akshare_func` 等）
- [ ] 测试单条更新功能
- [ ] 测试批量更新功能（如果支持）
- [ ] 检查日志输出是否正确

## 注意事项

1. **保持逻辑不变**：重构的目标是简化代码，不是改变功能逻辑
2. **向后兼容**：确保重构后的代码与现有调用方式兼容
3. **测试验证**：重构后务必进行充分测试
4. **文档更新**：如果服务的行为有变化，更新相关文档

## 示例：完整的重构示例

参考 `fund_portfolio_hold_em_service.py` 的完整实现。

