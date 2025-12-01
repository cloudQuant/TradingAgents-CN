# 基金历史行情-新浪 实现说明

## 概述
`fund_hist_sina` 数据集合已完整实现基金代码字段和唯一标识功能。

## 数据结构

### AKShare API
- **接口**: `ak.fund_etf_hist_sina(symbol='sh510050')`
- **参数**: symbol - 基金代码（如 sh510050）
- **返回字段**: 
  - `date` - 日期
  - `open` - 开盘价
  - `high` - 最高价
  - `low` - 最低价
  - `close` - 收盘价
  - `volume` - 成交量（单位：手）
- **注意**: API 不返回基金代码，需要手动添加

### 数据库存储字段
- `code` - 基金代码（手动添加）
- `date` - 日期
- `open` - 开盘价
- `high` - 最高价
- `low` - 最低价
- `close` - 收盘价
- `volume` - 成交量

### 唯一标识
- **组合键**: `code + date`
- **MongoDB 索引**: `{code: 1, date: 1}` (unique)

## 实现细节

### 1. 数据获取（刷新服务）
**文件**: `app/services/fund_refresh_service.py`

```python
# 单个基金更新
async def _refresh_fund_hist_sina(self, task_id: str, params: Dict[str, Any]):
    symbol = params.get('symbol')  # 如 'sh510050'
    
    # 调用 AKShare API
    df = await loop.run_in_executor(executor, self._fetch_fund_hist_sina, symbol)
    
    # ⭐ 关键步骤：添加基金代码字段
    df = df.copy()
    df["代码"] = symbol  # 添加中文列名
    
    # 保存数据
    await self.data_service.save_fund_hist_sina_data(df)
```

### 2. 数据保存（数据服务）
**文件**: `app/services/fund_data_service.py`

```python
async def save_fund_hist_sina_data(self, df: pd.DataFrame):
    # 字段映射：将中文列名转换为英文
    field_mapping = {
        "代码": "code",  # ⭐ 关键映射
        "date": "date",
        "日期": "date",
        # ... 其他字段映射
    }
    
    df = df.rename(columns=field_mapping)
    
    # 检查必需字段
    required_fields = ["date", "open", "high", "low", "close", "volume", "code"]
    
    # 构建 MongoDB 更新操作
    for idx, row in df.iterrows():
        code = str(row.get("code"))
        date_str = str(row.get("date"))
        
        record = {
            "code": code,
            "date": date_str,
            "open": float(row["open"]),
            # ... 其他字段
        }
        
        # ⭐ 关键：使用 code + date 作为唯一键
        ops.append(
            UpdateOne(
                {"code": code, "date": date_str},  # 唯一标识
                {"$set": record},
                upsert=True
            )
        )
    
    # 批量写入
    await self.col_fund_hist_sina.bulk_write(ops, ordered=False)
```

### 3. 路由定义
**文件**: `app/routers/funds.py`

```python
{
    "name": "fund_hist_sina",
    "display_name": "基金历史行情-新浪",
    "fields": [
        "code",    # ⭐ 基金代码字段
        "date",    # ⭐ 日期字段
        "open",
        "high",
        "low",
        "close",
        "volume",
    ],
}
```

## 数据流程

```
1. 用户请求更新 (symbol='sh510050')
   ↓
2. 调用 AKShare API
   ↓ 返回 [date, open, high, low, close, volume]
3. 添加基金代码字段
   ↓ 添加列 '代码' = 'sh510050'
4. 字段映射
   ↓ '代码' → 'code'
5. 数据验证
   ↓ 检查必需字段：code, date, ...
6. 构建 MongoDB 操作
   ↓ UpdateOne({code, date}, {$set: record}, upsert=True)
7. 批量写入数据库
   ↓ code + date 唯一标识，自动去重
8. 完成
```

## 更新方式

### 单个基金更新
```json
POST /api/funds/collections/fund_hist_sina/refresh
{
  "symbol": "sh510050"
}
```

### 批量更新
```json
POST /api/funds/collections/fund_hist_sina/refresh
{
  "symbols": ["sh510050", "sh510300", "sh510500"]
}
```

## 测试验证

### 运行测试
```bash
cd f:\source_code\TradingAgents-CN
python tests\funds\test_fund_hist_sina_code_date.py
```

### 测试覆盖
1. ✓ AKShare API 数据结构
2. ✓ 添加基金代码字段
3. ✓ 字段映射（代码 → code）
4. ✓ 唯一标识（code + date）
5. ✓ 数据保存结构

## 数据库索引

建议创建以下索引以优化查询性能：

```javascript
// MongoDB Shell
db.fund_hist_sina.createIndex({ code: 1, date: 1 }, { unique: true })
db.fund_hist_sina.createIndex({ code: 1 })
db.fund_hist_sina.createIndex({ date: 1 })
```

## 注意事项

1. **基金代码必须手动添加**
   - AKShare API 不返回基金代码
   - 刷新服务在获取数据后立即添加

2. **字段映射**
   - 中文字段 "代码" → 英文字段 "code"
   - 便于前端统一处理

3. **唯一标识**
   - 使用 code + date 组合键
   - 支持数据更新（upsert=True）
   - 同一基金同一日期只保留一条记录

4. **数据完整性**
   - 必须包含所有必需字段
   - code 和 date 不能为空
   - 数值字段自动处理 NaN/Inf

## 相关文件

- 需求文档: `tests/funds/requirements/14_基金历史行情-新浪.md`
- 测试文件: `tests/funds/test_fund_hist_sina_code_date.py`
- 刷新服务: `app/services/fund_refresh_service.py` (line 1863-2012)
- 数据服务: `app/services/fund_data_service.py` (line 2883-2990)
- 路由定义: `app/routers/funds.py` (line 244-257)

## 验收标准

✅ **已完成**:
1. 基金代码字段已添加
2. 使用 code + date 作为唯一标识
3. 数据保存逻辑正确
4. 测试用例全部通过
5. 支持单个和批量更新

## 总结

当前实现已完全符合需求：
- ✓ 增加基金代码字段
- ✓ 使用基金代码和日期作为唯一标识
- ✓ 支持数据去重和更新
- ✓ 完整的测试验证

无需额外优化，实现已经满足要求。
