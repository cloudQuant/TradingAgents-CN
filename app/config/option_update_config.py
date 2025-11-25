"""
期权数据集合更新参数配置
定义每个集合的单条更新和批量更新的参数配置
"""

from typing import Dict, Any, List, Optional

# 无参数集合列表（一次性获取所有数据）
NO_PARAM_COLLECTIONS = [
    "option_contract_info_ctp", "option_current_day_sse", "option_current_day_szse",
    "option_cffex_sz50_list_sina", "option_cffex_hs300_list_sina", "option_cffex_zz1000_list_sina",
    "option_current_em", "option_lhb_em", "option_value_analysis_em",
    "option_risk_analysis_em", "option_premium_analysis_em", "option_comm_info", "option_margin",
    "option_vol_gfex"
]

# 需要日期参数的集合
DATE_PARAM_COLLECTIONS = [
    "option_risk_indicator_sse", "option_daily_stats_sse", "option_daily_stats_szse",
    "option_czce_hist"
]

# 需要品种参数的集合
SYMBOL_PARAM_COLLECTIONS = [
    "option_finance_board", "option_cffex_sz50_spot_sina", "option_cffex_hs300_spot_sina",
    "option_cffex_zz1000_spot_sina", "option_cffex_sz50_daily_sina", "option_cffex_hs300_daily_sina",
    "option_cffex_zz1000_daily_sina", "option_sse_list_sina", "option_sse_expire_day_sina",
    "option_sse_codes_sina", "option_sse_underlying_spot_price_sina", "option_sse_greeks_sina",
    "option_sse_minute_sina", "option_sse_daily_sina", "option_finance_minute_sina",
    "option_minute_em", "option_commodity_contract_sina", "option_commodity_contract_table_sina",
    "option_commodity_hist_sina"
]

# 需要品种+日期参数的集合
SYMBOL_DATE_PARAM_COLLECTIONS = [
    "option_hist_shfe", "option_hist_dce", "option_hist_czce", "option_hist_gfex"
]

# 期权集合更新配置
OPTION_UPDATE_CONFIGS: Dict[str, Dict[str, Any]] = {
    # ==================== 无参数集合 ====================
    "option_contract_info_ctp": {
        "display_name": "OpenCTP期权合约信息",
        "update_description": "获取OpenCTP期权合约信息",
        "single_update": {"enabled": False, "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有数据", "params": []}
    },
    "option_current_day_sse": {
        "display_name": "上交所当日合约",
        "update_description": "获取上交所股票期权当日合约信息",
        "single_update": {"enabled": False, "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有数据", "params": []}
    },
    "option_current_day_szse": {
        "display_name": "深交所当日合约",
        "update_description": "获取深交所期权当日合约信息",
        "single_update": {"enabled": False, "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有数据", "params": []}
    },
    "option_cffex_sz50_list_sina": {
        "display_name": "中金所上证50期权合约",
        "update_description": "获取中金所上证50指数期权合约",
        "single_update": {"enabled": False, "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有数据", "params": []}
    },
    "option_cffex_hs300_list_sina": {
        "display_name": "中金所沪深300期权合约",
        "update_description": "获取中金所沪深300指数期权合约",
        "single_update": {"enabled": False, "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有数据", "params": []}
    },
    "option_cffex_zz1000_list_sina": {
        "display_name": "中金所中证1000期权合约",
        "update_description": "获取中金所中证1000指数期权合约",
        "single_update": {"enabled": False, "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有数据", "params": []}
    },
    "option_current_em": {
        "display_name": "期权实时数据",
        "update_description": "获取东方财富期权实时行情",
        "single_update": {"enabled": False, "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有数据", "params": []}
    },
    "option_lhb_em": {
        "display_name": "期权龙虎榜",
        "update_description": "获取东方财富期权龙虎榜",
        "single_update": {
            "enabled": True, "description": "更新指定标的和指标",
            "params": [
                {"name": "symbol", "label": "标的代码", "type": "select", "required": True,
                 "options": [{"label": "510050", "value": "510050"}, {"label": "510300", "value": "510300"}, {"label": "159919", "value": "159919"}]},
                {"name": "indicator", "label": "指标", "type": "select", "required": True,
                 "options": [{"label": "认氽交易量", "value": "期权交易情况-认氽交易量"}, {"label": "认购交易量", "value": "期权交易情况-认购交易量"}, {"label": "认氽持仓量", "value": "期权持仓情况-认氽持仓量"}, {"label": "认购持仓量", "value": "期权持仓情况-认购持仓量"}]},
                {"name": "trade_date", "label": "交易日", "type": "text", "placeholder": "如 20220121", "required": True}
            ]
        },
        "batch_update": {"enabled": True, "description": "批量更新当日所有标的和指标", "params": [
            {"name": "trade_date", "label": "交易日", "type": "text", "placeholder": "如 20220121"}
        ]}
    },
    "option_value_analysis_em": {
        "display_name": "期权价值分析",
        "update_description": "获取东方财富期权价值分析",
        "single_update": {"enabled": False, "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有数据", "params": []}
    },
    "option_risk_analysis_em": {
        "display_name": "期权风险分析",
        "update_description": "获取东方财富期权风险分析",
        "single_update": {"enabled": False, "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有数据", "params": []}
    },
    "option_premium_analysis_em": {
        "display_name": "期权折溢价",
        "update_description": "获取东方财富期权折溢价分析",
        "single_update": {"enabled": False, "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有数据", "params": []}
    },
    "option_comm_info": {
        "display_name": "商品期权手续费",
        "update_description": "获取九期网商品期权手续费",
        "single_update": {"enabled": False, "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有数据", "params": []}
    },
    "option_margin": {
        "display_name": "期权保证金",
        "update_description": "获取唯爱期货期权保证金",
        "single_update": {"enabled": False, "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有数据", "params": []}
    },
    "option_vol_gfex": {
        "display_name": "广期所隐含波动率",
        "update_description": "获取广期所隐含波动率参考值",
        "single_update": {"enabled": False, "params": []},
        "batch_update": {"enabled": True, "description": "一次性获取所有数据", "params": []}
    },
    
    # ==================== 需要日期参数的集合 ====================
    "option_risk_indicator_sse": {
        "display_name": "期权风险指标",
        "update_description": "获取上交所期权风险指标",
        "single_update": {
            "enabled": True, "description": "更新指定日期",
            "params": [{"name": "date", "label": "日期", "type": "text", "placeholder": "如 20241125", "required": True}]
        },
        "batch_update": {"enabled": True, "description": "批量更新最近交易日", "params": []}
    },
    "option_daily_stats_sse": {
        "display_name": "上交所期权每日统计",
        "update_description": "获取上交所期权每日统计",
        "single_update": {
            "enabled": True, "description": "更新指定日期",
            "params": [{"name": "date", "label": "日期", "type": "text", "placeholder": "如 20241125", "required": True}]
        },
        "batch_update": {"enabled": True, "description": "批量更新最近交易日", "params": []}
    },
    "option_daily_stats_szse": {
        "display_name": "深交所期权每日统计",
        "update_description": "获取深交所期权每日统计",
        "single_update": {
            "enabled": True, "description": "更新指定日期",
            "params": [{"name": "date", "label": "日期", "type": "text", "placeholder": "如 20241125", "required": True}]
        },
        "batch_update": {"enabled": True, "description": "批量更新最近交易日", "params": []}
    },
    "option_czce_hist": {
        "display_name": "郑商所期权历史行情",
        "update_description": "获取郑商所期权历史行情（按年度获取）",
        "single_update": {
            "enabled": True, "description": "更新指定年份和品种",
            "params": [
                {"name": "year", "label": "年份", "type": "text", "placeholder": "如 2025", "required": True},
                {"name": "symbol", "label": "品种代码", "type": "select", "required": True,
                 "options": [{"label": "白糖(SR)", "value": "SR"}, {"label": "棉花(CF)", "value": "CF"}, {"label": "PTA(TA)", "value": "TA"}, {"label": "甲醇(MA)", "value": "MA"}, {"label": "菜籽粕(RM)", "value": "RM"}]}
            ]
        },
        "batch_update": {"enabled": True, "description": "批量更新当年主要品种", "params": []}
    },
    
    # ==================== 需要品种参数的集合 ====================
    "option_finance_board": {
        "display_name": "金融期权行情数据",
        "update_description": "获取金融期权行情数据",
        "single_update": {
            "enabled": True, "description": "更新指定品种和月份",
            "params": [
                {"name": "symbol", "label": "品种", "type": "select", "required": True,
                 "options": [{"label": "华夏上证50ETF期权", "value": "华夏上证50ETF期权"},
                            {"label": "沪深300股指期权", "value": "沪深300股指期权"}]},
                {"name": "end_month", "label": "到期月份", "type": "text", "placeholder": "如 2412", "required": True}
            ]
        },
        "batch_update": {"enabled": True, "description": "批量更新所有品种", "params": []}
    },
    "option_cffex_sz50_spot_sina": {
        "display_name": "中金所上证50指数实时行情",
        "update_description": "获取中金所上证50指数期权实时行情",
        "single_update": {
            "enabled": True, "description": "更新指定合约",
            "params": [{"name": "symbol", "label": "合约代码", "type": "text", "placeholder": "如 io2412", "required": True}]
        },
        "batch_update": {"enabled": True, "description": "批量更新所有合约", "params": []}
    },
    "option_cffex_hs300_spot_sina": {
        "display_name": "中金所沪深300指数实时行情",
        "update_description": "获取中金所沪深300指数期权实时行情",
        "single_update": {
            "enabled": True, "description": "更新指定合约",
            "params": [{"name": "symbol", "label": "合约代码", "type": "text", "placeholder": "如 io2412", "required": True}]
        },
        "batch_update": {"enabled": True, "description": "批量更新所有合约", "params": []}
    },
    "option_cffex_zz1000_spot_sina": {
        "display_name": "中金所中证1000指数实时行情",
        "update_description": "获取中金所中证1000指数期权实时行情",
        "single_update": {
            "enabled": True, "description": "更新指定合约",
            "params": [{"name": "symbol", "label": "合约代码", "type": "text", "placeholder": "如 mo2412", "required": True}]
        },
        "batch_update": {"enabled": True, "description": "批量更新所有合约", "params": []}
    },
    "option_cffex_sz50_daily_sina": {
        "display_name": "中金所上证50指数日频行情",
        "update_description": "获取中金所上证50指数期权日频行情",
        "single_update": {
            "enabled": True, "description": "更新指定合约",
            "params": [{"name": "symbol", "label": "合约代码", "type": "text", "placeholder": "如 io2412C4000", "required": True}]
        },
        "batch_update": {"enabled": True, "description": "批量更新所有合约", "params": []}
    },
    "option_cffex_hs300_daily_sina": {
        "display_name": "中金所沪深300指数日频行情",
        "update_description": "获取中金所沪深300指数期权日频行情",
        "single_update": {
            "enabled": True, "description": "更新指定合约",
            "params": [{"name": "symbol", "label": "合约代码", "type": "text", "placeholder": "如 io2412C4000", "required": True}]
        },
        "batch_update": {"enabled": True, "description": "批量更新所有合约", "params": []}
    },
    "option_cffex_zz1000_daily_sina": {
        "display_name": "中金所中证1000指数日频行情",
        "update_description": "获取中金所中证1000指数期权日频行情",
        "single_update": {
            "enabled": True, "description": "更新指定合约",
            "params": [{"name": "symbol", "label": "合约代码", "type": "text", "placeholder": "如 mo2412C6000", "required": True}]
        },
        "batch_update": {"enabled": True, "description": "批量更新所有合约", "params": []}
    },
    "option_sse_list_sina": {
        "display_name": "上交所ETF合约到期月份",
        "update_description": "获取上交所ETF期权合约到期月份",
        "single_update": {
            "enabled": True, "description": "更新指定品种",
            "params": [{"name": "symbol", "label": "品种", "type": "select", "required": True,
                       "options": [{"label": "50ETF", "value": "50ETF"}, {"label": "300ETF", "value": "300ETF"}]}]
        },
        "batch_update": {"enabled": True, "description": "批量更新所有品种", "params": []}
    },
    "option_sse_expire_day_sina": {
        "display_name": "上交所ETF剩余到期时间",
        "update_description": "获取指定到期月份的剩余到期时间",
        "single_update": {
            "enabled": True, "description": "更新指定品种和月份",
            "params": [
                {"name": "symbol", "label": "品种", "type": "select", "required": True,
                 "options": [{"label": "50ETF", "value": "50ETF"}, {"label": "300ETF", "value": "300ETF"}]},
                {"name": "expire_month", "label": "到期月份", "type": "text", "placeholder": "如 2412", "required": True}
            ]
        },
        "batch_update": {"enabled": True, "description": "批量更新所有", "params": []}
    },
    "option_sse_codes_sina": {
        "display_name": "新浪期权合约代码",
        "update_description": "获取新浪期权看涨看跌合约代码",
        "single_update": {
            "enabled": True, "description": "更新指定条件",
            "params": [
                {"name": "symbol", "label": "品种", "type": "select", "required": True,
                 "options": [{"label": "50ETF", "value": "50ETF"}, {"label": "300ETF", "value": "300ETF"}]},
                {"name": "expire_month", "label": "到期月份", "type": "text", "placeholder": "如 2412", "required": True},
                {"name": "call_put", "label": "看涨/看跌", "type": "select", "required": True,
                 "options": [{"label": "看涨", "value": "购"}, {"label": "看跌", "value": "沽"}]}
            ]
        },
        "batch_update": {"enabled": True, "description": "批量更新", "params": []}
    },
    "option_sse_underlying_spot_price_sina": {
        "display_name": "期权标的物实时数据",
        "update_description": "获取期权标的物实时数据",
        "single_update": {
            "enabled": True, "description": "更新指定品种",
            "params": [{"name": "symbol", "label": "品种", "type": "select", "required": True,
                       "options": [{"label": "50ETF", "value": "50ETF"}, {"label": "300ETF", "value": "300ETF"}]}]
        },
        "batch_update": {"enabled": True, "description": "批量更新", "params": []}
    },
    "option_sse_greeks_sina": {
        "display_name": "期权希腊字母",
        "update_description": "获取新浪期权希腊字母",
        "single_update": {
            "enabled": True, "description": "更新指定合约",
            "params": [{"name": "symbol", "label": "合约代码", "type": "text", "placeholder": "如 10007313", "required": True}]
        },
        "batch_update": {"enabled": True, "description": "批量更新", "params": []}
    },
    "option_sse_minute_sina": {
        "display_name": "期权分钟行情",
        "update_description": "获取期权分钟行情（仅当天）",
        "single_update": {
            "enabled": True, "description": "更新指定合约",
            "params": [{"name": "symbol", "label": "合约代码", "type": "text", "placeholder": "如 10007313", "required": True}]
        },
        "batch_update": {"enabled": True, "description": "批量更新", "params": []}
    },
    "option_sse_daily_sina": {
        "display_name": "期权日行情",
        "update_description": "获取期权日行情",
        "single_update": {
            "enabled": True, "description": "更新指定合约",
            "params": [{"name": "symbol", "label": "合约代码", "type": "text", "placeholder": "如 10007313", "required": True}]
        },
        "batch_update": {"enabled": True, "description": "批量更新", "params": []}
    },
    "option_finance_minute_sina": {
        "display_name": "新浪期权分时行情",
        "update_description": "获取新浪金融期权分时行情",
        "single_update": {
            "enabled": True, "description": "更新指定合约",
            "params": [{"name": "symbol", "label": "合约代码", "type": "text", "placeholder": "如 mo2412C6000", "required": True}]
        },
        "batch_update": {"enabled": True, "description": "批量更新", "params": []}
    },
    "option_minute_em": {
        "display_name": "东财期权分时行情",
        "update_description": "获取东方财富期权分时行情",
        "single_update": {
            "enabled": True, "description": "更新指定合约",
            "params": [{"name": "symbol", "label": "合约代码", "type": "text", "placeholder": "期权合约代码", "required": True}]
        },
        "batch_update": {"enabled": True, "description": "批量更新", "params": []}
    },
    "option_commodity_contract_sina": {
        "display_name": "商品期权在交易合约",
        "update_description": "获取新浪商品期权在交易合约",
        "single_update": {
            "enabled": True, "description": "更新指定品种",
            "params": [{"name": "symbol", "label": "品种代码", "type": "text", "placeholder": "如 豆粕期权", "required": True}]
        },
        "batch_update": {"enabled": True, "description": "批量更新", "params": []}
    },
    "option_commodity_contract_table_sina": {
        "display_name": "商品期权T型报价表",
        "update_description": "获取新浪商品期权T型报价表",
        "single_update": {
            "enabled": True, "description": "更新指定条件",
            "params": [
                {"name": "symbol", "label": "品种代码", "type": "text", "placeholder": "如 豆粕期权", "required": True},
                {"name": "contract", "label": "合约月份", "type": "text", "placeholder": "如 m2501", "required": True}
            ]
        },
        "batch_update": {"enabled": True, "description": "批量更新", "params": []}
    },
    "option_commodity_hist_sina": {
        "display_name": "商品期权历史行情",
        "update_description": "获取新浪商品期权历史行情",
        "single_update": {
            "enabled": True, "description": "更新指定合约",
            "params": [{"name": "symbol", "label": "合约代码", "type": "text", "placeholder": "如 m2501C2700", "required": True}]
        },
        "batch_update": {"enabled": True, "description": "批量更新", "params": []}
    },
    
    # ==================== 需要品种+日期参数的集合 ====================
    "option_hist_shfe": {
        "display_name": "上期所商品期权",
        "update_description": "获取上期所商品期权数据",
        "single_update": {
            "enabled": True, "description": "更新指定条件",
            "params": [
                {"name": "symbol", "label": "品种代码", "type": "text", "placeholder": "如 cu", "required": True},
                {"name": "date", "label": "日期", "type": "text", "placeholder": "如 20241125", "required": True}
            ]
        },
        "batch_update": {"enabled": True, "description": "批量更新", "params": []}
    },
    "option_hist_dce": {
        "display_name": "大商所商品期权",
        "update_description": "获取大商所商品期权数据",
        "single_update": {
            "enabled": True, "description": "更新指定条件",
            "params": [
                {"name": "symbol", "label": "品种代码", "type": "text", "placeholder": "如 m", "required": True},
                {"name": "date", "label": "日期", "type": "text", "placeholder": "如 20241125", "required": True}
            ]
        },
        "batch_update": {"enabled": True, "description": "批量更新", "params": []}
    },
    "option_hist_czce": {
        "display_name": "郑商所商品期权",
        "update_description": "获取郑商所商品期权数据",
        "single_update": {
            "enabled": True, "description": "更新指定条件",
            "params": [
                {"name": "symbol", "label": "品种代码", "type": "text", "placeholder": "如 SR", "required": True},
                {"name": "date", "label": "日期", "type": "text", "placeholder": "如 20241125", "required": True}
            ]
        },
        "batch_update": {"enabled": True, "description": "批量更新", "params": []}
    },
    "option_hist_gfex": {
        "display_name": "广期所商品期权",
        "update_description": "获取广期所商品期权数据",
        "single_update": {
            "enabled": True, "description": "更新指定条件",
            "params": [
                {"name": "symbol", "label": "品种代码", "type": "text", "placeholder": "如 si", "required": True},
                {"name": "date", "label": "日期", "type": "text", "placeholder": "如 20241125", "required": True}
            ]
        },
        "batch_update": {"enabled": True, "description": "批量更新", "params": []}
    },
}


def get_collection_config(collection_name: str) -> Optional[Dict[str, Any]]:
    """获取指定集合的配置"""
    return OPTION_UPDATE_CONFIGS.get(collection_name)


def get_all_collection_names() -> List[str]:
    """获取所有集合名称"""
    return list(OPTION_UPDATE_CONFIGS.keys())
