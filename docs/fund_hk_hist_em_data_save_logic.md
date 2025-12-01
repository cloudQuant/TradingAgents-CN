# 香港基金历史数据保存逻辑说明

## 数据保存流程

### 1. 批量更新任务生成

在 `fund_hk_hist_em_service.py` 中，`_get_tasks_to_process` 方法为每个基金代码生成**两个任务**：

```python
# 例如基金代码 "1002200683" 会生成：
任务1: (code="1002200683", symbol="历史净值明细")
任务2: (code="1002200683", symbol="分红送配详情")
```

### 2. 数据获取和保存流程

每个任务独立执行以下步骤：

#### 步骤 1: 调用 Provider 获取数据
```python
# 任务1: 获取历史净值明细
df1 = provider.fetch_data(code="1002200683", symbol="历史净值明细")

# 任务2: 获取分红送配详情
df2 = provider.fetch_data(code="1002200683", symbol="分红送配详情")
```

#### 步骤 2: Provider 自动添加参数列

在 `fund_hk_hist_em_provider.py` 中配置了 `add_param_columns`：

```python
add_param_columns = {
    "code": "code",      # 将 code 参数值写入 "code" 列
    "symbol": "symbol",  # 将 symbol 参数值写入 "symbol" 列
}
```

Provider 的 `_add_param_columns` 方法会自动将参数值添加到 DataFrame：

**任务1 的 DataFrame**:
```
| code       | symbol      | 净值日期   | 单位净值 | 日增长值 | ... |
|------------|-------------|------------|----------|----------|-----|
| 1002200683 | 历史净值明细 | 2024-01-01 | 1.2345    | 0.0012   | ... |
| 1002200683 | 历史净值明细 | 2024-01-02 | 1.2356    | 0.0011   | ... |
```

**任务2 的 DataFrame**:
```
| code       | symbol      | 净值日期   | 权益登记日 | 除息日期 | 分红金额 | ... |
|------------|-------------|------------|------------|----------|----------|-----|
| 1002200683 | 分红送配详情 | 2024-01-15 | 2024-01-10 | 2024-01-11 | 0.05    | ... |
```

#### 步骤 3: 保存到数据库

每个任务获取数据后，立即调用 `control_db.save_dataframe_to_collection(df)` 保存：

```python
# 在 base_service.py 的 process_task 中
result = await control_db.save_dataframe_to_collection(
    df,
    extra_fields=extra_fields
)
```

### 3. 数据去重机制

#### 唯一键配置

```python
unique_keys = ["code", "symbol", "净值日期"]
```

#### MongoDB Upsert 操作

`ControlMongodb` 使用 MongoDB 的 `upsert` 操作：

```python
UpdateOne(
    filter={"code": "1002200683", "symbol": "历史净值明细", "净值日期": "2024-01-01"},
    update={"$set": {...}},
    upsert=True  # 如果不存在则插入，存在则更新
)
```

### 4. 数据分离保证

由于唯一键包含 `symbol` 字段，**净值数据和分红数据会被分别保存**，不会互相覆盖：

- **净值数据记录**:
  ```json
  {
    "code": "1002200683",
    "symbol": "历史净值明细",
    "净值日期": "2024-01-01",
    "单位净值": 1.2345,
    "日增长值": 0.0012,
    ...
  }
  ```

- **分红数据记录**:
  ```json
  {
    "code": "1002200683",
    "symbol": "分红送配详情",
    "净值日期": "2024-01-15",
    "权益登记日": "2024-01-10",
    "除息日期": "2024-01-11",
    "分红金额": 0.05,
    ...
  }
  ```

### 5. 并发安全性

- 每个任务独立保存，使用 MongoDB 的原子操作保证数据一致性
- 即使两个任务同时保存同一基金的数据，由于 `symbol` 不同，不会产生冲突
- 如果同一天的数据已存在，会进行更新而不是重复插入

## 数据查询示例

### 查询某个基金的所有净值数据
```python
collection.find({
    "code": "1002200683",
    "symbol": "历史净值明细"
})
```

### 查询某个基金的所有分红数据
```python
collection.find({
    "code": "1002200683",
    "symbol": "分红送配详情"
})
```

### 查询某个基金的所有数据（净值+分红）
```python
collection.find({
    "code": "1002200683"
})
```

## 总结

✅ **数据正确保存**：每个任务的数据都会通过 `add_param_columns` 自动添加 `code` 和 `symbol` 字段

✅ **数据不会冲突**：由于唯一键包含 `symbol`，净值数据和分红数据会分别保存

✅ **数据不会重复**：使用 `(code, symbol, 净值日期)` 作为唯一键，同一天的数据会更新而不是重复插入

✅ **并发安全**：每个任务独立保存，MongoDB 的原子操作保证数据一致性


