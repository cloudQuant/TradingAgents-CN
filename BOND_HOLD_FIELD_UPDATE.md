# 债券持仓字段统一说明

## 修改日期
2024-11-25

## 问题描述
`fund_portfolio_bond_hold_em` 数据表字段中英文混乱，存在重复字段。

## 原始字段结构

### AKShare API 返回字段（全部中文）
```python
['序号', '债券代码', '债券名称', '占净值比例', '持仓市值', '季度']
```

### 原保存逻辑添加的字段
```python
{
    '序号': 1,               # ❌ 不需要保存
    '基金代码': '000001',
    '债券代码': '019666',
    '债券名称': '22国债14',
    '占净值比例': 5.66,
    '持仓市值': 14225.50,
    '季度': '2024年4季度债券投资明细',
    
    # 重复的英文字段 ❌
    'code': '000001',        # 与 '基金代码' 重复
    'bond_code': '019666',   # 与 '债券代码' 重复
    'quarter': '2024...',    # 与 '季度' 重复
    
    # 元数据字段（英文）❌
    'source': 'akshare',
    'endpoint': 'fund_portfolio_bond_hold_em',
    'updated_at': '2024-11-25T00:45:00'
}
```

## 修改后字段结构

### 统一使用中文字段名
```python
{
    '基金代码': '000001',
    '债券代码': '019666',
    '债券名称': '22国债14',
    '占净值比例': 5.66,
    '持仓市值': 14225.50,
    '季度': '2024年4季度债券投资明细',
    
    # 元数据字段（统一使用中文）✅
    '数据源': 'akshare',
    '接口名称': 'fund_portfolio_bond_hold_em',
    '更新时间': '2024-11-25T00:45:00'
}
```

## 修改内容

### 1. 数据保存逻辑 (`app/services/fund_data_service.py`)

**修改前：**
```python
fund_code = str(doc.get('基金代码', ''))
bond_code = str(doc.get('债券代码', ''))
quarter = str(doc.get('季度', ''))
doc['code'] = fund_code
doc['bond_code'] = bond_code
doc['quarter'] = quarter
doc['source'] = 'akshare'
doc['endpoint'] = 'fund_portfolio_bond_hold_em'
doc['updated_at'] = datetime.now().isoformat()

ops.append(
    UpdateOne(
        {'code': fund_code, 'bond_code': bond_code, 'quarter': quarter},
        {'$set': doc},
        upsert=True
    )
)
```

**修改后：**
```python
# 使用中文字段名
fund_code = str(doc.get('基金代码', ''))
bond_code = str(doc.get('债券代码', ''))
quarter = str(doc.get('季度', ''))

# 添加元数据字段（使用中文）✅
doc['数据源'] = 'akshare'
doc['接口名称'] = 'fund_portfolio_bond_hold_em'
doc['更新时间'] = datetime.now().isoformat()

# 删除序号字段（不需要保存）✅
doc.pop('序号', None)

ops.append(
    UpdateOne(
        {'基金代码': fund_code, '债券代码': bond_code, '季度': quarter},
        {'$set': doc},
        upsert=True
    )
)
```

### 2. 统计方法更新

**修改前：**
```python
unique_funds = await self.col_fund_portfolio_bond_hold_em.distinct('code')
unique_bonds = await self.col_fund_portfolio_bond_hold_em.distinct('bond_code')
```

**修改后：**
```python
unique_funds = await self.col_fund_portfolio_bond_hold_em.distinct('基金代码')
unique_bonds = await self.col_fund_portfolio_bond_hold_em.distinct('债券代码')
```

## 字段对照表

| 原字段（英文）| 新字段（中文）| 说明 |
|------------|------------|------|
| `code` | `基金代码` | 删除重复的英文字段 |
| `bond_code` | `债券代码` | 删除重复的英文字段 |
| `quarter` | `季度` | 删除重复的英文字段 |
| `序号` | ~~删除~~ | 不需要保存到数据库 |
| `source` | `数据源` | 翻译为中文 |
| `endpoint` | `接口名称` | 翻译为中文 |
| `updated_at` | `更新时间` | 翻译为中文 |

## 数据示例

### 完整数据记录
```json
{
    "_id": "ObjectId(...)",
    "基金代码": "000001",
    "债券代码": "240401",
    "债券名称": "24农发01",
    "占净值比例": 5.66,
    "持仓市值": 14225.50,
    "季度": "2024年4季度债券投资明细",
    "数据源": "akshare",
    "接口名称": "fund_portfolio_bond_hold_em",
    "更新时间": "2024-11-25T00:45:00.123456"
}
```

## 唯一标识

使用三个字段组合作为唯一标识：
- `基金代码`
- `债券代码`
- `季度`

## 数据迁移

### 对于已有数据
旧数据可以保留，新数据会使用新字段结构。如需清理旧字段，可执行：

```python
# 删除重复的英文字段
await col.update_many(
    {},
    {'$unset': {
        'code': '',
        'bond_code': '',
        'quarter': '',
        'source': '',
        'endpoint': '',
        'updated_at': '',
        '序号': ''
    }}
)
```

### 或者清空重新导入
```python
# 清空所有数据
await fund_data_service.clear_fund_portfolio_bond_hold_em_data()

# 重新批量更新
# 使用前端界面或API触发批量更新
```

## 影响范围

### 后端
- ✅ `save_fund_portfolio_bond_hold_em_data` - 已更新
- ✅ `get_fund_portfolio_bond_hold_em_stats` - 已更新
- ✅ MongoDB查询和聚合 - 使用中文字段名

### 前端
- ✅ 前端查询和显示已经使用中文字段名，无需修改

### API
- ✅ API返回的数据结构保持不变

## 优势

1. **一致性**：所有字段使用统一的中文命名
2. **可读性**：数据库中的数据更易读
3. **无冗余**：删除了重复的英文字段
4. **易维护**：字段名与API返回结构保持一致

## 相关文件

- 数据服务：`app/services/fund_data_service.py`
  - `save_fund_portfolio_bond_hold_em_data` (行8627-8705)
  - `get_fund_portfolio_bond_hold_em_stats` (行8718-8750)
- 测试脚本：`test_akshare_bond_hold.py`

## 注意事项

1. ⚠️ 旧数据仍包含英文字段，可选择性清理
2. ⚠️ 如果有其他服务依赖英文字段，需要同步更新
3. ⚠️ 建议在清理旧数据前做好备份

---

**版本**: 1.0.0  
**更新日期**: 2024-11-25  
**维护者**: TradingAgents-CN Team
