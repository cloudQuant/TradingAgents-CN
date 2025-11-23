# 基金数据需求文档（26-71号）生成说明

## 概述

基于 akshare 接口文档 `_sources_data_fund_fund_public.md.txt.html`，为其中的每个接口生成对应的需求文档。

## 已完成的文档

### 手动创建的示例文档（5个）

1. ✅ **26_基金累计分红-新浪.md** - fund_etf_dividend_sina
2. ✅ **27_基金分红-东财.md** - fund_fh_em
3. ✅ **28_基金拆分-东财.md** - fund_cf_em
4. ✅ **29_基金分红排行-东财.md** - fund_fh_rank_em
5. ✅ **30_开放式基金排行-东财.md** - fund_open_fund_rank_em
6. ✅ **35_基金业绩-雪球.md** - fund_individual_achievement_xq
7. ✅ **51_基金经理-东财.md** - fund_manager_em
8. ✅ **59_REITs实时行情-东财.md** - reits_realtime_em

### 辅助文档

- ✅ **需求文档清单_26-65.md** - 完整的文档清单和说明
- ✅ **generate_remaining_docs.py** - 批量生成脚本（部分实现）

## 文档结构

每个需求文档包含以下部分：

### 1. 背景
说明补充基金数据的必要性

### 2. 任务
参考 bond_info_cm 的实现方式，获取并更新基金数据

### 3. 步骤
- 创建数据集合
- 实现前端界面（数据概览、列表、刷新、清空、更新、图表）
- 实现数据更新功能（文件导入、远程同步、单个/批量更新）

### 4. 测试驱动
- 编写测试用例（selenium/playwright）
- 开发功能
- 运行测试并修复

### 5. 验收标准
- 测试用例全部通过
- 手动操作无异常

### 6. API接口信息
- 接口名称
- 目标地址
- 描述
- 限量说明
- 输入/输出参数
- 接口示例
- 数据示例

## 接口分类统计

根据 akshare 文档，共有约 **46个接口**，分为以下类别：

### 分红送配类（4个）
- fund_etf_dividend_sina - 基金累计分红
- fund_fh_em - 基金分红
- fund_cf_em - 基金拆分
- fund_fh_rank_em - 基金分红排行

### 基金排行类（5个）
- fund_open_fund_rank_em - 开放式基金排行
- fund_exchange_rank_em - 场内交易基金排行
- fund_money_rank_em - 货币型基金排行
- fund_lcx_rank_em - 理财基金排行
- fund_hk_rank_em - 香港基金排行

### 基金分析类（5个）
- fund_individual_achievement_xq - 基金业绩（雪球）
- fund_value_estimation_em - 净值估算
- fund_individual_analysis_xq - 基金数据分析（雪球）
- fund_individual_profit_probability_xq - 基金盈利概率（雪球）
- fund_individual_detail_hold_xq - 基金持仓资产比例（雪球）

### 基金档案类（5个）
- fund_overview_em - 基金基本概况
- fund_fee_em - 基金交易费率
- fund_individual_detail_info_xq - 基金交易规则（雪球）
- fund_portfolio_hold_em - 基金持仓
- fund_portfolio_bond_hold_em - 债券持仓

### 投资组合类（2个）
- fund_portfolio_industry_allocation_em - 行业配置
- fund_portfolio_change_em - 重大变动

### 基金评级类（4个）
- fund_rating_all - 基金评级总汇
- fund_rating_sh - 上海证券评级
- fund_rating_zs - 招商证券评级
- fund_rating_ja - 济安金信评级

### 基金公司类（2个）
- fund_manager_em - 基金经理
- fund_new_found_em - 新发基金

### 基金规模类（6个）
- fund_scale_open_sina - 开放式基金规模
- fund_scale_close_sina - 封闭式基金规模
- fund_scale_structured_sina - 分级子基金规模
- fund_aum_em - 基金规模详情
- fund_aum_trend_em - 基金规模走势
- fund_aum_hist_em - 基金公司历年管理规模

### REITs类（2个）
- reits_realtime_em - REITs实时行情
- reits_hist_em - REITs历史行情

### 基金报告类（3个）
- fund_report_stock_cninfo - 基金重仓股
- fund_report_industry_allocation_cninfo - 基金行业配置
- fund_report_asset_allocation_cninfo - 基金资产配置

### 规模份额类（2个）
- fund_scale_change_em - 规模变动
- fund_hold_structure_em - 持有人结构

### 基金仓位类（3个）
- fund_stock_position_lg - 股票型基金仓位
- fund_balance_position_lg - 平衡混合型基金仓位
- fund_linghuo_position_lg - 灵活配置型基金仓位

### 基金公告类（3个）
- fund_announcement_dividend_em - 分红配送公告
- fund_announcement_report_em - 定期报告公告
- fund_announcement_personnel_em - 人事调整公告

## 实现建议

### 优先级划分

**高优先级（核心功能）**：
- 基金排行类（5个）
- 基金分析类（5个）
- 基金档案类（5个）

**中优先级（重要补充）**：
- 分红送配类（4个）
- 基金评级类（4个）
- 基金规模类（6个）
- REITs类（2个）

**低优先级（辅助信息）**：
- 投资组合类（2个）
- 基金公司类（2个）
- 基金报告类（3个）
- 规模份额类（2个）
- 基金仓位类（3个）
- 基金公告类（3个）

### 技术要点

1. **数据唯一性**：根据不同接口特点确定唯一键
   - 实时数据：代码 + 日期/时间
   - 历史数据：代码 + 日期 + 其他维度（如周期、复权方式）
   - 排行数据：代码 + 日期
   - 分析数据：代码 + 分析维度

2. **更新策略**：
   - 全量更新：排行、评级、规模等数据
   - 增量更新：历史行情、持仓等数据
   - 单个更新：支持按基金代码更新
   - 批量更新：支持批量基金代码更新

3. **数据来源**：
   - 东方财富网（东财）：主要数据源
   - 新浪财经：部分历史数据
   - 雪球/蛋卷：基金分析数据
   - 巨潮资讯：基金报告数据
   - 乐咕乐股：基金仓位数据

## 后续工作

1. 使用 `generate_remaining_docs.py` 脚本批量生成剩余文档
2. 根据实际需求调整文档内容
3. 按优先级逐步实现各个接口
4. 编写测试用例
5. 前后端联调
6. 上线验证

## 参考资料

- 已实现的基金数据集合：tests/funds/10-25
- 债券数据参考：bond_info_cm
- AKShare文档：https://akshare.akfamily.xyz/data/fund/fund.html
