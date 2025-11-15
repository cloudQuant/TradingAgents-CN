# AKShare 债券接口覆盖情况分析

## 概述

本文档分析了 AKShare 债券接口文档中的所有接口，检查其在代码中的实现情况，包括：
1. MongoDB 集合是否已创建
2. 是否已添加到定时任务中
3. 数据保存方法是否已实现

## 接口列表（共 37 个）

### 1. 中债信息接口

| 接口名称 | 集合名称 | 集合状态 | 定时任务 | 保存方法 | 状态 |
|---------|---------|---------|---------|---------|------|
| `bond_info_cm` | `bond_info_cm` | ✅ 已创建 | ✅ 已添加 | ✅ `save_info_cm_query` | ✅ 完整 |
| `bond_info_detail_cm` | `bond_info_cm` | ✅ 已创建 | ✅ 已添加 | ✅ `save_info_cm_detail` | ✅ 完整 |

### 2. 上交所债券接口

| 接口名称 | 集合名称 | 集合状态 | 定时任务 | 保存方法 | 状态 |
|---------|---------|---------|---------|---------|------|
| `bond_cash_summary_sse` | `bond_cash_summary` | ✅ 已创建 | ✅ 已添加 | ✅ `save_cash_summary` | ✅ 完整 |
| `bond_deal_summary_sse` | `bond_deal_summary` | ✅ 已创建 | ✅ 已添加 | ✅ `save_deal_summary` | ✅ 完整 |

### 3. 银行间市场接口

| 接口名称 | 集合名称 | 集合状态 | 定时任务 | 保存方法 | 状态 |
|---------|---------|---------|---------|---------|------|
| `bond_debt_nafmii` | `bond_nafmii_debts` | ✅ 已创建 | ✅ 已添加 | ✅ `save_nafmii` | ✅ 完整 |
| `bond_spot_quote` | `bond_spot_quote_detail` | ✅ 已创建 | ✅ 已添加 | ✅ `save_spot_quote_detail` | ✅ 完整 |
| `bond_spot_deal` | `bond_spot_deals` | ✅ 已创建 | ✅ 已添加 | ✅ `save_spot_deals` | ✅ 完整 |

### 4. 收益率曲线接口

| 接口名称 | 集合名称 | 集合状态 | 定时任务 | 保存方法 | 状态 |
|---------|---------|---------|---------|---------|------|
| `bond_china_yield` | `yield_curve_daily` | ✅ 已创建 | ✅ 已添加 | ✅ `save_yield_curve` | ✅ 完整 |
| `bond_china_close_return` | `yield_curve_daily` | ✅ 已创建 | ⚠️ 未添加 | ⚠️ 未实现 | ⚠️ 缺失 |

### 5. 沪深债券接口

| 接口名称 | 集合名称 | 集合状态 | 定时任务 | 保存方法 | 状态 |
|---------|---------|---------|---------|---------|------|
| `bond_zh_hs_spot` | `bond_spot_quotes` | ✅ 已创建 | ✅ 已添加 | ✅ `save_spot_quotes` | ✅ 完整 |
| `bond_zh_hs_daily` | `bond_daily` | ✅ 已创建 | ✅ 已添加 | ✅ `save_bond_daily` | ✅ 完整 |

### 6. 沪深可转债接口

| 接口名称 | 集合名称 | 集合状态 | 定时任务 | 保存方法 | 状态 |
|---------|---------|---------|---------|---------|------|
| `bond_zh_hs_cov_spot` | `bond_spot_quotes` | ✅ 已创建 | ✅ 已添加 | ✅ `save_spot_quotes` | ✅ 完整 |
| `bond_zh_hs_cov_daily` | `bond_daily` | ✅ 已创建 | ✅ 已添加 | ✅ `save_bond_daily` | ✅ 完整 |
| `bond_zh_hs_cov_min` | ❌ 未创建 | ❌ 未添加 | ❌ 未实现 | ❌ 缺失 |
| `bond_zh_hs_cov_pre_min` | ❌ 未创建 | ❌ 未添加 | ❌ 未实现 | ❌ 缺失 |

### 7. 可转债详情接口

| 接口名称 | 集合名称 | 集合状态 | 定时任务 | 保存方法 | 状态 |
|---------|---------|---------|---------|---------|------|
| `bond_cb_profile_sina` | `bond_cb_profiles` | ✅ 已创建 | ✅ 已添加 | ✅ `save_cb_profiles` | ✅ 完整 |
| `bond_cb_summary_sina` | `bond_cb_summary` | ✅ 已创建 | ⚠️ 未添加 | ⚠️ 未实现 | ⚠️ 缺失 |
| `bond_zh_cov` | `bond_cov_list` | ✅ 已创建 | ✅ 已添加 | ✅ `save_cov_list` | ✅ 完整 |
| `bond_zh_cov_info` | `bond_cb_profiles` | ✅ 已创建 | ⚠️ 未添加 | ⚠️ 未实现 | ⚠️ 缺失 |
| `bond_zh_cov_info_ths` | `bond_cb_profiles` | ✅ 已创建 | ⚠️ 未添加 | ⚠️ 未实现 | ⚠️ 缺失 |
| `bond_cov_comparison` | `bond_cb_comparison` | ✅ 已创建 | ✅ 已添加 | ✅ `save_cb_comparison` | ✅ 完整 |
| `bond_zh_cov_value_analysis` | `bond_cb_valuation_daily` | ✅ 已创建 | ✅ 已添加 | ✅ `save_cb_valuation` | ✅ 完整 |

### 8. 质押式回购接口

| 接口名称 | 集合名称 | 集合状态 | 定时任务 | 保存方法 | 状态 |
|---------|---------|---------|---------|---------|------|
| `bond_sh_buy_back_em` | `bond_buybacks` | ✅ 已创建 | ✅ 已添加 | ✅ `save_buybacks` | ✅ 完整 |
| `bond_sz_buy_back_em` | `bond_buybacks` | ✅ 已创建 | ✅ 已添加 | ✅ `save_buybacks` | ✅ 完整 |
| `bond_buy_back_hist_em` | `bond_buybacks_hist` | ✅ 已创建 | ✅ 已添加 | ✅ `save_buybacks_hist` | ✅ 完整 |

### 9. 集思录接口

| 接口名称 | 集合名称 | 集合状态 | 定时任务 | 保存方法 | 状态 |
|---------|---------|---------|---------|---------|------|
| `bond_cb_jsl` | `bond_cb_list_jsl` | ✅ 已创建 | ✅ 已添加 | ✅ `save_cb_list_jsl` | ✅ 完整 |
| `bond_cb_redeem_jsl` | `bond_cb_redeems` | ✅ 已创建 | ✅ 已添加 | ✅ `save_cb_redeems` | ✅ 完整 |
| `bond_cb_index_jsl` | `bond_indices_daily` | ✅ 已创建 | ⚠️ 未添加 | ⚠️ 未实现 | ⚠️ 缺失 |
| `bond_cb_adj_logs_jsl` | `bond_cb_adjustments` | ✅ 已创建 | ✅ 已添加 | ✅ `save_cb_adjustments` | ✅ 完整 |

### 10. 中美国债收益率接口

| 接口名称 | 集合名称 | 集合状态 | 定时任务 | 保存方法 | 状态 |
|---------|---------|---------|---------|---------|------|
| `bond_zh_us_rate` | `us_yield_daily` | ✅ 已创建 | ✅ 已添加 | ✅ `save_us_yield` | ✅ 完整 |

### 11. 债券发行接口

| 接口名称 | 集合名称 | 集合状态 | 定时任务 | 保存方法 | 状态 |
|---------|---------|---------|---------|---------|------|
| `bond_treasure_issue_cninfo` | `bond_issues` | ✅ 已创建 | ✅ 已添加 | ✅ `save_issues` | ✅ 完整 |
| `bond_local_government_issue_cninfo` | `bond_issues` | ✅ 已创建 | ✅ 已添加 | ✅ `save_issues` | ✅ 完整 |
| `bond_corporate_issue_cninfo` | `bond_issues` | ✅ 已创建 | ✅ 已添加 | ✅ `save_issues` | ✅ 完整 |
| `bond_cov_issue_cninfo` | `bond_issues` | ✅ 已创建 | ✅ 已添加 | ✅ `save_issues` | ✅ 完整 |
| `bond_cov_stock_issue_cninfo` | `bond_issues` | ✅ 已创建 | ✅ 已添加 | ✅ `save_issues` | ✅ 完整 |

### 12. 中债指数接口

| 接口名称 | 集合名称 | 集合状态 | 定时任务 | 保存方法 | 状态 |
|---------|---------|---------|---------|---------|------|
| `bond_new_composite_index_cbond` | `bond_indices_daily` | ✅ 已创建 | ✅ 已添加 | ✅ `save_indices` | ✅ 完整 |
| `bond_composite_index_cbond` | `bond_indices_daily` | ✅ 已创建 | ✅ 已添加 | ✅ `save_indices` | ✅ 完整 |

## 统计汇总

### 总体情况

- **总接口数**: 37
- **已完整实现**: 29 (78.4%)
- **部分实现**: 6 (16.2%)
- **未实现**: 2 (5.4%)

### 详细分类

#### ✅ 已完整实现 (29个)

1. `bond_info_cm`
2. `bond_info_detail_cm`
3. `bond_cash_summary_sse`
4. `bond_deal_summary_sse`
5. `bond_debt_nafmii`
6. `bond_spot_quote`
7. `bond_spot_deal`
8. `bond_china_yield`
9. `bond_zh_hs_spot`
10. `bond_zh_hs_daily`
11. `bond_zh_hs_cov_spot`
12. `bond_zh_hs_cov_daily`
13. `bond_cb_profile_sina`
14. `bond_zh_cov`
15. `bond_cov_comparison`
16. `bond_zh_cov_value_analysis`
17. `bond_sh_buy_back_em`
18. `bond_sz_buy_back_em`
19. `bond_buy_back_hist_em`
20. `bond_cb_jsl`
21. `bond_cb_redeem_jsl`
22. `bond_cb_adj_logs_jsl`
23. `bond_zh_us_rate`
24. `bond_treasure_issue_cninfo`
25. `bond_local_government_issue_cninfo`
26. `bond_corporate_issue_cninfo`
29. `bond_cov_issue_cninfo`
28. `bond_cov_stock_issue_cninfo`
29. `bond_new_composite_index_cbond`
30. `bond_composite_index_cbond`

#### ⚠️ 部分实现 (6个)

1. **`bond_china_close_return`**
   - 集合: `yield_curve_daily` ✅
   - 定时任务: ❌
   - 保存方法: ⚠️ (可复用 `save_yield_curve`)

2. **`bond_cb_summary_sina`**
   - 集合: `bond_cb_summary` ✅
   - 定时任务: ❌
   - 保存方法: ⚠️ (需要新增)

3. **`bond_zh_cov_info`**
   - 集合: `bond_cb_profiles` ✅
   - 定时任务: ❌
   - 保存方法: ⚠️ (可复用 `save_cb_profiles`)

4. **`bond_zh_cov_info_ths`**
   - 集合: `bond_cb_profiles` ✅
   - 定时任务: ❌
   - 保存方法: ⚠️ (可复用 `save_cb_profiles`)

5. **`bond_cb_index_jsl`**
   - 集合: `bond_indices_daily` ✅
   - 定时任务: ❌
   - 保存方法: ⚠️ (可复用 `save_indices`)

#### ❌ 未实现 (2个)

1. **`bond_zh_hs_cov_min`** (可转债分时行情)
   - 集合: ❌
   - 定时任务: ❌
   - 保存方法: ❌
   - 说明: 分时数据，可能需要单独的集合

2. **`bond_zh_hs_cov_pre_min`** (可转债盘前分时)
   - 集合: ❌
   - 定时任务: ❌
   - 保存方法: ❌
   - 说明: 盘前分时数据，可能需要单独的集合

## 建议改进

### 优先级 1: 补充缺失的定时任务

以下接口已创建集合和保存方法，但未添加到定时任务：

1. **`bond_china_close_return`**
   - 添加到收益率曲线同步任务，或创建独立任务
   - 复用 `save_yield_curve` 方法

2. **`bond_cb_summary_sina`**
   - 添加到可转债档案同步任务
   - 需要新增保存方法 `save_cb_summary`

3. **`bond_zh_cov_info`** 和 **`bond_zh_cov_info_ths`**
   - 添加到可转债档案同步任务
   - 复用或扩展 `save_cb_profiles` 方法

4. **`bond_cb_index_jsl`**
   - 添加到债券指数同步任务
   - 复用 `save_indices` 方法

### 优先级 2: 实现分时数据接口

如果需要分时数据，建议：

1. **创建集合**
   - `bond_minute_quotes` (分钟级行情)
   - 唯一键: `(code, datetime, period)`

2. **实现保存方法**
   - `save_bond_minute_quotes(df, code, period)`

3. **添加到定时任务**
   - 可转债分时行情同步（交易时段高频）
   - 盘前分时行情同步（开盘前）

### 优先级 3: 优化现有实现

1. **统一字段映射**
   - 确保所有接口的字段映射符合数据表设计文档

2. **错误处理**
   - 完善异常处理和数据验证

3. **性能优化**
   - 批量操作优化
   - 索引优化

## 结论

目前代码已经实现了 **78.4%** 的 AKShare 债券接口，覆盖了主要的业务场景：

✅ **已覆盖**:
- 债券基础信息和列表
- 历史行情数据（日线）
- 实时行情数据（现货报价）
- 收益率曲线
- 可转债详情和估值
- 债券发行信息
- 回购信息
- 指数数据

⚠️ **部分覆盖**:
- 部分详情接口（需要添加定时任务）
- 收盘收益率曲线（需要添加定时任务）

❌ **未覆盖**:
- 分时行情数据（分钟级）
- 盘前分时数据

整体实现情况良好，建议优先补充缺失的定时任务，然后根据业务需求决定是否实现分时数据接口。

