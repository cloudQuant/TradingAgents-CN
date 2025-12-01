# 批量更新数据保存逻辑详解

## 概述

本文档详细说明批量更新时数据如何保存到 MongoDB 数据集合的完整流程。

## 整体架构

```
批量更新任务
    ↓
并发获取数据 (process_task)
    ↓
数据队列 (data_queue)
    ↓
批量保存协程 (batch_saver)
    ↓
数据合并 (pd.concat)
    ↓
ControlMongodb.save_dataframe_to_collection
    ↓
MongoDB 批量写入 (bulk_write)
```

## 详细流程

### 1. 批量更新入口 (`_full_batch_update`)

**位置**: `app/services/data_sources/base_service.py`

**流程**:
1. 从源集合获取基金代码列表 (`_get_source_codes`)
2. 检查已有数据，过滤出需要处理的任务 (`_get_tasks_to_process`)
3. 调用 `_execute_batch_tasks` 并发执行任务

**关键代码**:
```python
# 获取代码列表
codes = await self._get_source_codes()

# 生成待处理任务
tasks_to_process = await self._get_tasks_to_process(codes, years)

# 并发执行
return await self._execute_batch_tasks(tasks_to_process, task_id, task_manager, concurrency)
```

### 2. 并发任务执行 (`_execute_batch_tasks`)

**核心组件**:
- **process_task**: 并发获取数据的协程（生产者）
- **batch_saver**: 批量保存数据的协程（消费者）
- **data_queue**: 异步队列，连接生产者和消费者

#### 2.1 数据获取协程 (`process_task`)

**职责**: 并发调用 provider 获取数据

**流程**:
```python
async def process_task(task_params: Tuple):
    # 1. 构建参数
    params = self.get_batch_params(*task_params)
    
    # 2. 调用 provider 获取数据（在线程池中执行，避免阻塞）
    df = await asyncio.get_event_loop().run_in_executor(
        None,
        lambda p=params: self.provider.fetch_data(**p)
    )
    
    # 3. 如果获取到数据，放入队列
    if df is not None and not df.empty:
        await data_queue.put(df)
        success_count += 1
```

**关键点**:
- 使用 `asyncio.Semaphore` 控制并发数
- 使用线程池执行同步的 provider 调用
- 获取到的 DataFrame 直接放入队列，不立即保存

#### 2.2 批量保存协程 (`batch_saver`)

**职责**: 从队列取出数据，累积到一定数量后批量保存

**流程**:
```python
async def batch_saver():
    accumulated_dfs = []  # 累积的 DataFrame 列表
    
    while True:
        # 1. 从队列获取数据
        df = await data_queue.get()
        if df is not None and not df.empty:
            accumulated_dfs.append(df)
        
        # 2. 检查是否需要保存
        should_save = (
            total_rows >= 5000 or  # 达到行数阈值
            elapsed >= 5.0 or      # 到达时间间隔（5秒）
            save_completed.is_set()  # 所有任务完成
        )
        
        # 3. 保存数据
        if should_save:
            combined_df = pd.concat(accumulated_dfs, ignore_index=True)
            result = await control_db.save_dataframe_to_collection(combined_df)
            accumulated_dfs.clear()
```

**保存触发条件**:
1. **行数阈值**: 累积数据达到 5000 条
2. **时间间隔**: 距离上次保存超过 5 秒
3. **任务完成**: 所有获取任务完成，保存剩余数据

**优势**:
- 减少数据库写入次数，提高性能
- 避免小批次频繁写库
- 定期 flush，避免数据积压

### 3. 数据合并 (`pd.concat`)

**位置**: `batch_saver` 中的 `save_accumulated` 函数

**代码**:
```python
combined_df = pd.concat(accumulated_dfs, ignore_index=True)
```

**作用**:
- 将多个 DataFrame 合并成一个
- `ignore_index=True` 重新生成索引

**示例**:
```
DataFrame 1: 1000 行 (基金 A 的历史数据)
DataFrame 2: 1500 行 (基金 B 的历史数据)
DataFrame 3: 800 行  (基金 C 的历史数据)
    ↓
合并后: 3300 行
```

### 4. 数据保存 (`ControlMongodb.save_dataframe_to_collection`)

**位置**: `app/services/database/control_mongodb.py`

#### 4.1 数据转换

**流程**:
```python
# 1. DataFrame 转为字典列表
records = df.to_dict("records")

# 2. 处理每条记录
for record in records:
    doc = dict(record)
    
    # 转换时间字段为 ISO 格式
    doc = self._convert_datetime_fields(doc)
    
    # 添加额外字段（如数据源、接口名称等）
    if extra_fields:
        doc.update(extra_fields)
```

#### 4.2 构建更新操作

**唯一键配置**:
- 对于 `fund_etf_fund_info_em`: `["基金代码", "净值日期"]`
- 用于判断数据是否已存在

**构建过滤条件** (`_build_filter`):
```python
def _build_filter(self, doc: Dict) -> Dict:
    filter_doc = {}
    for key in self.unique_keys:  # ["基金代码", "净值日期"]
        value = doc.get(key)
        if value is not None:
            # 处理日期类型
            if isinstance(value, (date, datetime)):
                filter_doc[key] = value.isoformat()
            else:
                filter_doc[key] = str(value)
    return filter_doc
```

**构建更新操作** (`_build_update_operation`):
```python
def _build_update_operation(self, doc: Dict) -> UpdateOne:
    filter_doc = self._build_filter(doc)  # {"基金代码": "511280", "净值日期": "2024-01-01"}
    
    # 添加更新时间
    doc["更新时间"] = datetime.now().isoformat()
    
    # 使用 upsert 操作
    return UpdateOne(
        filter_doc,  # 查询条件
        {"$set": doc, "$setOnInsert": {"创建时间": ..., "创建人": ...}},
        upsert=True  # 不存在则插入，存在则更新
    )
```

#### 4.3 批量执行

**批量大小**: 1000 条/批

**流程**:
```python
ops = []  # 更新操作列表

for record in records:
    ops.append(self._build_update_operation(record))
    
    # 达到批量大小时执行
    if len(ops) >= 1000:
        result = await self.collection.bulk_write(ops, ordered=False)
        ops = []

# 处理剩余操作
if ops:
    result = await self.collection.bulk_write(ops, ordered=False)
```

**MongoDB bulk_write 结果**:
- `upserted_count`: 新插入的文档数
- `matched_count`: 匹配到的文档数（已存在）
- `modified_count`: 实际更新的文档数（数据有变化）

**统计逻辑**:
```python
total_upserted = result["upserted"]  # 新增
total_modified = result["modified"]  # 更新（数据有变化）
unchanged = total_matched - total_modified  # 未变化（数据相同）
```

### 5. 去重逻辑

**去重机制**: 基于唯一键 (`unique_keys`)

**对于 `fund_etf_fund_info_em`**:
- 唯一键: `["基金代码", "净值日期"]`
- 含义: 同一个基金在同一天只能有一条记录

**去重流程**:
1. 构建查询条件: `{"基金代码": "511280", "净值日期": "2024-01-01"}`
2. 执行 upsert:
   - 如果不存在 → 插入新文档
   - 如果存在且数据不同 → 更新文档
   - 如果存在且数据相同 → 不更新（MongoDB 自动处理）

**示例**:
```
第一次保存:
  基金代码: 511280, 净值日期: 2024-01-01, 单位净值: 1.234
  → 插入新文档

第二次保存（相同基金代码和日期，但净值不同）:
  基金代码: 511280, 净值日期: 2024-01-01, 单位净值: 1.235
  → 更新现有文档

第三次保存（相同基金代码和日期，净值也相同）:
  基金代码: 511280, 净值日期: 2024-01-01, 单位净值: 1.235
  → 不更新（unchanged）
```

## 数据流示例

### 场景: 批量更新 1300 个基金的历史数据

```
1. 获取基金代码列表
   → 1300 个基金代码

2. 并发获取数据（并发数=3）
   → 3 个协程同时工作
   → 每个协程获取一个基金的数据
   → 获取到的 DataFrame 放入队列

3. 批量保存协程
   → 从队列取出 DataFrame
   → 累积到 5000 行或 5 秒后保存
   → 合并 DataFrame → 保存到 MongoDB

4. 保存过程
   → 1000 条/批执行 bulk_write
   → 根据唯一键去重
   → 统计新增/更新/未变化数量

5. 最终结果
   → 处理 1300 个任务
   → 保存 X 条数据（可能包含重复日期，会去重）
   → 实际保存 Y 个基金（不重复的基金代码数）
```

## 关键配置

### fund_etf_fund_info_em 服务配置

```python
class FundEtfFundInfoEmService(BaseService):
    collection_name = "fund_etf_fund_info_em"
    
    # 批量更新配置
    batch_source_collection = "fund_etf_fund_daily_em"  # 源集合
    batch_source_field = "基金代码"  # 从源集合获取的字段
    batch_concurrency = 3  # 并发数
    
    # 唯一键配置
    unique_keys = ["基金代码", "净值日期"]
    
    # 增量更新检查字段
    incremental_check_fields = ["基金代码"]
```

### 批量保存配置

```python
batch_size_threshold = 5000  # 达到 5000 条数据时批量保存
save_interval = 5.0  # 每 5 秒定期 flush
BATCH_SIZE = 1000  # MongoDB 批量写入大小
```

## 性能优化

1. **异步并发**: 使用 asyncio 并发获取数据
2. **批量写入**: 累积数据后批量保存，减少数据库操作
3. **批量大小**: 1000 条/批，平衡性能和内存
4. **定期 flush**: 5 秒间隔，避免数据积压
5. **去重优化**: 使用 MongoDB 的 upsert，避免先查询再插入

## 常见问题

### Q1: 为什么显示成功 1300 个，但只有 300 个基金？

**A**: 
- `success_count` 统计的是成功获取数据的任务数（1300 个基金代码）
- 实际基金数量是数据集合中不重复的基金代码数（300 个）
- 可能原因：
  1. 某些基金代码返回了数据，但"基金代码"字段为空或错误
  2. 某些基金代码返回了数据，但数据格式不正确，保存失败
  3. 数据去重时，某些基金代码的数据被覆盖或丢失

### Q2: 如何查看保存的详细日志？

**A**: 查看日志中的以下信息：
```
[fund_etf_fund_info_em] 批量保存完成: 新增=X, 更新=Y, 总行数=Z
[fund_etf_fund_info_em] 保存完成: 新增=X, 更新=Y, 未变化=Z, 总处理=W
```

### Q3: 数据保存失败怎么办？

**A**: 
1. 检查日志中的错误信息
2. 检查基金代码字段是否正确
3. 检查数据格式是否符合要求
4. 运行诊断脚本: `python scripts/diagnose_fund_etf_fund_info_em.py`

## 相关文件

- `app/services/data_sources/base_service.py` - 批量更新逻辑
- `app/services/database/control_mongodb.py` - 数据保存逻辑
- `app/services/data_sources/funds/services/fund_etf_fund_info_em_service.py` - 服务配置
- `scripts/diagnose_fund_etf_fund_info_em.py` - 诊断脚本

