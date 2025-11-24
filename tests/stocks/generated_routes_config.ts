/**
 * 生成的前端路由配置
 * 需要手动添加到 frontend/src/router/index.ts 文件中
 */

// 将以下路由配置添加到路由数组中
const generatedRoutes = [
{
  path: '/stocks/collections/news_report_time_baidu',
  name: 'NewsReportTimeBaidu',
  component: () => import('@/views/Stocks/Collections/NewsReportTimeBaidu.vue'),
  meta: { title: '财报发行', requiresAuth: true }
},
{
  path: '/stocks/collections/news_trade_notify_dividend_baidu',
  name: 'NewsTradeNotifyDividendBaidu',
  component: () => import('@/views/Stocks/Collections/NewsTradeNotifyDividendBaidu.vue'),
  meta: { title: '分红派息', requiresAuth: true }
},
{
  path: '/stocks/collections/news_trade_notify_suspend_baidu',
  name: 'NewsTradeNotifySuspendBaidu',
  component: () => import('@/views/Stocks/Collections/NewsTradeNotifySuspendBaidu.vue'),
  meta: { title: '停复牌', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_a_all_pb',
  name: 'StockAAllPb',
  component: () => import('@/views/Stocks/Collections/StockAAllPb.vue'),
  meta: { title: 'A 股等权重与中位数市净率', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_a_below_net_asset_statistics',
  name: 'StockABelowNetAssetStatistics',
  component: () => import('@/views/Stocks/Collections/StockABelowNetAssetStatistics.vue'),
  meta: { title: '破净股统计', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_a_congestion_lg',
  name: 'StockACongestionLg',
  component: () => import('@/views/Stocks/Collections/StockACongestionLg.vue'),
  meta: { title: '大盘拥挤度', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_a_gxl_lg',
  name: 'StockAGxlLg',
  component: () => import('@/views/Stocks/Collections/StockAGxlLg.vue'),
  meta: { title: 'A 股股息率', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_a_high_low_statistics',
  name: 'StockAHighLowStatistics',
  component: () => import('@/views/Stocks/Collections/StockAHighLowStatistics.vue'),
  meta: { title: '创新高和新低的股票数量', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_a_ttm_lyr',
  name: 'StockATtmLyr',
  component: () => import('@/views/Stocks/Collections/StockATtmLyr.vue'),
  meta: { title: 'A 股等权重与中位数市盈率', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_account_statistics_em',
  name: 'StockAccountStatisticsEm',
  component: () => import('@/views/Stocks/Collections/StockAccountStatisticsEm.vue'),
  meta: { title: '股票账户统计月度', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_add_stock',
  name: 'StockAddStock',
  component: () => import('@/views/Stocks/Collections/StockAddStock.vue'),
  meta: { title: '股票增发', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_allotment_cninfo',
  name: 'StockAllotmentCninfo',
  component: () => import('@/views/Stocks/Collections/StockAllotmentCninfo.vue'),
  meta: { title: '配股实施方案-巨潮资讯', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_analyst_detail_em',
  name: 'StockAnalystDetailEm',
  component: () => import('@/views/Stocks/Collections/StockAnalystDetailEm.vue'),
  meta: { title: '分析师详情', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_analyst_rank_em',
  name: 'StockAnalystRankEm',
  component: () => import('@/views/Stocks/Collections/StockAnalystRankEm.vue'),
  meta: { title: '分析师指数排行', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_balance_sheet_by_yearly_em',
  name: 'StockBalanceSheetByYearlyEm',
  component: () => import('@/views/Stocks/Collections/StockBalanceSheetByYearlyEm.vue'),
  meta: { title: '资产负债表-按年度', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_bid_ask_em',
  name: 'StockBidAskEm',
  component: () => import('@/views/Stocks/Collections/StockBidAskEm.vue'),
  meta: { title: '行情报价', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_bj_a_spot_em',
  name: 'StockBjASpotEm',
  component: () => import('@/views/Stocks/Collections/StockBjASpotEm.vue'),
  meta: { title: '京 A 股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_board_change_em',
  name: 'StockBoardChangeEm',
  component: () => import('@/views/Stocks/Collections/StockBoardChangeEm.vue'),
  meta: { title: '板块异动详情', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_board_concept_cons_em',
  name: 'StockBoardConceptConsEm',
  component: () => import('@/views/Stocks/Collections/StockBoardConceptConsEm.vue'),
  meta: { title: '东方财富-成份股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_board_concept_hist_em',
  name: 'StockBoardConceptHistEm',
  component: () => import('@/views/Stocks/Collections/StockBoardConceptHistEm.vue'),
  meta: { title: '东方财富-指数', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_board_concept_hist_min_em',
  name: 'StockBoardConceptHistMinEm',
  component: () => import('@/views/Stocks/Collections/StockBoardConceptHistMinEm.vue'),
  meta: { title: '东方财富-指数-分时', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_board_concept_index_ths',
  name: 'StockBoardConceptIndexThs',
  component: () => import('@/views/Stocks/Collections/StockBoardConceptIndexThs.vue'),
  meta: { title: '同花顺-概念板块指数', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_board_concept_info_ths',
  name: 'StockBoardConceptInfoThs',
  component: () => import('@/views/Stocks/Collections/StockBoardConceptInfoThs.vue'),
  meta: { title: '同花顺-概念板块简介', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_board_concept_name_em',
  name: 'StockBoardConceptNameEm',
  component: () => import('@/views/Stocks/Collections/StockBoardConceptNameEm.vue'),
  meta: { title: '东方财富-概念板块', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_board_concept_spot_em',
  name: 'StockBoardConceptSpotEm',
  component: () => import('@/views/Stocks/Collections/StockBoardConceptSpotEm.vue'),
  meta: { title: '东方财富-概念板块-实时行情', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_board_industry_cons_em',
  name: 'StockBoardIndustryConsEm',
  component: () => import('@/views/Stocks/Collections/StockBoardIndustryConsEm.vue'),
  meta: { title: '东方财富-成份股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_board_industry_hist_em',
  name: 'StockBoardIndustryHistEm',
  component: () => import('@/views/Stocks/Collections/StockBoardIndustryHistEm.vue'),
  meta: { title: '东方财富-指数-日频', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_board_industry_hist_min_em',
  name: 'StockBoardIndustryHistMinEm',
  component: () => import('@/views/Stocks/Collections/StockBoardIndustryHistMinEm.vue'),
  meta: { title: '东方财富-指数-分时', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_board_industry_index_ths',
  name: 'StockBoardIndustryIndexThs',
  component: () => import('@/views/Stocks/Collections/StockBoardIndustryIndexThs.vue'),
  meta: { title: '同花顺-指数', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_board_industry_spot_em',
  name: 'StockBoardIndustrySpotEm',
  component: () => import('@/views/Stocks/Collections/StockBoardIndustrySpotEm.vue'),
  meta: { title: '东方财富-行业板块-实时行情', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_board_industry_summary_ths',
  name: 'StockBoardIndustrySummaryThs',
  component: () => import('@/views/Stocks/Collections/StockBoardIndustrySummaryThs.vue'),
  meta: { title: '同花顺-同花顺行业一览表', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_buffett_index_lg',
  name: 'StockBuffettIndexLg',
  component: () => import('@/views/Stocks/Collections/StockBuffettIndexLg.vue'),
  meta: { title: '巴菲特指标', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_cg_equity_mortgage_cninfo',
  name: 'StockCgEquityMortgageCninfo',
  component: () => import('@/views/Stocks/Collections/StockCgEquityMortgageCninfo.vue'),
  meta: { title: '股权质押', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_cg_guarantee_cninfo',
  name: 'StockCgGuaranteeCninfo',
  component: () => import('@/views/Stocks/Collections/StockCgGuaranteeCninfo.vue'),
  meta: { title: '对外担保', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_cg_lawsuit_cninfo',
  name: 'StockCgLawsuitCninfo',
  component: () => import('@/views/Stocks/Collections/StockCgLawsuitCninfo.vue'),
  meta: { title: '公司诉讼', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_changes_em',
  name: 'StockChangesEm',
  component: () => import('@/views/Stocks/Collections/StockChangesEm.vue'),
  meta: { title: '盘口异动', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_circulate_stock_holder',
  name: 'StockCirculateStockHolder',
  component: () => import('@/views/Stocks/Collections/StockCirculateStockHolder.vue'),
  meta: { title: '流通股东', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_comment_detail_scrd_desire_daily_em',
  name: 'StockCommentDetailScrdDesireDailyEm',
  component: () => import('@/views/Stocks/Collections/StockCommentDetailScrdDesireDailyEm.vue'),
  meta: { title: '日度市场参与意愿', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_comment_detail_scrd_desire_em',
  name: 'StockCommentDetailScrdDesireEm',
  component: () => import('@/views/Stocks/Collections/StockCommentDetailScrdDesireEm.vue'),
  meta: { title: '市场参与意愿', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_comment_detail_scrd_focus_em',
  name: 'StockCommentDetailScrdFocusEm',
  component: () => import('@/views/Stocks/Collections/StockCommentDetailScrdFocusEm.vue'),
  meta: { title: '用户关注指数', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_comment_detail_zhpj_lspf_em',
  name: 'StockCommentDetailZhpjLspfEm',
  component: () => import('@/views/Stocks/Collections/StockCommentDetailZhpjLspfEm.vue'),
  meta: { title: '历史评分', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_comment_detail_zlkp_jgcyd_em',
  name: 'StockCommentDetailZlkpJgcydEm',
  component: () => import('@/views/Stocks/Collections/StockCommentDetailZlkpJgcydEm.vue'),
  meta: { title: '机构参与度', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_comment_em',
  name: 'StockCommentEm',
  component: () => import('@/views/Stocks/Collections/StockCommentEm.vue'),
  meta: { title: '千股千评', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_concept_cons_futu',
  name: 'StockConceptConsFutu',
  component: () => import('@/views/Stocks/Collections/StockConceptConsFutu.vue'),
  meta: { title: '富途牛牛-美股概念-成分股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_cy_a_spot_em',
  name: 'StockCyASpotEm',
  component: () => import('@/views/Stocks/Collections/StockCyASpotEm.vue'),
  meta: { title: '创业板', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_dividend_cninfo',
  name: 'StockDividendCninfo',
  component: () => import('@/views/Stocks/Collections/StockDividendCninfo.vue'),
  meta: { title: '历史分红', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_dxsyl_em',
  name: 'StockDxsylEm',
  component: () => import('@/views/Stocks/Collections/StockDxsylEm.vue'),
  meta: { title: '打新收益率', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_dzjy_hygtj',
  name: 'StockDzjyHygtj',
  component: () => import('@/views/Stocks/Collections/StockDzjyHygtj.vue'),
  meta: { title: '活跃 A 股统计', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_dzjy_hyyybtj',
  name: 'StockDzjyHyyybtj',
  component: () => import('@/views/Stocks/Collections/StockDzjyHyyybtj.vue'),
  meta: { title: '活跃营业部统计', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_dzjy_yybph',
  name: 'StockDzjyYybph',
  component: () => import('@/views/Stocks/Collections/StockDzjyYybph.vue'),
  meta: { title: '营业部排行', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_ebs_lg',
  name: 'StockEbsLg',
  component: () => import('@/views/Stocks/Collections/StockEbsLg.vue'),
  meta: { title: '股债利差', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_esg_hz_sina',
  name: 'StockEsgHzSina',
  component: () => import('@/views/Stocks/Collections/StockEsgHzSina.vue'),
  meta: { title: '华证指数', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_esg_msci_sina',
  name: 'StockEsgMsciSina',
  component: () => import('@/views/Stocks/Collections/StockEsgMsciSina.vue'),
  meta: { title: 'MSCI', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_esg_rate_sina',
  name: 'StockEsgRateSina',
  component: () => import('@/views/Stocks/Collections/StockEsgRateSina.vue'),
  meta: { title: 'ESG 评级数据', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_esg_rft_sina',
  name: 'StockEsgRftSina',
  component: () => import('@/views/Stocks/Collections/StockEsgRftSina.vue'),
  meta: { title: '路孚特', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_esg_zd_sina',
  name: 'StockEsgZdSina',
  component: () => import('@/views/Stocks/Collections/StockEsgZdSina.vue'),
  meta: { title: '秩鼎', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_fhps_detail_em',
  name: 'StockFhpsDetailEm',
  component: () => import('@/views/Stocks/Collections/StockFhpsDetailEm.vue'),
  meta: { title: '分红配送详情-东财', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_fhps_em',
  name: 'StockFhpsEm',
  component: () => import('@/views/Stocks/Collections/StockFhpsEm.vue'),
  meta: { title: '分红配送-东财', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_fund_stock_holder',
  name: 'StockFundStockHolder',
  component: () => import('@/views/Stocks/Collections/StockFundStockHolder.vue'),
  meta: { title: '基金持股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_gdfx_free_holding_detail_em',
  name: 'StockGdfxFreeHoldingDetailEm',
  component: () => import('@/views/Stocks/Collections/StockGdfxFreeHoldingDetailEm.vue'),
  meta: { title: '股东持股明细-十大流通股东', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_gdfx_free_holding_statistics_em',
  name: 'StockGdfxFreeHoldingStatisticsEm',
  component: () => import('@/views/Stocks/Collections/StockGdfxFreeHoldingStatisticsEm.vue'),
  meta: { title: '股东持股统计-十大流通股东', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_gdfx_free_holding_teamwork_em',
  name: 'StockGdfxFreeHoldingTeamworkEm',
  component: () => import('@/views/Stocks/Collections/StockGdfxFreeHoldingTeamworkEm.vue'),
  meta: { title: '股东协同-十大流通股东', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_gdfx_holding_detail_em',
  name: 'StockGdfxHoldingDetailEm',
  component: () => import('@/views/Stocks/Collections/StockGdfxHoldingDetailEm.vue'),
  meta: { title: '股东持股明细-十大股东', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_gdfx_holding_statistics_em',
  name: 'StockGdfxHoldingStatisticsEm',
  component: () => import('@/views/Stocks/Collections/StockGdfxHoldingStatisticsEm.vue'),
  meta: { title: '股东持股统计-十大股东', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_gdfx_holding_teamwork_em',
  name: 'StockGdfxHoldingTeamworkEm',
  component: () => import('@/views/Stocks/Collections/StockGdfxHoldingTeamworkEm.vue'),
  meta: { title: '股东协同-十大股东', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_ggcg_em',
  name: 'StockGgcgEm',
  component: () => import('@/views/Stocks/Collections/StockGgcgEm.vue'),
  meta: { title: '股东增减持', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_gpzy_distribute_statistics_bank_em',
  name: 'StockGpzyDistributeStatisticsBankEm',
  component: () => import('@/views/Stocks/Collections/StockGpzyDistributeStatisticsBankEm.vue'),
  meta: { title: '质押机构分布统计-银行', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_gpzy_distribute_statistics_company_em',
  name: 'StockGpzyDistributeStatisticsCompanyEm',
  component: () => import('@/views/Stocks/Collections/StockGpzyDistributeStatisticsCompanyEm.vue'),
  meta: { title: '质押机构分布统计-证券公司', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_gpzy_industry_data_em',
  name: 'StockGpzyIndustryDataEm',
  component: () => import('@/views/Stocks/Collections/StockGpzyIndustryDataEm.vue'),
  meta: { title: '上市公司质押比例', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_gpzy_pledge_ratio_detail_em',
  name: 'StockGpzyPledgeRatioDetailEm',
  component: () => import('@/views/Stocks/Collections/StockGpzyPledgeRatioDetailEm.vue'),
  meta: { title: '重要股东股权质押明细', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_gpzy_pledge_ratio_em',
  name: 'StockGpzyPledgeRatioEm',
  component: () => import('@/views/Stocks/Collections/StockGpzyPledgeRatioEm.vue'),
  meta: { title: '上市公司质押比例', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_gsrl_gsdt_em',
  name: 'StockGsrlGsdtEm',
  component: () => import('@/views/Stocks/Collections/StockGsrlGsdtEm.vue'),
  meta: { title: '公司动态', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_history_dividend_detail',
  name: 'StockHistoryDividendDetail',
  component: () => import('@/views/Stocks/Collections/StockHistoryDividendDetail.vue'),
  meta: { title: '分红配股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hk_company_profile_em',
  name: 'StockHkCompanyProfileEm',
  component: () => import('@/views/Stocks/Collections/StockHkCompanyProfileEm.vue'),
  meta: { title: '公司资料', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hk_daily',
  name: 'StockHkDaily',
  component: () => import('@/views/Stocks/Collections/StockHkDaily.vue'),
  meta: { title: '历史行情数据-新浪', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hk_dividend_payout_em',
  name: 'StockHkDividendPayoutEm',
  component: () => import('@/views/Stocks/Collections/StockHkDividendPayoutEm.vue'),
  meta: { title: '分红派息', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hk_famous_spot_em',
  name: 'StockHkFamousSpotEm',
  component: () => import('@/views/Stocks/Collections/StockHkFamousSpotEm.vue'),
  meta: { title: '知名港股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hk_financial_indicator_em',
  name: 'StockHkFinancialIndicatorEm',
  component: () => import('@/views/Stocks/Collections/StockHkFinancialIndicatorEm.vue'),
  meta: { title: '财务指标', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hk_growth_comparison_em',
  name: 'StockHkGrowthComparisonEm',
  component: () => import('@/views/Stocks/Collections/StockHkGrowthComparisonEm.vue'),
  meta: { title: '成长性对比', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hk_gxl_lg',
  name: 'StockHkGxlLg',
  component: () => import('@/views/Stocks/Collections/StockHkGxlLg.vue'),
  meta: { title: '恒生指数股息率', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hk_hist',
  name: 'StockHkHist',
  component: () => import('@/views/Stocks/Collections/StockHkHist.vue'),
  meta: { title: '历史行情数据-东财', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hk_hist_min_em',
  name: 'StockHkHistMinEm',
  component: () => import('@/views/Stocks/Collections/StockHkHistMinEm.vue'),
  meta: { title: '分时数据-东财', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hk_hot_rank_detail_em',
  name: 'StockHkHotRankDetailEm',
  component: () => import('@/views/Stocks/Collections/StockHkHotRankDetailEm.vue'),
  meta: { title: '港股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hk_hot_rank_detail_realtime_em',
  name: 'StockHkHotRankDetailRealtimeEm',
  component: () => import('@/views/Stocks/Collections/StockHkHotRankDetailRealtimeEm.vue'),
  meta: { title: '港股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hk_hot_rank_em',
  name: 'StockHkHotRankEm',
  component: () => import('@/views/Stocks/Collections/StockHkHotRankEm.vue'),
  meta: { title: '人气榜-港股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hk_hot_rank_latest_em',
  name: 'StockHkHotRankLatestEm',
  component: () => import('@/views/Stocks/Collections/StockHkHotRankLatestEm.vue'),
  meta: { title: '港股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hk_indicator_eniu',
  name: 'StockHkIndicatorEniu',
  component: () => import('@/views/Stocks/Collections/StockHkIndicatorEniu.vue'),
  meta: { title: '港股个股指标', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hk_main_board_spot_em',
  name: 'StockHkMainBoardSpotEm',
  component: () => import('@/views/Stocks/Collections/StockHkMainBoardSpotEm.vue'),
  meta: { title: '港股主板实时行情数据-东财', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hk_profit_forecast_et',
  name: 'StockHkProfitForecastEt',
  component: () => import('@/views/Stocks/Collections/StockHkProfitForecastEt.vue'),
  meta: { title: '港股盈利预测-经济通', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hk_scale_comparison_em',
  name: 'StockHkScaleComparisonEm',
  component: () => import('@/views/Stocks/Collections/StockHkScaleComparisonEm.vue'),
  meta: { title: '规模对比', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hk_security_profile_em',
  name: 'StockHkSecurityProfileEm',
  component: () => import('@/views/Stocks/Collections/StockHkSecurityProfileEm.vue'),
  meta: { title: '证券资料', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hk_spot',
  name: 'StockHkSpot',
  component: () => import('@/views/Stocks/Collections/StockHkSpot.vue'),
  meta: { title: '实时行情数据-新浪', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hk_spot_em',
  name: 'StockHkSpotEm',
  component: () => import('@/views/Stocks/Collections/StockHkSpotEm.vue'),
  meta: { title: '实时行情数据-东财', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hk_valuation_baidu',
  name: 'StockHkValuationBaidu',
  component: () => import('@/views/Stocks/Collections/StockHkValuationBaidu.vue'),
  meta: { title: '港股估值指标', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hk_valuation_comparison_em',
  name: 'StockHkValuationComparisonEm',
  component: () => import('@/views/Stocks/Collections/StockHkValuationComparisonEm.vue'),
  meta: { title: '估值对比', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hold_change_cninfo',
  name: 'StockHoldChangeCninfo',
  component: () => import('@/views/Stocks/Collections/StockHoldChangeCninfo.vue'),
  meta: { title: '股本变动', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hold_control_cninfo',
  name: 'StockHoldControlCninfo',
  component: () => import('@/views/Stocks/Collections/StockHoldControlCninfo.vue'),
  meta: { title: '实际控制人持股变动', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hold_management_detail_cninfo',
  name: 'StockHoldManagementDetailCninfo',
  component: () => import('@/views/Stocks/Collections/StockHoldManagementDetailCninfo.vue'),
  meta: { title: '高管持股变动明细', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hold_management_detail_em',
  name: 'StockHoldManagementDetailEm',
  component: () => import('@/views/Stocks/Collections/StockHoldManagementDetailEm.vue'),
  meta: { title: '董监高及相关人员持股变动明细', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hold_management_person_em',
  name: 'StockHoldManagementPersonEm',
  component: () => import('@/views/Stocks/Collections/StockHoldManagementPersonEm.vue'),
  meta: { title: '人员增减持股变动明细', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hold_num_cninfo',
  name: 'StockHoldNumCninfo',
  component: () => import('@/views/Stocks/Collections/StockHoldNumCninfo.vue'),
  meta: { title: '股东人数及持股集中度', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hot_deal_xq',
  name: 'StockHotDealXq',
  component: () => import('@/views/Stocks/Collections/StockHotDealXq.vue'),
  meta: { title: '交易排行榜', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hot_follow_xq',
  name: 'StockHotFollowXq',
  component: () => import('@/views/Stocks/Collections/StockHotFollowXq.vue'),
  meta: { title: '关注排行榜', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hot_keyword_em',
  name: 'StockHotKeywordEm',
  component: () => import('@/views/Stocks/Collections/StockHotKeywordEm.vue'),
  meta: { title: '热门关键词', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hot_rank_detail_em',
  name: 'StockHotRankDetailEm',
  component: () => import('@/views/Stocks/Collections/StockHotRankDetailEm.vue'),
  meta: { title: 'A股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hot_rank_detail_realtime_em',
  name: 'StockHotRankDetailRealtimeEm',
  component: () => import('@/views/Stocks/Collections/StockHotRankDetailRealtimeEm.vue'),
  meta: { title: 'A股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hot_rank_em',
  name: 'StockHotRankEm',
  component: () => import('@/views/Stocks/Collections/StockHotRankEm.vue'),
  meta: { title: '人气榜-A股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hot_rank_latest_em',
  name: 'StockHotRankLatestEm',
  component: () => import('@/views/Stocks/Collections/StockHotRankLatestEm.vue'),
  meta: { title: 'A股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hot_rank_relate_em',
  name: 'StockHotRankRelateEm',
  component: () => import('@/views/Stocks/Collections/StockHotRankRelateEm.vue'),
  meta: { title: '相关股票', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hot_search_baidu',
  name: 'StockHotSearchBaidu',
  component: () => import('@/views/Stocks/Collections/StockHotSearchBaidu.vue'),
  meta: { title: '热搜股票', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hot_tweet_xq',
  name: 'StockHotTweetXq',
  component: () => import('@/views/Stocks/Collections/StockHotTweetXq.vue'),
  meta: { title: '讨论排行榜', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hot_up_em',
  name: 'StockHotUpEm',
  component: () => import('@/views/Stocks/Collections/StockHotUpEm.vue'),
  meta: { title: '飙升榜-A股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_hsgt_fund_flow_summary_em',
  name: 'StockHsgtFundFlowSummaryEm',
  component: () => import('@/views/Stocks/Collections/StockHsgtFundFlowSummaryEm.vue'),
  meta: { title: '沪深港通资金流向', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_index_pb_lg',
  name: 'StockIndexPbLg',
  component: () => import('@/views/Stocks/Collections/StockIndexPbLg.vue'),
  meta: { title: '指数市净率', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_index_pe_lg',
  name: 'StockIndexPeLg',
  component: () => import('@/views/Stocks/Collections/StockIndexPeLg.vue'),
  meta: { title: '指数市盈率', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_individual_basic_info_hk_xq',
  name: 'StockIndividualBasicInfoHkXq',
  component: () => import('@/views/Stocks/Collections/StockIndividualBasicInfoHkXq.vue'),
  meta: { title: '个股信息查询-雪球', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_individual_basic_info_us_xq',
  name: 'StockIndividualBasicInfoUsXq',
  component: () => import('@/views/Stocks/Collections/StockIndividualBasicInfoUsXq.vue'),
  meta: { title: '个股信息查询-雪球', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_individual_basic_info_xq',
  name: 'StockIndividualBasicInfoXq',
  component: () => import('@/views/Stocks/Collections/StockIndividualBasicInfoXq.vue'),
  meta: { title: '个股信息查询-雪球', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_individual_info_em',
  name: 'StockIndividualInfoEm',
  component: () => import('@/views/Stocks/Collections/StockIndividualInfoEm.vue'),
  meta: { title: '个股信息查询-东财', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_individual_spot_xq',
  name: 'StockIndividualSpotXq',
  component: () => import('@/views/Stocks/Collections/StockIndividualSpotXq.vue'),
  meta: { title: '实时行情数据-雪球', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_industry_category_cninfo',
  name: 'StockIndustryCategoryCninfo',
  component: () => import('@/views/Stocks/Collections/StockIndustryCategoryCninfo.vue'),
  meta: { title: '行业分类数据-巨潮资讯', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_industry_change_cninfo',
  name: 'StockIndustryChangeCninfo',
  component: () => import('@/views/Stocks/Collections/StockIndustryChangeCninfo.vue'),
  meta: { title: '上市公司行业归属的变动情况-巨潮资讯', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_industry_clf_hist_sw',
  name: 'StockIndustryClfHistSw',
  component: () => import('@/views/Stocks/Collections/StockIndustryClfHistSw.vue'),
  meta: { title: '申万个股行业分类变动历史', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_industry_pe_ratio_cninfo',
  name: 'StockIndustryPeRatioCninfo',
  component: () => import('@/views/Stocks/Collections/StockIndustryPeRatioCninfo.vue'),
  meta: { title: '行业市盈率', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_info_a_code_name',
  name: 'StockInfoACodeName',
  component: () => import('@/views/Stocks/Collections/StockInfoACodeName.vue'),
  meta: { title: '股票列表-A股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_info_bj_name_code',
  name: 'StockInfoBjNameCode',
  component: () => import('@/views/Stocks/Collections/StockInfoBjNameCode.vue'),
  meta: { title: '股票列表-北证', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_info_change_name',
  name: 'StockInfoChangeName',
  component: () => import('@/views/Stocks/Collections/StockInfoChangeName.vue'),
  meta: { title: '股票更名', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_info_sh_delist',
  name: 'StockInfoShDelist',
  component: () => import('@/views/Stocks/Collections/StockInfoShDelist.vue'),
  meta: { title: '暂停-终止上市-上证', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_info_sh_name_code',
  name: 'StockInfoShNameCode',
  component: () => import('@/views/Stocks/Collections/StockInfoShNameCode.vue'),
  meta: { title: '股票列表-上证', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_info_sz_change_name',
  name: 'StockInfoSzChangeName',
  component: () => import('@/views/Stocks/Collections/StockInfoSzChangeName.vue'),
  meta: { title: '名称变更-深证', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_info_sz_delist',
  name: 'StockInfoSzDelist',
  component: () => import('@/views/Stocks/Collections/StockInfoSzDelist.vue'),
  meta: { title: '终止-暂停上市-深证', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_info_sz_name_code',
  name: 'StockInfoSzNameCode',
  component: () => import('@/views/Stocks/Collections/StockInfoSzNameCode.vue'),
  meta: { title: '股票列表-深证', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_inner_trade_xq',
  name: 'StockInnerTradeXq',
  component: () => import('@/views/Stocks/Collections/StockInnerTradeXq.vue'),
  meta: { title: '内部交易', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_institute_hold',
  name: 'StockInstituteHold',
  component: () => import('@/views/Stocks/Collections/StockInstituteHold.vue'),
  meta: { title: '机构持股一览表', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_institute_hold_detail',
  name: 'StockInstituteHoldDetail',
  component: () => import('@/views/Stocks/Collections/StockInstituteHoldDetail.vue'),
  meta: { title: '机构持股详情', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_institute_recommend',
  name: 'StockInstituteRecommend',
  component: () => import('@/views/Stocks/Collections/StockInstituteRecommend.vue'),
  meta: { title: '机构推荐池', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_institute_recommend_detail',
  name: 'StockInstituteRecommendDetail',
  component: () => import('@/views/Stocks/Collections/StockInstituteRecommendDetail.vue'),
  meta: { title: '股票评级记录', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_intraday_em',
  name: 'StockIntradayEm',
  component: () => import('@/views/Stocks/Collections/StockIntradayEm.vue'),
  meta: { title: '日内分时数据-东财', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_intraday_sina',
  name: 'StockIntradaySina',
  component: () => import('@/views/Stocks/Collections/StockIntradaySina.vue'),
  meta: { title: '日内分时数据-新浪', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_ipo_benefit_ths',
  name: 'StockIpoBenefitThs',
  component: () => import('@/views/Stocks/Collections/StockIpoBenefitThs.vue'),
  meta: { title: 'IPO 受益股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_ipo_declare',
  name: 'StockIpoDeclare',
  component: () => import('@/views/Stocks/Collections/StockIpoDeclare.vue'),
  meta: { title: '首发申报信息', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_ipo_summary_cninfo',
  name: 'StockIpoSummaryCninfo',
  component: () => import('@/views/Stocks/Collections/StockIpoSummaryCninfo.vue'),
  meta: { title: '上市相关-巨潮资讯', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_irm_ans_cninfo',
  name: 'StockIrmAnsCninfo',
  component: () => import('@/views/Stocks/Collections/StockIrmAnsCninfo.vue'),
  meta: { title: '互动易-回答', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_irm_cninfo',
  name: 'StockIrmCninfo',
  component: () => import('@/views/Stocks/Collections/StockIrmCninfo.vue'),
  meta: { title: '互动易-提问', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_kc_a_spot_em',
  name: 'StockKcASpotEm',
  component: () => import('@/views/Stocks/Collections/StockKcASpotEm.vue'),
  meta: { title: '科创板', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_lh_yyb_capital',
  name: 'StockLhYybCapital',
  component: () => import('@/views/Stocks/Collections/StockLhYybCapital.vue'),
  meta: { title: '龙虎榜-营业部排行-资金实力最强', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_lh_yyb_control',
  name: 'StockLhYybControl',
  component: () => import('@/views/Stocks/Collections/StockLhYybControl.vue'),
  meta: { title: '龙虎榜-营业部排行-抱团操作实力', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_lh_yyb_most',
  name: 'StockLhYybMost',
  component: () => import('@/views/Stocks/Collections/StockLhYybMost.vue'),
  meta: { title: '龙虎榜-营业部排行-上榜次数最多', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_lhb_detail_daily_sina',
  name: 'StockLhbDetailDailySina',
  component: () => import('@/views/Stocks/Collections/StockLhbDetailDailySina.vue'),
  meta: { title: '龙虎榜-每日详情', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_lhb_detail_em',
  name: 'StockLhbDetailEm',
  component: () => import('@/views/Stocks/Collections/StockLhbDetailEm.vue'),
  meta: { title: '龙虎榜详情', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_lhb_ggtj_sina',
  name: 'StockLhbGgtjSina',
  component: () => import('@/views/Stocks/Collections/StockLhbGgtjSina.vue'),
  meta: { title: '龙虎榜-个股上榜统计', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_lhb_hyyyb_em',
  name: 'StockLhbHyyybEm',
  component: () => import('@/views/Stocks/Collections/StockLhbHyyybEm.vue'),
  meta: { title: '每日活跃营业部', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_lhb_jgmmtj_em',
  name: 'StockLhbJgmmtjEm',
  component: () => import('@/views/Stocks/Collections/StockLhbJgmmtjEm.vue'),
  meta: { title: '机构买卖每日统计', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_lhb_jgmx_sina',
  name: 'StockLhbJgmxSina',
  component: () => import('@/views/Stocks/Collections/StockLhbJgmxSina.vue'),
  meta: { title: '龙虎榜-机构席位成交明细', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_lhb_jgstatistic_em',
  name: 'StockLhbJgstatisticEm',
  component: () => import('@/views/Stocks/Collections/StockLhbJgstatisticEm.vue'),
  meta: { title: '机构席位追踪', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_lhb_jgzz_sina',
  name: 'StockLhbJgzzSina',
  component: () => import('@/views/Stocks/Collections/StockLhbJgzzSina.vue'),
  meta: { title: '龙虎榜-机构席位追踪', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_lhb_stock_detail_em',
  name: 'StockLhbStockDetailEm',
  component: () => import('@/views/Stocks/Collections/StockLhbStockDetailEm.vue'),
  meta: { title: '个股龙虎榜详情', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_lhb_stock_statistic_em',
  name: 'StockLhbStockStatisticEm',
  component: () => import('@/views/Stocks/Collections/StockLhbStockStatisticEm.vue'),
  meta: { title: '个股上榜统计', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_lhb_traderstatistic_em',
  name: 'StockLhbTraderstatisticEm',
  component: () => import('@/views/Stocks/Collections/StockLhbTraderstatisticEm.vue'),
  meta: { title: '营业部统计', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_lhb_yyb_detail_em',
  name: 'StockLhbYybDetailEm',
  component: () => import('@/views/Stocks/Collections/StockLhbYybDetailEm.vue'),
  meta: { title: '营业部详情数据-东财', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_lhb_yybph_em',
  name: 'StockLhbYybphEm',
  component: () => import('@/views/Stocks/Collections/StockLhbYybphEm.vue'),
  meta: { title: '营业部排行', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_lhb_yytj_sina',
  name: 'StockLhbYytjSina',
  component: () => import('@/views/Stocks/Collections/StockLhbYytjSina.vue'),
  meta: { title: '龙虎榜-营业上榜统计', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_lrb_em',
  name: 'StockLrbEm',
  component: () => import('@/views/Stocks/Collections/StockLrbEm.vue'),
  meta: { title: '利润表', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_main_stock_holder',
  name: 'StockMainStockHolder',
  component: () => import('@/views/Stocks/Collections/StockMainStockHolder.vue'),
  meta: { title: '主要股东', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_margin_account_info',
  name: 'StockMarginAccountInfo',
  component: () => import('@/views/Stocks/Collections/StockMarginAccountInfo.vue'),
  meta: { title: '两融账户信息', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_margin_detail_sse',
  name: 'StockMarginDetailSse',
  component: () => import('@/views/Stocks/Collections/StockMarginDetailSse.vue'),
  meta: { title: '融资融券明细', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_margin_detail_szse',
  name: 'StockMarginDetailSzse',
  component: () => import('@/views/Stocks/Collections/StockMarginDetailSzse.vue'),
  meta: { title: '融资融券明细', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_margin_ratio_pa',
  name: 'StockMarginRatioPa',
  component: () => import('@/views/Stocks/Collections/StockMarginRatioPa.vue'),
  meta: { title: '标的证券名单及保证金比例查询', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_margin_sse',
  name: 'StockMarginSse',
  component: () => import('@/views/Stocks/Collections/StockMarginSse.vue'),
  meta: { title: '融资融券汇总', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_margin_szse',
  name: 'StockMarginSzse',
  component: () => import('@/views/Stocks/Collections/StockMarginSzse.vue'),
  meta: { title: '融资融券汇总', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_margin_underlying_info_szse',
  name: 'StockMarginUnderlyingInfoSzse',
  component: () => import('@/views/Stocks/Collections/StockMarginUnderlyingInfoSzse.vue'),
  meta: { title: '标的证券信息', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_market_activity_legu',
  name: 'StockMarketActivityLegu',
  component: () => import('@/views/Stocks/Collections/StockMarketActivityLegu.vue'),
  meta: { title: '赚钱效应分析', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_market_pb_lg',
  name: 'StockMarketPbLg',
  component: () => import('@/views/Stocks/Collections/StockMarketPbLg.vue'),
  meta: { title: '主板市净率', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_market_pe_lg',
  name: 'StockMarketPeLg',
  component: () => import('@/views/Stocks/Collections/StockMarketPeLg.vue'),
  meta: { title: '主板市盈率', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_new_a_spot_em',
  name: 'StockNewASpotEm',
  component: () => import('@/views/Stocks/Collections/StockNewASpotEm.vue'),
  meta: { title: '新股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_new_gh_cninfo',
  name: 'StockNewGhCninfo',
  component: () => import('@/views/Stocks/Collections/StockNewGhCninfo.vue'),
  meta: { title: '新股过会', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_new_ipo_cninfo',
  name: 'StockNewIpoCninfo',
  component: () => import('@/views/Stocks/Collections/StockNewIpoCninfo.vue'),
  meta: { title: '新股发行', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_news_main_cx',
  name: 'StockNewsMainCx',
  component: () => import('@/views/Stocks/Collections/StockNewsMainCx.vue'),
  meta: { title: '财经内容精选', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_pg_em',
  name: 'StockPgEm',
  component: () => import('@/views/Stocks/Collections/StockPgEm.vue'),
  meta: { title: '配股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_price_js',
  name: 'StockPriceJs',
  component: () => import('@/views/Stocks/Collections/StockPriceJs.vue'),
  meta: { title: '美港目标价', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_profile_cninfo',
  name: 'StockProfileCninfo',
  component: () => import('@/views/Stocks/Collections/StockProfileCninfo.vue'),
  meta: { title: '公司概况-巨潮资讯', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_profit_forecast_em',
  name: 'StockProfitForecastEm',
  component: () => import('@/views/Stocks/Collections/StockProfitForecastEm.vue'),
  meta: { title: '盈利预测-东方财富', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_profit_forecast_ths',
  name: 'StockProfitForecastThs',
  component: () => import('@/views/Stocks/Collections/StockProfitForecastThs.vue'),
  meta: { title: '盈利预测-同花顺', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_profit_sheet_by_report_em',
  name: 'StockProfitSheetByReportEm',
  component: () => import('@/views/Stocks/Collections/StockProfitSheetByReportEm.vue'),
  meta: { title: '利润表-按报告期', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_profit_sheet_by_yearly_em',
  name: 'StockProfitSheetByYearlyEm',
  component: () => import('@/views/Stocks/Collections/StockProfitSheetByYearlyEm.vue'),
  meta: { title: '利润表-按年度', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_qbzf_em',
  name: 'StockQbzfEm',
  component: () => import('@/views/Stocks/Collections/StockQbzfEm.vue'),
  meta: { title: '增发', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_qsjy_em',
  name: 'StockQsjyEm',
  component: () => import('@/views/Stocks/Collections/StockQsjyEm.vue'),
  meta: { title: '券商业绩月报', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_rank_cxfl_ths',
  name: 'StockRankCxflThs',
  component: () => import('@/views/Stocks/Collections/StockRankCxflThs.vue'),
  meta: { title: '持续放量', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_rank_cxsl_ths',
  name: 'StockRankCxslThs',
  component: () => import('@/views/Stocks/Collections/StockRankCxslThs.vue'),
  meta: { title: '持续缩量', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_rank_forecast_cninfo',
  name: 'StockRankForecastCninfo',
  component: () => import('@/views/Stocks/Collections/StockRankForecastCninfo.vue'),
  meta: { title: '投资评级', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_rank_ljqd_ths',
  name: 'StockRankLjqdThs',
  component: () => import('@/views/Stocks/Collections/StockRankLjqdThs.vue'),
  meta: { title: '量价齐跌', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_rank_ljqs_ths',
  name: 'StockRankLjqsThs',
  component: () => import('@/views/Stocks/Collections/StockRankLjqsThs.vue'),
  meta: { title: '量价齐升', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_rank_xstp_ths',
  name: 'StockRankXstpThs',
  component: () => import('@/views/Stocks/Collections/StockRankXstpThs.vue'),
  meta: { title: '向上突破', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_rank_xxtp_ths',
  name: 'StockRankXxtpThs',
  component: () => import('@/views/Stocks/Collections/StockRankXxtpThs.vue'),
  meta: { title: '向下突破', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_rank_xzjp_ths',
  name: 'StockRankXzjpThs',
  component: () => import('@/views/Stocks/Collections/StockRankXzjpThs.vue'),
  meta: { title: '险资举牌', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_register_bj',
  name: 'StockRegisterBj',
  component: () => import('@/views/Stocks/Collections/StockRegisterBj.vue'),
  meta: { title: '北交所', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_register_cyb',
  name: 'StockRegisterCyb',
  component: () => import('@/views/Stocks/Collections/StockRegisterCyb.vue'),
  meta: { title: '创业板', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_register_db',
  name: 'StockRegisterDb',
  component: () => import('@/views/Stocks/Collections/StockRegisterDb.vue'),
  meta: { title: '达标企业', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_register_kcb',
  name: 'StockRegisterKcb',
  component: () => import('@/views/Stocks/Collections/StockRegisterKcb.vue'),
  meta: { title: '科创板', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_register_sh',
  name: 'StockRegisterSh',
  component: () => import('@/views/Stocks/Collections/StockRegisterSh.vue'),
  meta: { title: '上海主板', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_register_sz',
  name: 'StockRegisterSz',
  component: () => import('@/views/Stocks/Collections/StockRegisterSz.vue'),
  meta: { title: '深圳主板', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_report_disclosure',
  name: 'StockReportDisclosure',
  component: () => import('@/views/Stocks/Collections/StockReportDisclosure.vue'),
  meta: { title: '预约披露时间-巨潮资讯', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_report_fund_hold',
  name: 'StockReportFundHold',
  component: () => import('@/views/Stocks/Collections/StockReportFundHold.vue'),
  meta: { title: '基金持股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_report_fund_hold_detail',
  name: 'StockReportFundHoldDetail',
  component: () => import('@/views/Stocks/Collections/StockReportFundHoldDetail.vue'),
  meta: { title: '基金持股明细', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_repurchase_em',
  name: 'StockRepurchaseEm',
  component: () => import('@/views/Stocks/Collections/StockRepurchaseEm.vue'),
  meta: { title: '股票回购数据', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_restricted_release_detail_em',
  name: 'StockRestrictedReleaseDetailEm',
  component: () => import('@/views/Stocks/Collections/StockRestrictedReleaseDetailEm.vue'),
  meta: { title: '限售股解禁详情', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_restricted_release_queue_sina',
  name: 'StockRestrictedReleaseQueueSina',
  component: () => import('@/views/Stocks/Collections/StockRestrictedReleaseQueueSina.vue'),
  meta: { title: '个股限售解禁-新浪', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_restricted_release_stockholder_em',
  name: 'StockRestrictedReleaseStockholderEm',
  component: () => import('@/views/Stocks/Collections/StockRestrictedReleaseStockholderEm.vue'),
  meta: { title: '解禁股东', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_restricted_release_summary_em',
  name: 'StockRestrictedReleaseSummaryEm',
  component: () => import('@/views/Stocks/Collections/StockRestrictedReleaseSummaryEm.vue'),
  meta: { title: '限售股解禁', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_sector_detail',
  name: 'StockSectorDetail',
  component: () => import('@/views/Stocks/Collections/StockSectorDetail.vue'),
  meta: { title: '板块详情', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_sector_spot',
  name: 'StockSectorSpot',
  component: () => import('@/views/Stocks/Collections/StockSectorSpot.vue'),
  meta: { title: '板块行情', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_sgt_settlement_exchange_rate_sse',
  name: 'StockSgtSettlementExchangeRateSse',
  component: () => import('@/views/Stocks/Collections/StockSgtSettlementExchangeRateSse.vue'),
  meta: { title: '结算汇率-沪港通', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_sgt_settlement_exchange_rate_szse',
  name: 'StockSgtSettlementExchangeRateSzse',
  component: () => import('@/views/Stocks/Collections/StockSgtSettlementExchangeRateSzse.vue'),
  meta: { title: '结算汇率-深港通', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_sh_a_spot_em',
  name: 'StockShASpotEm',
  component: () => import('@/views/Stocks/Collections/StockShASpotEm.vue'),
  meta: { title: '沪 A 股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_share_change_cninfo',
  name: 'StockShareChangeCninfo',
  component: () => import('@/views/Stocks/Collections/StockShareChangeCninfo.vue'),
  meta: { title: '公司股本变动-巨潮资讯', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_share_hold_change_bse',
  name: 'StockShareHoldChangeBse',
  component: () => import('@/views/Stocks/Collections/StockShareHoldChangeBse.vue'),
  meta: { title: '董监高及相关人员持股变动-北证', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_share_hold_change_sse',
  name: 'StockShareHoldChangeSse',
  component: () => import('@/views/Stocks/Collections/StockShareHoldChangeSse.vue'),
  meta: { title: '董监高及相关人员持股变动-上证', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_share_hold_change_szse',
  name: 'StockShareHoldChangeSzse',
  component: () => import('@/views/Stocks/Collections/StockShareHoldChangeSzse.vue'),
  meta: { title: '董监高及相关人员持股变动-深证', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_sns_sseinfo',
  name: 'StockSnsSseinfo',
  component: () => import('@/views/Stocks/Collections/StockSnsSseinfo.vue'),
  meta: { title: '上证e互动', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_sse_deal_daily',
  name: 'StockSseDealDaily',
  component: () => import('@/views/Stocks/Collections/StockSseDealDaily.vue'),
  meta: { title: '上海证券交易所-每日概况', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_sse_summary',
  name: 'StockSseSummary',
  component: () => import('@/views/Stocks/Collections/StockSseSummary.vue'),
  meta: { title: '上海证券交易所', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_staq_net_stop',
  name: 'StockStaqNetStop',
  component: () => import('@/views/Stocks/Collections/StockStaqNetStop.vue'),
  meta: { title: '两网及退市', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_sy_em',
  name: 'StockSyEm',
  component: () => import('@/views/Stocks/Collections/StockSyEm.vue'),
  meta: { title: '个股商誉明细', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_sy_hy_em',
  name: 'StockSyHyEm',
  component: () => import('@/views/Stocks/Collections/StockSyHyEm.vue'),
  meta: { title: '行业商誉', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_sy_jz_em',
  name: 'StockSyJzEm',
  component: () => import('@/views/Stocks/Collections/StockSyJzEm.vue'),
  meta: { title: '个股商誉减值明细', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_sy_profile_em',
  name: 'StockSyProfileEm',
  component: () => import('@/views/Stocks/Collections/StockSyProfileEm.vue'),
  meta: { title: 'A股商誉市场概况', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_sy_yq_em',
  name: 'StockSyYqEm',
  component: () => import('@/views/Stocks/Collections/StockSyYqEm.vue'),
  meta: { title: '商誉减值预期明细', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_sz_a_spot_em',
  name: 'StockSzASpotEm',
  component: () => import('@/views/Stocks/Collections/StockSzASpotEm.vue'),
  meta: { title: '深 A 股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_szse_area_summary',
  name: 'StockSzseAreaSummary',
  component: () => import('@/views/Stocks/Collections/StockSzseAreaSummary.vue'),
  meta: { title: '地区交易排序', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_szse_sector_summary',
  name: 'StockSzseSectorSummary',
  component: () => import('@/views/Stocks/Collections/StockSzseSectorSummary.vue'),
  meta: { title: '股票行业成交', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_szse_summary',
  name: 'StockSzseSummary',
  component: () => import('@/views/Stocks/Collections/StockSzseSummary.vue'),
  meta: { title: '证券类别统计', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_us_daily',
  name: 'StockUsDaily',
  component: () => import('@/views/Stocks/Collections/StockUsDaily.vue'),
  meta: { title: '历史行情数据-新浪', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_us_famous_spot_em',
  name: 'StockUsFamousSpotEm',
  component: () => import('@/views/Stocks/Collections/StockUsFamousSpotEm.vue'),
  meta: { title: '知名美股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_us_hist',
  name: 'StockUsHist',
  component: () => import('@/views/Stocks/Collections/StockUsHist.vue'),
  meta: { title: '历史行情数据-东财', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_us_hist_min_em',
  name: 'StockUsHistMinEm',
  component: () => import('@/views/Stocks/Collections/StockUsHistMinEm.vue'),
  meta: { title: '分时数据-东财', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_us_pink_spot_em',
  name: 'StockUsPinkSpotEm',
  component: () => import('@/views/Stocks/Collections/StockUsPinkSpotEm.vue'),
  meta: { title: '粉单市场', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_us_spot',
  name: 'StockUsSpot',
  component: () => import('@/views/Stocks/Collections/StockUsSpot.vue'),
  meta: { title: '实时行情数据-新浪', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_us_spot_em',
  name: 'StockUsSpotEm',
  component: () => import('@/views/Stocks/Collections/StockUsSpotEm.vue'),
  meta: { title: '实时行情数据-东财', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_value_em',
  name: 'StockValueEm',
  component: () => import('@/views/Stocks/Collections/StockValueEm.vue'),
  meta: { title: '个股估值', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_xgsr_ths',
  name: 'StockXgsrThs',
  component: () => import('@/views/Stocks/Collections/StockXgsrThs.vue'),
  meta: { title: '新股上市首日', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_xjll_em',
  name: 'StockXjllEm',
  component: () => import('@/views/Stocks/Collections/StockXjllEm.vue'),
  meta: { title: '现金流量表', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_yjbb_em',
  name: 'StockYjbbEm',
  component: () => import('@/views/Stocks/Collections/StockYjbbEm.vue'),
  meta: { title: '业绩报表', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_yjkb_em',
  name: 'StockYjkbEm',
  component: () => import('@/views/Stocks/Collections/StockYjkbEm.vue'),
  meta: { title: '业绩快报', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_yzxdr_em',
  name: 'StockYzxdrEm',
  component: () => import('@/views/Stocks/Collections/StockYzxdrEm.vue'),
  meta: { title: '一致行动人', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zcfz_bj_em',
  name: 'StockZcfzBjEm',
  component: () => import('@/views/Stocks/Collections/StockZcfzBjEm.vue'),
  meta: { title: '资产负债表-北交所', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zcfz_em',
  name: 'StockZcfzEm',
  component: () => import('@/views/Stocks/Collections/StockZcfzEm.vue'),
  meta: { title: '资产负债表-沪深', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_a_cdr_daily',
  name: 'StockZhACdrDaily',
  component: () => import('@/views/Stocks/Collections/StockZhACdrDaily.vue'),
  meta: { title: '历史行情数据', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_a_daily',
  name: 'StockZhADaily',
  component: () => import('@/views/Stocks/Collections/StockZhADaily.vue'),
  meta: { title: '历史行情数据-新浪', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_a_disclosure_relation_cninfo',
  name: 'StockZhADisclosureRelationCninfo',
  component: () => import('@/views/Stocks/Collections/StockZhADisclosureRelationCninfo.vue'),
  meta: { title: '信息披露调研-巨潮资讯', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_a_disclosure_report_cninfo',
  name: 'StockZhADisclosureReportCninfo',
  component: () => import('@/views/Stocks/Collections/StockZhADisclosureReportCninfo.vue'),
  meta: { title: '信息披露公告-巨潮资讯', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_a_gbjg_em',
  name: 'StockZhAGbjgEm',
  component: () => import('@/views/Stocks/Collections/StockZhAGbjgEm.vue'),
  meta: { title: '股本结构', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_a_gdhs',
  name: 'StockZhAGdhs',
  component: () => import('@/views/Stocks/Collections/StockZhAGdhs.vue'),
  meta: { title: '股东户数', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_a_gdhs_detail_em',
  name: 'StockZhAGdhsDetailEm',
  component: () => import('@/views/Stocks/Collections/StockZhAGdhsDetailEm.vue'),
  meta: { title: '股东户数详情', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_a_hist',
  name: 'StockZhAHist',
  component: () => import('@/views/Stocks/Collections/StockZhAHist.vue'),
  meta: { title: 'A股历史行情-东财', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_a_hist_min_em',
  name: 'StockZhAHistMinEm',
  component: () => import('@/views/Stocks/Collections/StockZhAHistMinEm.vue'),
  meta: { title: 'A股分时数据-东财', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_a_hist_pre_min_em',
  name: 'StockZhAHistPreMinEm',
  component: () => import('@/views/Stocks/Collections/StockZhAHistPreMinEm.vue'),
  meta: { title: '盘前数据', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_a_hist_tx',
  name: 'StockZhAHistTx',
  component: () => import('@/views/Stocks/Collections/StockZhAHistTx.vue'),
  meta: { title: '历史行情数据-腾讯', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_a_minute',
  name: 'StockZhAMinute',
  component: () => import('@/views/Stocks/Collections/StockZhAMinute.vue'),
  meta: { title: '分时数据-新浪', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_a_new_em',
  name: 'StockZhANewEm',
  component: () => import('@/views/Stocks/Collections/StockZhANewEm.vue'),
  meta: { title: '新股', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_a_spot',
  name: 'StockZhASpot',
  component: () => import('@/views/Stocks/Collections/StockZhASpot.vue'),
  meta: { title: '实时行情数据-新浪', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_a_spot_em',
  name: 'StockZhASpotEm',
  component: () => import('@/views/Stocks/Collections/StockZhASpotEm.vue'),
  meta: { title: '沪深京A股实时行情-东财', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_a_st_em',
  name: 'StockZhAStEm',
  component: () => import('@/views/Stocks/Collections/StockZhAStEm.vue'),
  meta: { title: '风险警示板', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_a_stop_em',
  name: 'StockZhAStopEm',
  component: () => import('@/views/Stocks/Collections/StockZhAStopEm.vue'),
  meta: { title: '两网及退市', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_a_tick_tx',
  name: 'StockZhATickTx',
  component: () => import('@/views/Stocks/Collections/StockZhATickTx.vue'),
  meta: { title: '腾讯财经', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_ab_comparison_em',
  name: 'StockZhAbComparisonEm',
  component: () => import('@/views/Stocks/Collections/StockZhAbComparisonEm.vue'),
  meta: { title: 'AB 股比价', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_ah_daily',
  name: 'StockZhAhDaily',
  component: () => import('@/views/Stocks/Collections/StockZhAhDaily.vue'),
  meta: { title: '历史行情数据', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_ah_name',
  name: 'StockZhAhName',
  component: () => import('@/views/Stocks/Collections/StockZhAhName.vue'),
  meta: { title: 'A+H股票字典', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_ah_spot',
  name: 'StockZhAhSpot',
  component: () => import('@/views/Stocks/Collections/StockZhAhSpot.vue'),
  meta: { title: '实时行情数据-腾讯', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_ah_spot_em',
  name: 'StockZhAhSpotEm',
  component: () => import('@/views/Stocks/Collections/StockZhAhSpotEm.vue'),
  meta: { title: '实时行情数据-东财', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_b_daily',
  name: 'StockZhBDaily',
  component: () => import('@/views/Stocks/Collections/StockZhBDaily.vue'),
  meta: { title: '历史行情数据', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_b_minute',
  name: 'StockZhBMinute',
  component: () => import('@/views/Stocks/Collections/StockZhBMinute.vue'),
  meta: { title: '分时数据', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_b_spot',
  name: 'StockZhBSpot',
  component: () => import('@/views/Stocks/Collections/StockZhBSpot.vue'),
  meta: { title: '实时行情数据-新浪', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_b_spot_em',
  name: 'StockZhBSpotEm',
  component: () => import('@/views/Stocks/Collections/StockZhBSpotEm.vue'),
  meta: { title: '实时行情数据-东财', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_dupont_comparison_em',
  name: 'StockZhDupontComparisonEm',
  component: () => import('@/views/Stocks/Collections/StockZhDupontComparisonEm.vue'),
  meta: { title: '杜邦分析比较', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_growth_comparison_em',
  name: 'StockZhGrowthComparisonEm',
  component: () => import('@/views/Stocks/Collections/StockZhGrowthComparisonEm.vue'),
  meta: { title: '成长性比较', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_kcb_daily',
  name: 'StockZhKcbDaily',
  component: () => import('@/views/Stocks/Collections/StockZhKcbDaily.vue'),
  meta: { title: '历史行情数据', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_kcb_report_em',
  name: 'StockZhKcbReportEm',
  component: () => import('@/views/Stocks/Collections/StockZhKcbReportEm.vue'),
  meta: { title: '科创板公告', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_kcb_spot',
  name: 'StockZhKcbSpot',
  component: () => import('@/views/Stocks/Collections/StockZhKcbSpot.vue'),
  meta: { title: '实时行情数据', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_scale_comparison_em',
  name: 'StockZhScaleComparisonEm',
  component: () => import('@/views/Stocks/Collections/StockZhScaleComparisonEm.vue'),
  meta: { title: '公司规模', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_valuation_baidu',
  name: 'StockZhValuationBaidu',
  component: () => import('@/views/Stocks/Collections/StockZhValuationBaidu.vue'),
  meta: { title: 'A 股估值指标', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_valuation_comparison_em',
  name: 'StockZhValuationComparisonEm',
  component: () => import('@/views/Stocks/Collections/StockZhValuationComparisonEm.vue'),
  meta: { title: '估值比较', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zh_vote_baidu',
  name: 'StockZhVoteBaidu',
  component: () => import('@/views/Stocks/Collections/StockZhVoteBaidu.vue'),
  meta: { title: '涨跌投票', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zt_pool_dtgc_em',
  name: 'StockZtPoolDtgcEm',
  component: () => import('@/views/Stocks/Collections/StockZtPoolDtgcEm.vue'),
  meta: { title: '跌停股池', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zt_pool_em',
  name: 'StockZtPoolEm',
  component: () => import('@/views/Stocks/Collections/StockZtPoolEm.vue'),
  meta: { title: '涨停股池', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zt_pool_previous_em',
  name: 'StockZtPoolPreviousEm',
  component: () => import('@/views/Stocks/Collections/StockZtPoolPreviousEm.vue'),
  meta: { title: '昨日涨停股池', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zt_pool_strong_em',
  name: 'StockZtPoolStrongEm',
  component: () => import('@/views/Stocks/Collections/StockZtPoolStrongEm.vue'),
  meta: { title: '强势股池', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zt_pool_sub_new_em',
  name: 'StockZtPoolSubNewEm',
  component: () => import('@/views/Stocks/Collections/StockZtPoolSubNewEm.vue'),
  meta: { title: '次新股池', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zt_pool_zbgc_em',
  name: 'StockZtPoolZbgcEm',
  component: () => import('@/views/Stocks/Collections/StockZtPoolZbgcEm.vue'),
  meta: { title: '炸板股池', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zygc_em',
  name: 'StockZygcEm',
  component: () => import('@/views/Stocks/Collections/StockZygcEm.vue'),
  meta: { title: '主营构成-东财', requiresAuth: true }
},
{
  path: '/stocks/collections/stock_zyjs_ths',
  name: 'StockZyjsThs',
  component: () => import('@/views/Stocks/Collections/StockZyjsThs.vue'),
  meta: { title: '主营介绍-同花顺', requiresAuth: true }
},
]

export default generatedRoutes
