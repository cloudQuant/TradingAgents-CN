# 期权数据集合 API 更新功能测试报告

## 测试时间: 2025-12-14 19:06:46

## 测试摘要

| 测试项 | 总数 | 成功 | 跳过 | 失败 | 成功率 |

|--------|------|------|------|------|--------|

| 刷新功能 | 42 | 41 | 1 | 0 | 100.0% |

| 数据获取 | 42 | 42 | - | 0 | 100.0% |

## 详细测试结果

| 序号 | 集合名称 | 显示名称 | 刷新状态 | 数据状态 | 数据量 |

|------|----------|----------|----------|----------|--------|

| 1 | option_contract_info_ctp | openctp 期权合约信息 | ✓ 成功 | ✓ 成功 | 20028 |

| 2 | option_finance_board | 金融期权行情数据 | ✓ 成功 | ✓ 成功 | 102 |

| 3 | option_risk_indicator_sse | 上交所期权风险指标 | ✓ 成功 | ✓ 成功 | 720 |

| 4 | option_current_day_sse | 上交所当日合约 | ✓ 成功 | ✓ 成功 | 650 |

| 5 | option_current_day_szse | 深交所当日合约 | ✓ 成功 | ✓ 成功 | 766 |

| 6 | option_daily_stats_sse | 上交所每日统计 | ✓ 成功 | ✓ 成功 | 5 |

| 7 | option_daily_stats_szse | 深交所日度概况 | ✓ 成功 | ✓ 成功 | 1 |

| 8 | option_cffex_sz50_list_sina | 中金所上证 50 指数合约列表 | ✓ 成功 | ✓ 成功 | 6 |

| 9 | option_cffex_hs300_list_sina | 中金所沪深 300 指数合约列表 | ✓ 成功 | ✓ 成功 | 6 |

| 10 | option_cffex_zz1000_list_sina | 中金所中证 1000 指数合约列表 | ✓ 成功 | ✓ 成功 | 6 |

| 11 | option_cffex_sz50_spot_sina | 中金所上证 50 指数实时行情 | ✓ 成功 | ✓ 成功 | 161 |

| 12 | option_cffex_hs300_spot_sina | 中金所沪深 300 指数实时行情 | ✓ 成功 | ✓ 成功 | 256 |

| 13 | option_cffex_zz1000_spot_sina | 中金所中证 1000 指数实时行情 | ✓ 成功 | ✓ 成功 | 248 |

| 14 | option_cffex_sz50_daily_sina | 中金所上证 50 指数日频行情 | ✓ 成功 | ✓ 成功 | 1 |

| 15 | option_cffex_hs300_daily_sina | 中金所沪深 300 指数日频行情 | ✓ 成功 | ✓ 成功 | 1 |

| 16 | option_cffex_zz1000_daily_sina | 中金所中证 1000 指数日频行情 | ✓ 成功 | ✓ 成功 | 1 |

| 17 | option_sse_list_sina | 上交所 50ETF 合约到期月份列表 | ✓ 成功 | ✓ 成功 | 4 |

| 18 | option_sse_expire_day_sina | 剩余到期时间 | ✓ 成功 | ✓ 成功 | 1 |

| 19 | option_sse_codes_sina | 看涨看跌合约代码 | ✓ 成功 | ✓ 成功 | 1 |

| 20 | option_sse_spot_price_sina | 期权实时数据 | ⊘ 跳过 | ✓ 成功 | 1 |

| 21 | option_sse_underlying_spot_price_sina | 期权标的物实时数据 | ✓ 成功 | ✓ 成功 | 34 |

| 22 | option_sse_greeks_sina | 期权希腊字母信息表 | ✓ 成功 | ✓ 成功 | 2 |

| 23 | option_sse_minute_sina | 期权分钟数据 | ✓ 成功 | ✓ 成功 | 0 |

| 24 | option_sse_daily_sina | 期权日数据 | ✓ 成功 | ✓ 成功 | 38 |

| 25 | option_finance_minute_sina | 金融期权股票期权分时行情 | ✓ 成功 | ✓ 成功 | 1204 |

| 26 | option_minute_em | 东财期权分时行情 | ✓ 成功 | ✓ 成功 | 0 |

| 27 | option_current_em | 东财期权行情 | ✓ 成功 | ✓ 成功 | 0 |

| 28 | option_lhb_em | 期权龙虎榜 | ✓ 成功 | ✓ 成功 | 1 |

| 29 | option_value_analysis_em | 期权价值分析 | ✓ 成功 | ✓ 成功 | 0 |

| 30 | option_risk_analysis_em | 期权风险分析 | ✓ 成功 | ✓ 成功 | 0 |

| 31 | option_premium_analysis_em | 期权折溢价 | ✓ 成功 | ✓ 成功 | 0 |

| 32 | option_commodity_contract_sina | 商品期权当前合约 | ✓ 成功 | ✓ 成功 | 1 |

| 33 | option_commodity_contract_table_sina | 商品期权 T 型报价表 | ✓ 成功 | ✓ 成功 | 77 |

| 34 | option_commodity_hist_sina | 商品期权历史行情 | ✓ 成功 | ✓ 成功 | 1 |

| 35 | option_comm_info | 商品期权手续费 | ✓ 成功 | ✓ 成功 | 1 |

| 36 | option_margin | 期权保证金 | ✓ 成功 | ✓ 成功 | 1 |

| 37 | option_hist_shfe | 上期所期权数据 | ✓ 成功 | ✓ 成功 | 270 |

| 38 | option_hist_dce | 大商所期权数据 | ✓ 成功 | ✓ 成功 | 0 |

| 39 | option_hist_czce | 郑商所期权数据 | ✓ 成功 | ✓ 成功 | 146 |

| 40 | option_hist_gfex | 广期所期权数据 | ✓ 成功 | ✓ 成功 | 1 |

| 41 | option_vol_gfex | 广期所隐含波动率 | ✓ 成功 | ✓ 成功 | 0 |

| 42 | option_czce_hist | 郑商所期权历史行情 | ✓ 成功 | ✓ 成功 | 1 |
