# 债券接口与数据集合映射表

## 文档中的所有接口（37个）

### 1. 中债信息接口 (2个)
- ✅ `bond_info_cm` → `bond_info_cm` 集合
- ✅ `bond_info_detail_cm` → `bond_info_cm` 集合（通过endpoint区分）

### 2. 上交所债券接口 (2个)
- ✅ `bond_cash_summary_sse` → `bond_cash_summary` 集合
- ✅ `bond_deal_summary_sse` → `bond_deal_summary` 集合

### 3. 银行间市场接口 (3个)
- ✅ `bond_debt_nafmii` → `bond_nafmii_debts` 集合
- ✅ `bond_spot_quote` → `bond_spot_quote_detail` 集合
- ✅ `bond_spot_deal` → `bond_spot_deals` 集合

### 4. 收益率曲线接口 (2个)
- ✅ `bond_china_yield` → `yield_curve_daily` 集合
- ✅ `bond_china_close_return` → `yield_curve_daily` 集合（通过yield_type区分）

### 5. 沪深债券接口 (2个)
- ✅ `bond_zh_hs_spot` → `bond_spot_quotes` 集合（category=hs_spot）
- ✅ `bond_zh_hs_daily` → `bond_daily` 集合

### 6. 沪深可转债接口 (4个)
- ✅ `bond_zh_hs_cov_spot` → `bond_spot_quotes` 集合（category=cov_spot）
- ✅ `bond_zh_hs_cov_daily` → `bond_daily` 集合
- ✅ `bond_zh_hs_cov_min` → `bond_minute_quotes` 集合
- ✅ `bond_zh_hs_cov_pre_min` → `bond_minute_quotes` 集合

### 7. 可转债详情接口 (6个)
- ✅ `bond_cb_profile_sina` → `bond_cb_profiles` 集合
- ✅ `bond_cb_summary_sina` → `bond_cb_summary` 集合
- ✅ `bond_zh_cov` → `bond_cov_list` 集合
- ✅ `bond_zh_cov_info` → `bond_cb_profiles` 集合
- ✅ `bond_zh_cov_info_ths` → `bond_cb_profiles` 集合
- ✅ `bond_cov_comparison` → `bond_cb_comparison` 集合
- ✅ `bond_zh_cov_value_analysis` → `bond_cb_valuation_daily` 集合

### 8. 质押式回购接口 (3个)
- ✅ `bond_sh_buy_back_em` → `bond_buybacks` 集合（exchange=SH）
- ✅ `bond_sz_buy_back_em` → `bond_buybacks` 集合（exchange=SZ）
- ✅ `bond_buy_back_hist_em` → `bond_buybacks_hist` 集合

### 9. 集思录接口 (4个)
- ✅ `bond_cb_jsl` → `bond_cb_list_jsl` 集合
- ✅ `bond_cb_redeem_jsl` → `bond_cb_redeems` 集合
- ✅ `bond_cb_index_jsl` → `bond_indices_daily` 集合
- ✅ `bond_cb_adj_logs_jsl` → `bond_cb_adjustments` 集合

### 10. 中美国债收益率接口 (1个)
- ✅ `bond_zh_us_rate` → `us_yield_daily` 集合

### 11. 债券发行接口 (5个)
- ✅ `bond_treasure_issue_cninfo` → `bond_issues` 集合（issue_type=treasure）
- ✅ `bond_local_government_issue_cninfo` → `bond_issues` 集合（issue_type=local_government）
- ✅ `bond_corporate_issue_cninfo` → `bond_issues` 集合（issue_type=corporate）
- ✅ `bond_cov_issue_cninfo` → `bond_issues` 集合（issue_type=cov）
- ✅ `bond_cov_stock_issue_cninfo` → `bond_issues` 集合（issue_type=cov_stock）

### 12. 中债指数接口 (2个)
- ✅ `bond_new_composite_index_cbond` → `bond_indices_daily` 集合
- ✅ `bond_composite_index_cbond` → `bond_indices_daily` 集合

## 数据集合列表（26个）

所有37个接口映射到26个数据集合：

1. ✅ `bond_basic_info` - 债券基础信息
2. ✅ `bond_daily` - 债券历史行情
3. ✅ `yield_curve_daily` - 收益率曲线
4. ✅ `bond_spot_quotes` - 债券现货报价
5. ✅ `bond_minute_quotes` - 债券分钟数据
6. ✅ `bond_cb_profiles` - 可转债档案
7. ✅ `bond_cb_valuation_daily` - 可转债估值
8. ✅ `bond_cb_comparison` - 可转债比价表
9. ✅ `bond_cb_adjustments` - 可转债转股价格调整
10. ✅ `bond_cb_redeems` - 可转债强赎
11. ✅ `bond_issues` - 债券发行
12. ✅ `bond_buybacks` - 债券回购
13. ✅ `bond_buybacks_hist` - 债券回购历史
14. ✅ `bond_indices_daily` - 债券指数
15. ✅ `us_yield_daily` - 美国国债收益率
16. ✅ `bond_spot_quote_detail` - 现货报价明细
17. ✅ `bond_spot_deals` - 现货成交明细
18. ✅ `bond_deal_summary` - 成交概览
19. ✅ `bond_cash_summary` - 现券市场概览
20. ✅ `bond_nafmii_debts` - 银行间市场债务
21. ✅ `bond_info_cm` - 中债信息
22. ✅ `bond_cov_list` - 可转债列表
23. ✅ `bond_cb_list_jsl` - 集思录可转债
24. ✅ `bond_cb_summary` - 可转债债券概况
25. ✅ `bond_events` - 债券事件
26. ✅ `yield_curve_map` - 收益率曲线映射

## 前端访问状态

所有26个集合都已添加到：
- ✅ `/api/bonds/collections` API端点
- ✅ 前端债券概览页面的数据集合链接
- ✅ 前端集合数据展示页面路由

## 总结

✅ **所有37个AKShare债券接口都已实现对应的数据集合**
✅ **所有26个数据集合都可以从债券概览页面访问**
✅ **所有集合都有完整的前端展示页面**

