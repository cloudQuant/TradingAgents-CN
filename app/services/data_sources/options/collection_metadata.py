"""
期权数据集合元信息配置
定义所有期权数据集合的静态元信息，用于动态注册和前端展示
"""

OPTION_COLLECTION_METADATA = {
    # 01. openctp期权合约信息
    "option_contract_info_ctp": {
        "display_name": "openctp期权合约信息",
        "description": "openctp期权合约信息，包含交易所、合约、保证金、手续费等",
        "route": "/options/collections/option_contract_info_ctp",
        "order": 1,
    },
    # 02. 金融期权行情数据
    "option_finance_board": {
        "display_name": "金融期权行情数据",
        "description": "上海证券交易所、深圳证券交易所、中国金融期货交易所的金融期权行情数据",
        "route": "/options/collections/option_finance_board",
        "order": 2,
    },
    # 03. 上交所期权风险指标
    "option_risk_indicator_sse": {
        "display_name": "上交所期权风险指标",
        "description": "上海证券交易所-产品-股票期权-期权风险指标数据",
        "route": "/options/collections/option_risk_indicator_sse",
        "order": 3,
    },
    # 04. 上交所当日合约
    "option_current_day_sse": {
        "display_name": "上交所当日合约",
        "description": "上海证券交易所-产品-股票期权-信息披露-当日合约",
        "route": "/options/collections/option_current_day_sse",
        "order": 4,
    },
    # 05. 深交所当日合约
    "option_current_day_szse": {
        "display_name": "深交所当日合约",
        "description": "深圳证券交易所-期权子网-行情数据-当日合约",
        "route": "/options/collections/option_current_day_szse",
        "order": 5,
    },
    # 06. 上交所每日统计
    "option_daily_stats_sse": {
        "display_name": "上交所每日统计",
        "description": "上海证券交易所-产品-股票期权-每日统计",
        "route": "/options/collections/option_daily_stats_sse",
        "order": 6,
    },
    # 07. 深交所日度概况
    "option_daily_stats_szse": {
        "display_name": "深交所日度概况",
        "description": "深圳证券交易所-市场数据-期权数据-日度概况",
        "route": "/options/collections/option_daily_stats_szse",
        "order": 7,
    },
    # 08. 中金所上证50指数合约列表
    "option_cffex_sz50_list_sina": {
        "display_name": "中金所上证50指数合约列表",
        "description": "中金所上证50指数所有合约，返回的第一个合约为主力合约",
        "route": "/options/collections/option_cffex_sz50_list_sina",
        "order": 8,
    },
    # 09. 中金所沪深300指数合约列表
    "option_cffex_hs300_list_sina": {
        "display_name": "中金所沪深300指数合约列表",
        "description": "中金所沪深300指数所有合约，返回的第一个合约为主力合约",
        "route": "/options/collections/option_cffex_hs300_list_sina",
        "order": 9,
    },
    # 10. 中金所中证1000指数合约列表
    "option_cffex_zz1000_list_sina": {
        "display_name": "中金所中证1000指数合约列表",
        "description": "中金所中证1000指数所有合约，返回的第一个合约为主力合约",
        "route": "/options/collections/option_cffex_zz1000_list_sina",
        "order": 10,
    },
    # 11. 中金所上证50指数实时行情
    "option_cffex_sz50_spot_sina": {
        "display_name": "中金所上证50指数实时行情",
        "description": "新浪财经-中金所上证50指数指定合约实时行情",
        "route": "/options/collections/option_cffex_sz50_spot_sina",
        "order": 11,
    },
    # 12. 中金所沪深300指数实时行情
    "option_cffex_hs300_spot_sina": {
        "display_name": "中金所沪深300指数实时行情",
        "description": "新浪财经-中金所沪深300指数指定合约实时行情",
        "route": "/options/collections/option_cffex_hs300_spot_sina",
        "order": 12,
    },
    # 13. 中金所中证1000指数实时行情
    "option_cffex_zz1000_spot_sina": {
        "display_name": "中金所中证1000指数实时行情",
        "description": "新浪财经-中金所中证1000指数指定合约实时行情",
        "route": "/options/collections/option_cffex_zz1000_spot_sina",
        "order": 13,
    },
    # 14. 中金所上证50指数日频行情
    "option_cffex_sz50_daily_sina": {
        "display_name": "中金所上证50指数日频行情",
        "description": "中金所上证50指数指定合约日频行情",
        "route": "/options/collections/option_cffex_sz50_daily_sina",
        "order": 14,
    },
    # 15. 中金所沪深300指数日频行情
    "option_cffex_hs300_daily_sina": {
        "display_name": "中金所沪深300指数日频行情",
        "description": "中金所沪深300指数指定合约日频行情",
        "route": "/options/collections/option_cffex_hs300_daily_sina",
        "order": 15,
    },
    # 16. 中金所中证1000指数日频行情
    "option_cffex_zz1000_daily_sina": {
        "display_name": "中金所中证1000指数日频行情",
        "description": "中金所中证1000指数指定合约日频行情",
        "route": "/options/collections/option_cffex_zz1000_daily_sina",
        "order": 16,
    },
    # 17. 上交所50ETF合约到期月份列表
    "option_sse_list_sina": {
        "display_name": "上交所50ETF合约到期月份列表",
        "description": "获取期权上交所50ETF合约到期月份列表",
        "route": "/options/collections/option_sse_list_sina",
        "order": 17,
    },
    # 18. 剩余到期时间
    "option_sse_expire_day_sina": {
        "display_name": "剩余到期时间",
        "description": "获取指定到期月份指定品种的剩余到期时间",
        "route": "/options/collections/option_sse_expire_day_sina",
        "order": 18,
    },
    # 19. 看涨看跌合约代码
    "option_sse_codes_sina": {
        "display_name": "看涨看跌合约代码",
        "description": "新浪期权看涨看跌合约的代码",
        "route": "/options/collections/option_sse_codes_sina",
        "order": 19,
    },
    # 20. 期权实时数据
    "option_sse_spot_price_sina": {
        "display_name": "期权实时数据",
        "description": "期权实时数据",
        "route": "/options/collections/option_sse_spot_price_sina",
        "order": 20,
    },
    # 21. 期权标的物实时数据
    "option_sse_underlying_spot_price_sina": {
        "display_name": "期权标的物实时数据",
        "description": "获取期权标的物的实时数据",
        "route": "/options/collections/option_sse_underlying_spot_price_sina",
        "order": 21,
    },
    # 22. 期权希腊字母信息表
    "option_sse_greeks_sina": {
        "display_name": "期权希腊字母信息表",
        "description": "新浪财经-期权希腊字母信息表",
        "route": "/options/collections/option_sse_greeks_sina",
        "order": 22,
    },
    # 23. 期权分钟数据
    "option_sse_minute_sina": {
        "display_name": "期权分钟数据",
        "description": "期权行情分钟数据，只能返还当天的分钟数据",
        "route": "/options/collections/option_sse_minute_sina",
        "order": 23,
    },
    # 24. 期权日数据
    "option_sse_daily_sina": {
        "display_name": "期权日数据",
        "description": "期权行情日数据",
        "route": "/options/collections/option_sse_daily_sina",
        "order": 24,
    },
    # 25. 金融期权股票期权分时行情
    "option_finance_minute_sina": {
        "display_name": "金融期权股票期权分时行情",
        "description": "新浪财经-金融期权-股票期权-分时行情数据",
        "route": "/options/collections/option_finance_minute_sina",
        "order": 25,
    },
    # 26. 东财期权分时行情
    "option_minute_em": {
        "display_name": "东财期权分时行情",
        "description": "东方财富网-行情中心-期权市场-分时行情",
        "route": "/options/collections/option_minute_em",
        "order": 26,
    },
    # 27. 东财期权行情
    "option_current_em": {
        "display_name": "东财期权行情",
        "description": "东方财富网-行情中心-期权市场",
        "route": "/options/collections/option_current_em",
        "order": 27,
    },
    # 28. 期权龙虎榜
    "option_lhb_em": {
        "display_name": "期权龙虎榜",
        "description": "东方财富网-数据中心-期货期权-期权龙虎榜单-金融期权",
        "route": "/options/collections/option_lhb_em",
        "order": 28,
    },
    # 29. 期权价值分析
    "option_value_analysis_em": {
        "display_name": "期权价值分析",
        "description": "东方财富网-数据中心-特色数据-期权价值分析",
        "route": "/options/collections/option_value_analysis_em",
        "order": 29,
    },
    # 30. 期权风险分析
    "option_risk_analysis_em": {
        "display_name": "期权风险分析",
        "description": "东方财富网-数据中心-特色数据-期权风险分析",
        "route": "/options/collections/option_risk_analysis_em",
        "order": 30,
    },
    # 31. 期权折溢价
    "option_premium_analysis_em": {
        "display_name": "期权折溢价",
        "description": "东方财富网-数据中心-特色数据-期权折溢价",
        "route": "/options/collections/option_premium_analysis_em",
        "order": 31,
    },
    # 32. 商品期权当前合约
    "option_commodity_contract_sina": {
        "display_name": "商品期权当前合约",
        "description": "新浪财经-商品期权当前在交易的合约",
        "route": "/options/collections/option_commodity_contract_sina",
        "order": 32,
    },
    # 33. 商品期权T型报价表
    "option_commodity_contract_table_sina": {
        "display_name": "商品期权T型报价表",
        "description": "新浪财经-商品期权的T型报价表",
        "route": "/options/collections/option_commodity_contract_table_sina",
        "order": 33,
    },
    # 34. 商品期权历史行情
    "option_commodity_hist_sina": {
        "display_name": "商品期权历史行情",
        "description": "新浪财经-商品期权的历史行情数据-日频率",
        "route": "/options/collections/option_commodity_hist_sina",
        "order": 34,
    },
    # 35. 商品期权手续费
    "option_comm_info": {
        "display_name": "商品期权手续费",
        "description": "九期网-商品期权手续费数据",
        "route": "/options/collections/option_comm_info",
        "order": 35,
    },
    # 36. 期权保证金
    "option_margin": {
        "display_name": "期权保证金",
        "description": "唯爱期货-期权保证金",
        "route": "/options/collections/option_margin",
        "order": 36,
    },
    # 37. 上期所期权数据
    "option_hist_shfe": {
        "display_name": "上期所期权数据",
        "description": "上海期货交易所商品期权数据",
        "route": "/options/collections/option_hist_shfe",
        "order": 37,
    },
    # 38. 大商所期权数据
    "option_hist_dce": {
        "display_name": "大商所期权数据",
        "description": "大连商品交易所商品期权数据",
        "route": "/options/collections/option_hist_dce",
        "order": 38,
    },
    # 39. 郑商所期权数据
    "option_hist_czce": {
        "display_name": "郑商所期权数据",
        "description": "郑州商品交易所商品期权数据",
        "route": "/options/collections/option_hist_czce",
        "order": 39,
    },
    # 40. 广期所期权数据
    "option_hist_gfex": {
        "display_name": "广期所期权数据",
        "description": "广州期货交易所商品期权数据",
        "route": "/options/collections/option_hist_gfex",
        "order": 40,
    },
    # 41. 广期所隐含波动率
    "option_vol_gfex": {
        "display_name": "广期所隐含波动率",
        "description": "广州期货交易所商品期权数据-隐含波动参考值",
        "route": "/options/collections/option_vol_gfex",
        "order": 41,
    },
    # 42. 郑商所期权历史行情
    "option_czce_hist": {
        "display_name": "郑商所期权历史行情",
        "description": "郑州商品交易所的商品期权历史行情数据",
        "route": "/options/collections/option_czce_hist",
        "order": 42,
    },
}
