# 单个更新性能分析

## 问题描述

单个更新 `fund_etf_fund_info_em` 时，保存到数据集合的速度特别慢。

## 性能数据

从日志分析：
- **1068 条数据**：耗时约 16 秒（23:41:38 → 23:41:54）
- **2910 条数据**：耗时约 3分20秒（23:43:46 → 23:47:06）

平均速度：
- 1068 条：约 67 条/秒
- 2910 条：约 14.5 条/秒

## 当前写入流程

### 1. 单个更新入口 (`update_single_data`)

```python
# fund_etf_fund_info_em_service.py
async def update_single_data(self, **kwargs):
    # 1. 获取数据
    df = self.provider.fetch_data(fund_code=fund_code)
    
    # 2. 保存数据
    control_db = ControlMongodb(self.collection, unique_keys)
    result = await control_db.save_dataframe_to_collection(df, extra_fields)
```

### 2. 数据保存流程 (`save_dataframe_to_collection`)

```python
# control_mongodb.py
async def save_dataframe_to_collection(self, df, extra_fields):
    # 1. DataFrame → 字典列表
    records = df.to_dict("records")  # 1068 条或 2910 条
    
    # 2. 遍历每条记录
    for record in records:  # 循环 1068 次或 2910 次
        doc = dict(record)
        
        # 转换时间字段（每条记录都调用）
        doc = self._convert_datetime_fields(doc)
        
        # 添加额外字段
        if extra_fields:
            doc.update(extra_fields)
        
        # 构建更新操作（每条记录都调用）
        ops.append(self._build_update_operation(doc))
        
        # 达到 1000 条时执行 bulk_write
        if len(ops) >= 1000:
            result = await self._execute_batch(ops)
            ops = []
    
    # 处理剩余操作
    if ops:
        result = await self._execute_batch(ops)
```

### 3. 每条记录的处理开销

对于每条记录，都会执行：

1. **`_convert_datetime_fields(doc)`**：
   ```python
   for key, value in list(doc.items()):  # 遍历所有字段
       if isinstance(value, datetime):
           doc[key] = value.isoformat()
       elif isinstance(value, date):
           doc[key] = value.isoformat()
       elif pd.isna(value):
           doc[key] = None
   ```
   - 开销：O(n)，n 是字段数（约 10-15 个字段）

2. **`_build_filter(doc)`**：
   ```python
   for key in self.unique_keys:  # ["基金代码", "净值日期"]
       value = doc.get(key)
       if value is not None:
           if isinstance(value, (date, datetime)):
               filter_doc[key] = value.isoformat()
           else:
               filter_doc[key] = str(value)
   ```
   - 开销：O(2)，2 个唯一键

3. **`_build_update_operation(doc)`**：
   ```python
   doc["更新时间"] = datetime.now().isoformat()  # 每条记录都调用 datetime.now()
   # 构建 UpdateOne 对象
   ```
   - 开销：创建 datetime 对象 + 构建 UpdateOne 对象

### 4. 批量写入

- **批量大小**：1000 条/批
- **执行方式**：`bulk_write(ops, ordered=False)`
- **对于 1068 条**：执行 2 次 bulk_write（1000 + 68）
- **对于 2910 条**：执行 3 次 bulk_write（1000 + 1000 + 910）

## 性能瓶颈分析

### 瓶颈 1: 逐条处理开销

**问题**：
- 每条记录都要单独调用 `_convert_datetime_fields`、`_build_filter`、`_build_update_operation`
- 对于 2910 条数据，这些函数被调用 2910 次

**开销估算**：
- `_convert_datetime_fields`：2910 次 × 10 字段 = 29,100 次字段检查
- `_build_filter`：2910 次 × 2 唯一键 = 5,820 次键处理
- `datetime.now()`：2910 次调用（每条记录都获取当前时间）

### 瓶颈 2: 时间字段转换效率

**问题**：
- 每条记录都遍历所有字段检查是否为 datetime
- 使用 `list(doc.items())` 创建新列表

**优化空间**：
- 可以批量处理时间字段转换
- 可以预先知道哪些字段是时间类型

### 瓶颈 3: datetime.now() 重复调用

**问题**：
- 每条记录都调用 `datetime.now()` 获取当前时间
- 对于 2910 条数据，调用 2910 次

**优化空间**：
- 可以在批量处理前获取一次时间，所有记录共用

### 瓶颈 4: 批量大小可能不够优化

**当前**：1000 条/批
- 对于 1068 条：2 次数据库操作
- 对于 2910 条：3 次数据库操作

**可能优化**：
- 对于单个更新，数据量通常不会太大（几千条），可以考虑一次性写入
- 或者根据数据量动态调整批量大小

## 优化建议

### 优化 1: 批量处理时间字段转换

```python
# 优化前：每条记录都转换
for record in records:
    doc = self._convert_datetime_fields(doc)

# 优化后：批量转换
def _convert_datetime_fields_batch(self, records: List[Dict]) -> List[Dict]:
    """批量转换时间字段"""
    current_time = datetime.now().isoformat()  # 只调用一次
    
    for doc in records:
        for key, value in list(doc.items()):
            if isinstance(value, datetime):
                doc[key] = value.isoformat()
            elif isinstance(value, date):
                doc[key] = value.isoformat()
            elif pd.isna(value):
                doc[key] = None
        # 统一设置更新时间
        doc["更新时间"] = current_time
    
    return records
```

### 优化 2: 批量构建更新操作

```python
# 优化前：逐条构建
for record in records:
    ops.append(self._build_update_operation(doc))

# 优化后：批量构建
def _build_update_operations_batch(self, records: List[Dict]) -> List[UpdateOne]:
    """批量构建更新操作"""
    current_time = datetime.now().isoformat()
    ops = []
    
    for doc in records:
        # 批量处理逻辑
        filter_doc = self._build_filter(doc)
        doc["更新时间"] = current_time
        ops.append(UpdateOne(filter_doc, {"$set": doc, ...}, upsert=True))
    
    return ops
```

### 优化 3: 对于单个更新，使用更小的批量或一次性写入

```python
# 对于单个更新，如果数据量 < 5000，可以考虑一次性写入
if len(records) < 5000:
    # 一次性构建所有操作
    ops = self._build_update_operations_batch(records)
    result = await self._execute_batch(ops)
else:
    # 分批处理
    ...
```

### 优化 4: 使用更高效的 DataFrame 处理

```python
# 优化前：to_dict("records") 然后逐条处理
records = df.to_dict("records")

# 优化后：直接在 DataFrame 层面处理
# 批量转换时间字段
for col in df.columns:
    if df[col].dtype == 'datetime64[ns]':
        df[col] = df[col].dt.strftime('%Y-%m-%dT%H:%M:%S')
```

## 预期性能提升

优化后预期：
- **1068 条数据**：从 16 秒 → 约 2-3 秒（提升 5-8 倍）
- **2910 条数据**：从 3分20秒 → 约 5-8 秒（提升 25-40 倍）

## 实施优先级

1. **高优先级**：优化 `datetime.now()` 重复调用（简单，效果明显）
2. **中优先级**：批量处理时间字段转换（中等复杂度，效果明显）
3. **低优先级**：优化批量大小策略（需要测试）

