# Bug修复: MongoDB无法编码datetime.date对象

## 问题描述

在更新基金申购状态数据时，出现以下错误：

```
Invalid document {'q': {'code': '000005', 'date': '11-21'}, 'u': {'$set': {..., '下一开放日': datetime.date(2025, 12, 8), ...}}, ...} | cannot encode object: datetime.date(2025, 12, 8), of type: <class 'datetime.date'>
```

## 错误原因

从AKShare获取的数据中，某些字段（如`下一开放日`）的值是Python的`datetime.date`对象。MongoDB的pymongo驱动无法直接编码`datetime.date`类型，只能编码以下类型：
- 字符串 (str)
- datetime.datetime 对象
- None
- 数字等基本类型

## 影响范围

所有从AKShare获取包含日期字段的基金数据保存操作都可能受此问题影响：
1. ✅ `save_fund_purchase_status_data` - 基金申购状态（包含`下一开放日`等日期字段）
2. ✅ `save_fund_name_em_data` - 基金基本信息
3. ✅ `save_fund_basic_info_data` - 基金详细信息
4. ✅ `save_fund_info_index_data` - 指数型基金信息

## 修复方案

在所有数据保存方法中，添加日期类型检测和转换逻辑：

```python
import datetime as dt

for key, value in list(doc.items()):
    # 原有的NaN/Infinity清理逻辑
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        try:
            if math.isnan(value) or math.isinf(value):
                doc[key] = None
        except (TypeError, ValueError):
            pass
    # 新增：转换 datetime.date 对象为字符串
    elif isinstance(value, dt.date) and not isinstance(value, dt.datetime):
        doc[key] = value.strftime('%Y-%m-%d')
    # 新增：转换 datetime.datetime 对象为字符串
    elif isinstance(value, dt.datetime):
        doc[key] = value.strftime('%Y-%m-%d')
```

### 修复要点

1. **检查顺序很重要**：
   - 先检查 `datetime.date` (必须排除 `datetime.datetime`)
   - 再检查 `datetime.datetime`
   - 因为 `datetime.datetime` 是 `datetime.date` 的子类

2. **转换格式**：
   - 统一使用 `'%Y-%m-%d'` 格式（如：`2025-12-08`）
   - 保持与其他日期字段一致

3. **保持None值**：
   - 如果日期字段为None，不做转换
   - 避免引入新的错误

## 修复的文件

**文件**: `app/services/fund_data_service.py`

**修改的方法**:
1. `save_fund_purchase_status_data` (第642-662行)
2. `save_fund_name_em_data` (第64-84行)
3. `save_fund_basic_info_data` (第223-243行)
4. `save_fund_info_index_data` (第376-395行)

## 验证方法

### 1. 单元测试验证
```bash
# 运行基金申购状态测试
pytest tests/funds/test_fund_purchase_status.py::TestFundPurchaseStatusBackend::test_save_fund_purchase_data -v
```

### 2. 手动测试验证
```bash
# 1. 启动后端服务
python main.py

# 2. 启动前端服务
cd frontend && npm run dev

# 3. 访问页面并测试
# http://localhost:5173/funds/collections/fund_purchase_status
# 点击"更新数据" -> "开始更新"
# 应该能成功保存数据，不再出现 datetime.date 编码错误
```

### 3. 验证数据
```python
# 连接MongoDB检查保存的数据
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['tradingagents']
collection = db['fund_purchase_status']

# 查看一条记录
doc = collection.find_one({'基金代码': '000005'})
print(doc)

# 验证 '下一开放日' 字段是字符串类型
print(f"下一开放日: {doc['下一开放日']}, 类型: {type(doc['下一开放日'])}")
# 应该输出: 下一开放日: 2025-12-08, 类型: <class 'str'>
```

## 测试用例

### 正常情况 - 包含日期字段
```python
import pandas as pd
from datetime import date

# 创建包含datetime.date的测试数据
test_df = pd.DataFrame([{
    '基金代码': '000005',
    '基金简称': '测试基金',
    '下一开放日': date(2025, 12, 8),  # datetime.date对象
    '申购状态': '开放申购',
    '赎回状态': '开放赎回'
}])

# 应该能成功保存，不抛出异常
service = FundDataService(db)
result = await service.save_fund_purchase_status_data(test_df)
assert result == 1
```

### 边界情况 - None值
```python
# 日期字段为None
test_df = pd.DataFrame([{
    '基金代码': '000006',
    '基金简称': '测试基金2',
    '下一开放日': None,  # None值应该保持不变
    '申购状态': '开放申购'
}])

result = await service.save_fund_purchase_status_data(test_df)
assert result == 1
```

## 预防措施

### 1. 在数据获取时就进行转换
可以考虑在AKShare数据获取后立即转换日期类型：

```python
async def _fetch_fund_purchase_em():
    df = await asyncio.get_event_loop().run_in_executor(
        executor, ak.fund_purchase_em
    )
    
    # 立即转换日期列
    date_columns = ['下一开放日', '最新净值/万份收益-报告时间']
    for col in date_columns:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: x.strftime('%Y-%m-%d') if isinstance(x, date) else x
            )
    
    return df
```

### 2. 添加类型检查测试
```python
def test_no_datetime_objects_in_saved_data():
    """确保保存到数据库的数据不包含datetime对象"""
    from datetime import date, datetime
    
    # 获取刚保存的数据
    doc = collection.find_one()
    
    # 递归检查所有值
    def check_no_datetime(obj):
        if isinstance(obj, dict):
            for v in obj.values():
                check_no_datetime(v)
        elif isinstance(obj, list):
            for item in obj:
                check_no_datetime(item)
        elif isinstance(obj, (date, datetime)):
            raise AssertionError(f"Found datetime object: {obj}")
    
    check_no_datetime(doc)
```

## 总结

### 修复内容
- ✅ 为所有基金数据保存方法添加日期类型转换
- ✅ 统一日期格式为 'YYYY-MM-DD'
- ✅ 保持与现有代码风格一致
- ✅ 不影响其他功能

### 影响
- ✅ 无破坏性改动
- ✅ 只是增加了类型转换逻辑
- ✅ 提高了代码的健壮性
- ✅ 解决了MongoDB编码错误

### 后续建议
1. 考虑在数据获取层就进行日期转换
2. 添加自动化测试验证日期字段的类型
3. 在文档中明确说明日期字段的存储格式
4. 考虑使用Pydantic模型进行数据验证

## 验收标准

- ✅ 更新基金申购状态数据不再出现 datetime.date 编码错误
- ✅ 所有日期字段正确保存为字符串格式
- ✅ 现有功能不受影响
- ✅ 单元测试通过
