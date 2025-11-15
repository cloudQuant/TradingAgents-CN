# 债券数据表结构设计文档

根据 AKShare 债券接口文档重新设计的数据库表结构。

## 1. 债券基础信息表 (bond_basic_info)

**数据来源**: `bond_zh_hs_cov_spot`, `bond_zh_hs_spot`

**唯一键**: `code`

| 字段名 | 类型 | 说明 | 来源字段 |
|--------|------|------|----------|
| code | string | 债券代码（标准化后） | 债券代码/可转债代码/code |
| raw_code | string | 原始代码 | - |
| name | string | 债券名称 | 债券名称/可转债名称/name |
| exchange | string | 交易所 (SH/SZ) | 从代码推断 |
| category | string | 类别 (convertible/exchangeable/interest/credit/other) | 从名称推断 |
| issuer | string | 发行人 | 发行人/发行主体 |
| list_date | string | 上市日期 (YYYY-MM-DD) | 上市日期/上市日 |
| maturity_date | string | 到期日 (YYYY-MM-DD) | 到期日/到期日期 |
| coupon_rate | float | 息票率 (%) | 票面利率/息票率 |
| source | string | 数据来源 | "akshare" |
| created_at | string | 创建时间 | ISO格式 |
| updated_at | string | 更新时间 | ISO格式 |

## 2. 债券历史行情表 (bond_daily)

**数据来源**: `bond_zh_hs_daily`, `bond_zh_hs_cov_daily`

**唯一键**: `(code, date)`

| 字段名 | 类型 | 说明 | 来源字段 |
|--------|------|------|----------|
| code | string | 债券代码 | - |
| date | string | 交易日期 (YYYY-MM-DD) | date |
| open | float | 开盘价 | open |
| high | float | 最高价 | high |
| low | float | 最低价 | low |
| close | float | 收盘价 | close |
| volume | float | 成交量 | volume |
| amount | float | 成交额（如果有） | amount |
| source | string | 数据来源 | "akshare" |

## 3. 债券现货报价表 (bond_spot_quotes)

**数据来源**: `bond_zh_hs_spot`, `bond_zh_hs_cov_spot`

**唯一键**: `(code, timestamp, category)`

| 字段名 | 类型 | 说明 | 来源字段 |
|--------|------|------|----------|
| code | string | 债券代码 | 代码/code |
| timestamp | string | 时间戳 | ticktime/时间 |
| category | string | 类别 | "convertible" / "other" |
| name | string | 债券名称 | 名称/name |
| latest_price | float | 最新价 | 最新价/trade |
| change | float | 涨跌额 | 涨跌额/pricechange |
| change_percent | float | 涨跌幅 | 涨跌幅 |
| buy | float | 买入价 | 买入 |
| sell | float | 卖出价 | 卖出 |
| prev_close | float | 昨收 | 昨收 |
| open | float | 今开 | 今开 |
| high | float | 最高 | 最高 |
| low | float | 最低 | 最低 |
| volume | int | 成交量 | 成交量/volume |
| amount | float | 成交额 | 成交额/amount |
| source | string | 数据来源 | "akshare" |

## 4. 收益率曲线表 (yield_curve_daily)

**数据来源**: `bond_china_yield`

**唯一键**: `(date, tenor, curve_name)`

| 字段名 | 类型 | 说明 | 来源字段 |
|--------|------|------|----------|
| date | string | 日期 (YYYY-MM-DD) | 日期 |
| curve_name | string | 曲线名称 | 曲线名称 |
| tenor | string | 期限 | 3月/6月/1年/3年/5年/7年/10年/30年等 |
| yield | float | 收益率 (%) | 对应期限的收益率值 |
| source | string | 数据来源 | "akshare" |

## 5. 债券详细信息表 (bond_info_cm)

**数据来源**: `bond_info_detail_cm`

**唯一键**: `(code, endpoint)`

| 字段名 | 类型 | 说明 | 来源字段 |
|--------|------|------|----------|
| code | string | 债券代码 | bondCode/债券代码 |
| endpoint | string | 接口标识 | "bond_info_detail_cm" |
| [其他字段] | any | 所有其他字段从 name-value 对展开 | name-value 键值对 |
| source | string | 数据来源 | "akshare" |

**说明**: 此表存储键值对格式的详细信息，字段名直接从 name 字段映射。

## 6. 债券中债查询结果表 (bond_info_cm_query)

**数据来源**: `bond_info_cm`

**唯一键**: `(code, endpoint)`

| 字段名 | 类型 | 说明 | 来源字段 |
|--------|------|------|----------|
| code | string | 债券代码 | 债券代码 |
| endpoint | string | 接口标识 | "bond_info_cm_query" |
| bond_name | string | 债券简称 | 债券简称 |
| issuer | string | 发行人/受托机构 | 发行人/受托机构 |
| bond_type | string | 债券类型 | 债券类型 |
| issue_date | string | 发行日期 | 发行日期 |
| latest_rating | string | 最新债项评级 | 最新债项评级 |
| query_code | string | 查询代码 | 查询代码 |
| source | string | 数据来源 | "akshare" |

## 数据迁移说明

旧数据可以删除，因为：
1. 数据来源都是 AKShare，可以重新获取
2. 新结构更好地匹配接口返回的字段
3. 字段映射更加清晰和准确

## 索引设计

```javascript
// bond_basic_info
db.bond_basic_info.createIndex({ "code": 1 }, { unique: true });
db.bond_basic_info.createIndex({ "category": 1 });
db.bond_basic_info.createIndex({ "exchange": 1 });
db.bond_basic_info.createIndex({ "maturity_date": 1 });
db.bond_basic_info.createIndex({ "name": 1 });

// bond_daily
db.bond_daily.createIndex({ "code": 1, "date": 1 }, { unique: true });
db.bond_daily.createIndex({ "date": 1 });

// yield_curve_daily
db.yield_curve_daily.createIndex({ "date": 1, "tenor": 1, "curve_name": 1 }, { unique: true });
db.yield_curve_daily.createIndex({ "date": 1 });
db.yield_curve_daily.createIndex({ "curve_name": 1 });

// bond_spot_quotes
db.bond_spot_quotes.createIndex({ "code": 1, "timestamp": 1, "category": 1 }, { unique: true });
db.bond_spot_quotes.createIndex({ "timestamp": 1 });

// bond_info_cm
db.bond_info_cm.createIndex({ "code": 1 });
db.bond_info_cm.createIndex({ "code": 1, "endpoint": 1 }, { unique: true });
```

