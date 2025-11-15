# 债券数据表结构重新设计总结

## 概述

根据 AKShare 债券接口文档，重新设计了债券数据表结构，使其更准确地匹配接口返回的字段格式。

## 主要改进

### 1. 债券基础信息表 (bond_basic_info)

**改进点**:
- 使用 `code` 作为唯一键
- 规范化代码格式
- 添加 `created_at` 和 `updated_at` 时间戳
- 支持更新逻辑：存在则更新，不存在则插入

**字段映射**:
- `债券代码` / `可转债代码` / `code` → `code`
- `债券名称` / `可转债名称` / `name` → `name`
- `发行人` / `发行主体` → `issuer`
- `上市日期` / `上市日` → `list_date`
- `到期日` / `到期日期` → `maturity_date`
- `票面利率` / `息票率` → `coupon_rate`

### 2. 债券历史行情表 (bond_daily)

**改进点**:
- 使用 `(code, date)` 作为唯一键
- 标准化字段名：open, high, low, close, volume
- 支持多种日期格式转换

### 3. 债券现货报价表 (bond_spot_quotes)

**改进点**:
- 使用 `(code, timestamp, category)` 作为唯一键
- 字段映射：中文字段名 → 英文标准字段名
- 支持可转债和普通债券的报价数据

**字段映射**:
- `最新价` / `trade` → `latest_price`
- `涨跌额` / `pricechange` → `change`
- `涨跌幅` → `change_percent`
- `买入` → `buy`
- `卖出` → `sell`
- `昨收` / `preclose` → `prev_close`
- `今开` / `open` → `open`
- `最高` / `high` → `high`
- `最低` / `low` → `low`
- `成交量` / `volume` → `volume`
- `成交额` / `amount` → `amount`

### 4. 收益率曲线表 (yield_curve_daily)

**改进点**:
- 使用 `(date, tenor, curve_name)` 作为唯一键
- 支持多个曲线类型（国债、中短期票据、商业银行债等）
- 正确分离曲线名称和期限
- 过滤非数值数据

**数据结构**:
- `date`: 日期
- `curve_name`: 曲线名称（如"中债国债收益率曲线"）
- `tenor`: 期限（如"3月"、"6月"、"1年"等）
- `yield`: 收益率数值（%）

### 5. 债券详细信息表 (bond_info_cm)

**改进点**:
- 使用 `(code, endpoint)` 作为唯一键
- 支持键值对格式的详细信息
- 自动展开 name-value 对为字段

## 数据迁移步骤

### 1. 备份现有数据（可选）

```bash
# 使用 MongoDB 导出
mongodump --db=your_database --collection=bond_basic_info --out=./backup
```

### 2. 清理旧数据

```bash
# 运行清理脚本
python scripts/cleanup_bond_data.py
```

或者手动清理：

```python
from app.core.database import get_mongo_db

db = get_mongo_db()
collections = ["bond_basic_info", "bond_daily", "yield_curve_daily", ...]
for col_name in collections:
    await db.get_collection(col_name).delete_many({})
```

### 3. 重新同步数据

运行以下同步任务：

1. **债券基础信息同步** - 获取所有债券列表
2. **债券收益率曲线同步** - 获取收益率曲线数据
3. **债券历史数据同步** - 获取历史行情数据（按需）
4. **中债信息详情同步** - 获取详细信息

## 字段映射对照表

### bond_zh_hs_spot (债券现货)

| AKShare字段 | 标准字段 | 说明 |
|------------|---------|------|
| 代码 | code | 债券代码 |
| 名称 | name | 债券名称 |
| 最新价 | latest_price | 最新价格 |
| 涨跌额 | change | 涨跌金额 |
| 涨跌幅 | change_percent | 涨跌百分比 |
| 买入 | buy | 买入价 |
| 卖出 | sell | 卖出价 |
| 昨收 | prev_close | 昨日收盘价 |
| 今开 | open | 今日开盘价 |
| 最高 | high | 最高价 |
| 最低 | low | 最低价 |
| 成交量 | volume | 成交量（手） |
| 成交额 | amount | 成交额（万元） |

### bond_zh_hs_cov_spot (可转债现货)

| AKShare字段 | 标准字段 | 说明 |
|------------|---------|------|
| symbol | code | 债券代码 |
| name | name | 债券名称 |
| trade | latest_price | 最新价格 |
| pricechange | change | 涨跌金额 |
| volume | volume | 成交量 |
| amount | amount | 成交额 |
| ticktime | timestamp | 时间戳 |

### bond_china_yield (收益率曲线)

| AKShare字段 | 标准字段 | 说明 |
|------------|---------|------|
| 曲线名称 | curve_name | 收益率曲线名称 |
| 日期 | date | 日期 |
| 3月/6月/1年/... | tenor | 期限 |
| [对应期限的值] | yield | 收益率数值 |

### bond_info_detail_cm (债券详情)

返回格式为 name-value 键值对，需要展开为字段。

## 索引优化

### bond_basic_info
- 唯一索引: `code`
- 普通索引: `category`, `exchange`, `maturity_date`, `list_date`, `name`

### bond_daily
- 唯一索引: `(code, date)`
- 普通索引: `date`

### yield_curve_daily
- 唯一索引: `(date, tenor, curve_name)`
- 普通索引: `date`, `curve_name`, `(date, tenor)`

### bond_spot_quotes
- 唯一索引: `(code, timestamp, category)`
- 普通索引: `timestamp`

### bond_info_cm
- 唯一索引: `(code, endpoint)`
- 普通索引: `code`

## 注意事项

1. **代码规范化**: 所有债券代码都会通过 `normalize_bond_code` 规范化
2. **日期格式**: 统一使用 `YYYY-MM-DD` 格式
3. **字段类型**: 
   - 收益率和利率使用 `float` 类型（百分比数值，如 3.5 表示 3.5%）
   - 日期使用 `string` 类型
   - 代码使用 `string` 类型
4. **唯一键设计**: 根据业务逻辑选择合适的组合键，确保数据唯一性
5. **数据验证**: 保存前会验证数据格式和类型，跳过无效数据

## 测试建议

清理和重新同步后，建议：

1. 检查数据完整性：验证各表的数据量
2. 测试查询功能：确保前端页面能正常显示数据
3. 验证字段映射：确认字段正确映射和显示
4. 检查唯一约束：确保没有重复数据

## 相关文档

- [数据表结构设计](./bond_database_schema.md)
- [数据迁移指南](./bond_data_migration.md)
- [债券数据同步指南](./bonds_data_sync_guide.md)

