"""
期权数据集合更新参数配置
定义每个期权数据集合的更新参数、选项等配置
"""

OPTION_UPDATE_CONFIG = {
    # 01. openctp期权合约信息
    "option_contract_info_ctp": {
        "display_name": "openctp期权合约信息",
        "update_description": "一次性获取所有期权合约信息",
        "single_update": {"enabled": False},
        "batch_update": {"enabled": False},
    },
    # 02. 金融期权行情数据
    "option_finance_board": {
        "display_name": "金融期权行情数据",
        "update_description": "获取指定合约的金融期权行情数据",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "合约名称", "type": "select", "required": True,
                 "options": ["华泰柏瑞沪深300ETF期权", "华夏上证50ETF期权", "嘉实沪深300ETF期权"]},
                {"name": "end_month", "label": "到期月份", "type": "string", "required": True,
                 "placeholder": "如: 2412"},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 03. 上交所期权风险指标
    "option_risk_indicator_sse": {
        "display_name": "上交所期权风险指标",
        "update_description": "获取指定日期的期权风险指标",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "date", "label": "日期", "type": "date", "required": True},
            ],
        },
        "batch_update": {"enabled": True, "params": [
            {"name": "start_date", "label": "开始日期", "type": "date", "required": True},
            {"name": "end_date", "label": "结束日期", "type": "date", "required": True},
        ]},
    },
    # 04. 上交所当日合约
    "option_current_day_sse": {
        "display_name": "上交所当日合约",
        "update_description": "一次性获取所有当日合约",
        "single_update": {"enabled": False},
        "batch_update": {"enabled": False},
    },
    # 05. 深交所当日合约
    "option_current_day_szse": {
        "display_name": "深交所当日合约",
        "update_description": "一次性获取所有当日合约",
        "single_update": {"enabled": False},
        "batch_update": {"enabled": False},
    },
    # 06. 上交所每日统计
    "option_daily_stats_sse": {
        "display_name": "上交所每日统计",
        "update_description": "获取指定日期的每日统计",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "date", "label": "日期", "type": "date", "required": True},
            ],
        },
        "batch_update": {"enabled": True, "params": [
            {"name": "start_date", "label": "开始日期", "type": "date", "required": True},
            {"name": "end_date", "label": "结束日期", "type": "date", "required": True},
        ]},
    },
    # 07. 深交所日度概况
    "option_daily_stats_szse": {
        "display_name": "深交所日度概况",
        "update_description": "获取指定日期的日度概况",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "date", "label": "日期", "type": "date", "required": True},
            ],
        },
        "batch_update": {"enabled": True, "params": [
            {"name": "start_date", "label": "开始日期", "type": "date", "required": True},
            {"name": "end_date", "label": "结束日期", "type": "date", "required": True},
        ]},
    },
    # 08-10. 中金所合约列表
    "option_cffex_sz50_list_sina": {
        "display_name": "中金所上证50指数合约列表",
        "update_description": "一次性获取所有合约",
        "single_update": {"enabled": False},
        "batch_update": {"enabled": False},
    },
    "option_cffex_hs300_list_sina": {
        "display_name": "中金所沪深300指数合约列表",
        "update_description": "一次性获取所有合约",
        "single_update": {"enabled": False},
        "batch_update": {"enabled": False},
    },
    "option_cffex_zz1000_list_sina": {
        "display_name": "中金所中证1000指数合约列表",
        "update_description": "一次性获取所有合约",
        "single_update": {"enabled": False},
        "batch_update": {"enabled": False},
    },
    # 11-13. 中金所实时行情
    "option_cffex_sz50_spot_sina": {
        "display_name": "中金所上证50指数实时行情",
        "update_description": "获取指定合约的实时行情",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "合约代码", "type": "string", "required": True},
            ],
        },
        "batch_update": {"enabled": False},
    },
    "option_cffex_hs300_spot_sina": {
        "display_name": "中金所沪深300指数实时行情",
        "update_description": "获取指定合约的实时行情",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "合约代码", "type": "string", "required": True},
            ],
        },
        "batch_update": {"enabled": False},
    },
    "option_cffex_zz1000_spot_sina": {
        "display_name": "中金所中证1000指数实时行情",
        "update_description": "获取指定合约的实时行情",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "合约代码", "type": "string", "required": True},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 14-16. 中金所日频行情
    "option_cffex_sz50_daily_sina": {
        "display_name": "中金所上证50指数日频行情",
        "update_description": "获取指定合约的日频行情",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "合约代码", "type": "string", "required": True},
            ],
        },
        "batch_update": {"enabled": False},
    },
    "option_cffex_hs300_daily_sina": {
        "display_name": "中金所沪深300指数日频行情",
        "update_description": "获取指定合约的日频行情",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "合约代码", "type": "string", "required": True},
            ],
        },
        "batch_update": {"enabled": False},
    },
    "option_cffex_zz1000_daily_sina": {
        "display_name": "中金所中证1000指数日频行情",
        "update_description": "获取指定合约的日频行情",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "合约代码", "type": "string", "required": True},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 17. 上交所50ETF合约到期月份列表
    "option_sse_list_sina": {
        "display_name": "上交所50ETF合约到期月份列表",
        "update_description": "一次性获取所有到期月份",
        "single_update": {"enabled": False},
        "batch_update": {"enabled": False},
    },
    # 18. 剩余到期时间
    "option_sse_expire_day_sina": {
        "display_name": "剩余到期时间",
        "update_description": "获取指定月份品种的剩余到期时间",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "trade_date", "label": "到期月份", "type": "string", "required": True,
                 "placeholder": "如: 2412"},
                {"name": "symbol", "label": "品种", "type": "select", "required": True,
                 "options": ["50ETF", "300ETF", "500ETF", "创业板ETF", "科创50ETF"]},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 19. 看涨看跌合约代码
    "option_sse_codes_sina": {
        "display_name": "看涨看跌合约代码",
        "update_description": "获取指定月份品种的合约代码",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "trade_date", "label": "到期月份", "type": "string", "required": True},
                {"name": "underlying", "label": "品种", "type": "select", "required": True,
                 "options": ["50ETF", "300ETF", "500ETF"]},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 20. 期权实时数据
    "option_sse_spot_price_sina": {
        "display_name": "期权实时数据",
        "update_description": "获取指定合约的实时数据",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "合约代码", "type": "string", "required": True},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 21. 期权标的物实时数据
    "option_sse_underlying_spot_price_sina": {
        "display_name": "期权标的物实时数据",
        "update_description": "获取期权标的物的实时数据",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "品种", "type": "select", "required": True,
                 "options": ["50ETF", "300ETF", "500ETF"]},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 22. 期权希腊字母信息表
    "option_sse_greeks_sina": {
        "display_name": "期权希腊字母信息表",
        "update_description": "获取期权希腊字母信息",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "合约代码", "type": "string", "required": True},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 23. 期权分钟数据
    "option_sse_minute_sina": {
        "display_name": "期权分钟数据",
        "update_description": "获取期权分钟数据（当天）",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "合约代码", "type": "string", "required": True},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 24. 期权日数据
    "option_sse_daily_sina": {
        "display_name": "期权日数据",
        "update_description": "获取期权日数据",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "合约代码", "type": "string", "required": True},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 25. 金融期权股票期权分时行情
    "option_finance_minute_sina": {
        "display_name": "金融期权股票期权分时行情",
        "update_description": "获取金融期权分时行情",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "合约代码", "type": "string", "required": True},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 26. 东财期权分时行情
    "option_minute_em": {
        "display_name": "东财期权分时行情",
        "update_description": "获取期权分时行情",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "合约代码", "type": "string", "required": True},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 27. 东财期权行情
    "option_current_em": {
        "display_name": "东财期权行情",
        "update_description": "获取期权市场行情",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "品种", "type": "select", "required": True,
                 "options": ["华夏上证50ETF期权", "华泰柏瑞沪深300ETF期权", "嘉实沪深300ETF期权"]},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 28. 期权龙虎榜
    "option_lhb_em": {
        "display_name": "期权龙虎榜",
        "update_description": "获取期权龙虎榜数据",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "品种", "type": "select", "required": True,
                 "options": ["沪深300股指期权", "上证50股指期权", "中证1000股指期权"]},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 29. 期权价值分析
    "option_value_analysis_em": {
        "display_name": "期权价值分析",
        "update_description": "获取期权价值分析数据",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "品种", "type": "select", "required": True,
                 "options": ["沪深300股指期权", "上证50股指期权"]},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 30. 期权风险分析
    "option_risk_analysis_em": {
        "display_name": "期权风险分析",
        "update_description": "获取期权风险分析数据",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "品种", "type": "select", "required": True,
                 "options": ["沪深300股指期权", "上证50股指期权"]},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 31. 期权折溢价
    "option_premium_analysis_em": {
        "display_name": "期权折溢价",
        "update_description": "获取期权折溢价数据",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "品种", "type": "select", "required": True,
                 "options": ["沪深300股指期权", "上证50股指期权"]},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 32. 商品期权当前合约
    "option_commodity_contract_sina": {
        "display_name": "商品期权当前合约",
        "update_description": "获取商品期权当前在交易的合约",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "品种", "type": "select", "required": True,
                 "options": ["铜期权", "天然橡胶期权", "黄金期权", "豆粕期权", "玉米期权", "白糖期权", "棉花期权"]},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 33. 商品期权T型报价表
    "option_commodity_contract_table_sina": {
        "display_name": "商品期权T型报价表",
        "update_description": "获取商品期权T型报价表",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "品种", "type": "select", "required": True,
                 "options": ["铜期权", "天然橡胶期权", "黄金期权", "豆粕期权", "玉米期权", "白糖期权", "棉花期权"]},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 34. 商品期权历史行情
    "option_commodity_hist_sina": {
        "display_name": "商品期权历史行情",
        "update_description": "获取商品期权历史行情数据",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "合约代码", "type": "string", "required": True},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 35. 商品期权手续费
    "option_comm_info": {
        "display_name": "商品期权手续费",
        "update_description": "一次性获取所有商品期权手续费数据",
        "single_update": {"enabled": False},
        "batch_update": {"enabled": False},
    },
    # 36. 期权保证金
    "option_margin": {
        "display_name": "期权保证金",
        "update_description": "一次性获取所有期权保证金数据",
        "single_update": {"enabled": False},
        "batch_update": {"enabled": False},
    },
    # 37-40. 商品期权交易所数据
    "option_hist_shfe": {
        "display_name": "上期所期权数据",
        "update_description": "获取上海期货交易所商品期权数据",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "品种", "type": "select", "required": True,
                 "options": ["铜期权", "天然橡胶期权", "黄金期权", "锌期权", "铝期权"]},
                {"name": "date", "label": "日期", "type": "date", "required": True},
            ],
        },
        "batch_update": {"enabled": False},
    },
    "option_hist_dce": {
        "display_name": "大商所期权数据",
        "update_description": "获取大连商品交易所商品期权数据",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "品种", "type": "select", "required": True,
                 "options": ["豆粕期权", "玉米期权", "铁矿石期权", "聚乙烯期权", "棕榈油期权"]},
                {"name": "date", "label": "日期", "type": "date", "required": True},
            ],
        },
        "batch_update": {"enabled": False},
    },
    "option_hist_czce": {
        "display_name": "郑商所期权数据",
        "update_description": "获取郑州商品交易所商品期权数据",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "品种", "type": "select", "required": True,
                 "options": ["白糖期权", "棉花期权", "甲醇期权", "PTA期权", "菜籽粕期权"]},
                {"name": "date", "label": "日期", "type": "date", "required": True},
            ],
        },
        "batch_update": {"enabled": False},
    },
    "option_hist_gfex": {
        "display_name": "广期所期权数据",
        "update_description": "获取广州期货交易所商品期权数据",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "品种", "type": "select", "required": True,
                 "options": ["工业硅期权", "碳酸锂期权"]},
                {"name": "date", "label": "日期", "type": "date", "required": True},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 41. 广期所隐含波动率
    "option_vol_gfex": {
        "display_name": "广期所隐含波动率",
        "update_description": "获取广期所隐含波动率参考值",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "品种", "type": "select", "required": True,
                 "options": ["工业硅期权", "碳酸锂期权"]},
            ],
        },
        "batch_update": {"enabled": False},
    },
    # 42. 郑商所期权历史行情
    "option_czce_hist": {
        "display_name": "郑商所期权历史行情",
        "update_description": "获取郑州商品交易所期权历史行情数据",
        "single_update": {
            "enabled": True,
            "params": [
                {"name": "symbol", "label": "合约代码", "type": "string", "required": True},
            ],
        },
        "batch_update": {"enabled": False},
    },
}
