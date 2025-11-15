# 为什么37个债券接口只形成26个集合？

## 原因分析

37个接口映射到26个集合，主要是因为**多个接口的数据结构相似，可以合并存储在同一集合中，通过特定字段进行区分**。这是数据库设计的常见优化策略，可以减少集合数量，提高查询效率，同时保持数据的逻辑清晰。

## 详细映射关系

### 1. 合并存储的接口组（11组，共22个接口）

#### 组1: 现货报价集合 (`bond_spot_quotes`) - 2个接口
- `bond_zh_hs_spot` → `bond_spot_quotes` (category="hs_spot")
- `bond_zh_hs_cov_spot` → `bond_spot_quotes` (category="cov_spot")

**合并原因**: 都是现货报价数据，结构相同，通过 `category` 字段区分债券类型。

#### 组2: 历史行情集合 (`bond_daily`) - 2个接口
- `bond_zh_hs_daily` → `bond_daily`
- `bond_zh_hs_cov_daily` → `bond_daily`

**合并原因**: 都是日线历史行情数据，结构相同（date, open, high, low, close, volume等），通过 `code` 字段自然区分（代码本身就不同）。

#### 组3: 收益率曲线集合 (`yield_curve_daily`) - 2个接口
- `bond_china_yield` → `yield_curve_daily` (yield_type为空或默认)
- `bond_china_close_return` → `yield_curve_daily` (yield_type="到期收益率"或"即期收益率")

**合并原因**: 都是收益率曲线数据，结构相同（date, tenor, yield），通过 `yield_type` 字段区分收益率类型。

#### 组4: 中债信息集合 (`bond_info_cm`) - 2个接口
- `bond_info_cm` → `bond_info_cm` (endpoint="bond_info_cm")
- `bond_info_detail_cm` → `bond_info_cm` (endpoint="bond_info_detail_cm")

**合并原因**: 都是中债信息数据，通过 `endpoint` 字段区分查询结果和详细信息。

#### 组5: 债券发行集合 (`bond_issues`) - 5个接口
- `bond_treasure_issue_cninfo` → `bond_issues` (issue_type="treasure")
- `bond_local_government_issue_cninfo` → `bond_issues` (issue_type="local_government")
- `bond_corporate_issue_cninfo` → `bond_issues` (issue_type="corporate")
- `bond_cov_issue_cninfo` → `bond_issues` (issue_type="cov")
- `bond_cov_stock_issue_cninfo` → `bond_issues` (issue_type="cov_stock")

**合并原因**: 都是债券发行公告数据，结构相同，通过 `issue_type` 字段区分债券类型。

#### 组6: 债券回购集合 (`bond_buybacks`) - 2个接口
- `bond_sh_buy_back_em` → `bond_buybacks` (exchange="SH")
- `bond_sz_buy_back_em` → `bond_buybacks` (exchange="SZ")

**合并原因**: 都是回购数据，结构相同，通过 `exchange` 字段区分交易所。

#### 组7: 分钟数据集合 (`bond_minute_quotes`) - 2个接口
- `bond_zh_hs_cov_min` → `bond_minute_quotes` (period="1", pre_minute=false)
- `bond_zh_hs_cov_pre_min` → `bond_minute_quotes` (period="1", pre_minute=true)

**合并原因**: 都是分钟级分时数据，结构相同，通过 `period` 和 `pre_minute` 字段区分。

#### 组8: 可转债档案集合 (`bond_cb_profiles`) - 3个接口
- `bond_cb_profile_sina` → `bond_cb_profiles` (provider="sina", endpoint="bond_cb_profile_sina")
- `bond_zh_cov_info` → `bond_cb_profiles` (provider="eastmoney", endpoint="bond_zh_cov_info")
- `bond_zh_cov_info_ths` → `bond_cb_profiles` (provider="ths", endpoint="bond_zh_cov_info_ths")

**合并原因**: 都是可转债详情信息，结构相似，通过 `provider` 和 `endpoint` 字段区分数据源。

#### 组9: 债券指数集合 (`bond_indices_daily`) - 2个接口
- `bond_new_composite_index_cbond` → `bond_indices_daily` (index_id="新综合指数")
- `bond_composite_index_cbond` → `bond_indices_daily` (index_id="综合指数")

**合并原因**: 都是债券指数数据，结构相同（date, value），通过 `index_id` 字段区分指数类型。

### 2. 独立存储的接口（15个接口，15个集合）

这些接口的数据结构独特，不适合合并：

1. `bond_basic_info` - 债券基础信息（来自多个接口的汇总）
2. `bond_cash_summary` - 上交所现券市场概览
3. `bond_deal_summary` - 上交所成交概览
4. `bond_nafmii_debts` - 银行间市场债务
5. `bond_spot_quote_detail` - 现货报价明细
6. `bond_spot_deals` - 现货成交明细
7. `bond_cov_list` - 可转债列表
8. `bond_cb_list_jsl` - 集思录可转债
9. `bond_cb_summary` - 可转债债券概况
10. `bond_cb_valuation_daily` - 可转债估值
11. `bond_cb_comparison` - 可转债比价表
12. `bond_cb_adjustments` - 可转债转股价格调整
13. `bond_cb_redeems` - 可转债强赎
14. `bond_buybacks_hist` - 债券回购历史
15. `us_yield_daily` - 美国国债收益率
16. `bond_events` - 债券事件
17. `yield_curve_map` - 收益率曲线映射

## 合并存储的优势

### 1. **减少集合数量**
- 从37个集合减少到26个集合
- 降低数据库管理复杂度

### 2. **统一查询接口**
- 相同类型的数据可以在一个集合中统一查询
- 例如：查询所有现货报价，只需查询 `bond_spot_quotes` 集合，通过 `category` 过滤

### 3. **提高查询效率**
- 可以建立统一的索引
- 减少跨集合查询的复杂度

### 4. **数据一致性**
- 相同类型的数据使用相同的字段结构
- 便于数据验证和清洗

### 5. **灵活的数据区分**
- 通过字段（如 `category`, `issue_type`, `exchange`）区分不同来源
- 可以轻松添加新的数据源类型

## 数据区分机制

每个合并的集合都通过以下机制区分不同接口的数据：

| 集合名称 | 区分字段 | 字段值 |
|---------|---------|--------|
| `bond_spot_quotes` | `category` | "hs_spot", "cov_spot" |
| `bond_daily` | `code` | 代码本身不同 |
| `yield_curve_daily` | `yield_type`, `curve_name` | "到期收益率", "即期收益率"等 |
| `bond_info_cm` | `endpoint` | "bond_info_cm", "bond_info_detail_cm" |
| `bond_issues` | `issue_type` | "treasure", "local_government", "corporate", "cov", "cov_stock" |
| `bond_buybacks` | `exchange` | "SH", "SZ" |
| `bond_minute_quotes` | `period`, `pre_minute` | period="1", pre_minute=true/false |
| `bond_cb_profiles` | `provider`, `endpoint` | "sina", "eastmoney", "ths" |
| `bond_indices_daily` | `index_id` | "新综合指数", "综合指数" |

## 查询示例

### 查询所有现货报价
```python
# 查询所有现货报价（包括普通债券和可转债）
db.bond_spot_quotes.find({})

# 只查询可转债现货报价
db.bond_spot_quotes.find({"category": "cov_spot"})

# 只查询普通债券现货报价
db.bond_spot_quotes.find({"category": "hs_spot"})
```

### 查询所有债券发行
```python
# 查询所有债券发行
db.bond_issues.find({})

# 只查询国债发行
db.bond_issues.find({"issue_type": "treasure"})

# 只查询可转债发行
db.bond_issues.find({"issue_type": "cov"})
```

## 总结

37个接口映射到26个集合是合理的数据库设计：

1. **11组接口（22个）** 合并存储，通过字段区分
2. **15个接口** 独立存储，因为数据结构独特
3. **合并存储** 提高了查询效率和数据管理便利性
4. **字段区分** 机制保证了数据的准确性和可追溯性

这种设计既保持了数据的逻辑清晰，又提高了系统的可维护性和查询效率。

