"""
股票集合静态元信息
由于股票数据集合数量庞大（380+），采用动态生成元信息的方式
"""

from typing import Dict, Any


def _snake_to_display_name(name: str) -> str:
    """将下划线命名转换为显示名称"""
    # 常见后缀映射
    suffix_map = {
        '_em': '-东财',
        '_sina': '-新浪',
        '_ths': '-同花顺',
        '_xq': '-雪球',
        '_lg': '-乐咕',
        '_cninfo': '-巨潮',
        '_baidu': '-百度',
    }
    
    display = name
    for suffix, label in suffix_map.items():
        if display.endswith(suffix):
            display = display[:-len(suffix)] + label
            break
    
    # 常见前缀映射
    prefix_map = {
        'stock_zh_a_': 'A股',
        'stock_zh_b_': 'B股',
        'stock_hk_': '港股',
        'stock_us_': '美股',
        'stock_': '股票',
    }
    
    for prefix, label in prefix_map.items():
        if display.startswith(prefix):
            display = label + display[len(prefix):]
            break
    
    return display.replace('_', ' ').title()


# 核心股票集合元信息（手动维护的重要集合）
STOCK_COLLECTION_METADATA: Dict[str, Dict[str, Any]] = {
    # ==================== 实时行情类 ====================
    'stock_zh_a_spot_em': {
        'display_name': '沪深京A股实时行情-东财',
        'description': '东方财富网-沪深京A股-实时行情数据，包含最新价、涨跌幅、成交量等',
        'route': '/stocks/collections/stock_zh_a_spot_em',
        'order': 1,
    },
    'stock_sh_a_spot_em': {
        'display_name': '沪A股实时行情-东财',
        'description': '东方财富网-上海A股-实时行情数据',
        'route': '/stocks/collections/stock_sh_a_spot_em',
        'order': 2,
    },
    'stock_sz_a_spot_em': {
        'display_name': '深A股实时行情-东财',
        'description': '东方财富网-深圳A股-实时行情数据',
        'route': '/stocks/collections/stock_sz_a_spot_em',
        'order': 3,
    },
    'stock_bj_a_spot_em': {
        'display_name': '北交所A股实时行情-东财',
        'description': '东方财富网-北交所A股-实时行情数据',
        'route': '/stocks/collections/stock_bj_a_spot_em',
        'order': 4,
    },
    'stock_kc_a_spot_em': {
        'display_name': '科创板实时行情-东财',
        'description': '东方财富网-科创板-实时行情数据',
        'route': '/stocks/collections/stock_kc_a_spot_em',
        'order': 5,
    },
    'stock_cy_a_spot_em': {
        'display_name': '创业板实时行情-东财',
        'description': '东方财富网-创业板-实时行情数据',
        'route': '/stocks/collections/stock_cy_a_spot_em',
        'order': 6,
    },
    'stock_new_a_spot_em': {
        'display_name': '新股实时行情-东财',
        'description': '东方财富网-新股-实时行情数据',
        'route': '/stocks/collections/stock_new_a_spot_em',
        'order': 7,
    },
    'stock_hk_spot_em': {
        'display_name': '港股实时行情-东财',
        'description': '东方财富网-港股-实时行情数据',
        'route': '/stocks/collections/stock_hk_spot_em',
        'order': 8,
    },
    'stock_us_spot_em': {
        'display_name': '美股实时行情-东财',
        'description': '东方财富网-美股-实时行情数据',
        'route': '/stocks/collections/stock_us_spot_em',
        'order': 9,
    },
    
    # ==================== 个股信息类 ====================
    'stock_individual_info_em': {
        'display_name': '个股信息查询-东财',
        'description': '东方财富网-个股-股票信息，包含总股本、流通股、总市值等',
        'route': '/stocks/collections/stock_individual_info_em',
        'order': 10,
    },
    'stock_individual_basic_info_xq': {
        'display_name': '个股信息查询-雪球',
        'description': '雪球-个股-基本信息',
        'route': '/stocks/collections/stock_individual_basic_info_xq',
        'order': 11,
    },
    
    # ==================== 历史行情类 ====================
    'stock_zh_a_hist': {
        'display_name': 'A股历史行情',
        'description': '东方财富网-A股历史行情数据，支持日/周/月K线',
        'route': '/stocks/collections/stock_zh_a_hist',
        'order': 20,
    },
    'stock_zh_a_hist_min_em': {
        'display_name': 'A股分时行情-东财',
        'description': '东方财富网-A股分时行情数据',
        'route': '/stocks/collections/stock_zh_a_hist_min_em',
        'order': 21,
    },
    'stock_hk_hist': {
        'display_name': '港股历史行情',
        'description': '东方财富网-港股历史行情数据',
        'route': '/stocks/collections/stock_hk_hist',
        'order': 22,
    },
    'stock_us_hist': {
        'display_name': '美股历史行情',
        'description': '东方财富网-美股历史行情数据',
        'route': '/stocks/collections/stock_us_hist',
        'order': 23,
    },
    
    # ==================== 板块行情类 ====================
    'stock_board_industry_name_em': {
        'display_name': '行业板块列表-东财',
        'description': '东方财富网-行业板块名称列表',
        'route': '/stocks/collections/stock_board_industry_name_em',
        'order': 30,
    },
    'stock_board_concept_name_em': {
        'display_name': '概念板块列表-东财',
        'description': '东方财富网-概念板块名称列表',
        'route': '/stocks/collections/stock_board_concept_name_em',
        'order': 31,
    },
    'stock_board_industry_cons_em': {
        'display_name': '行业板块成分股-东财',
        'description': '东方财富网-行业板块成分股',
        'route': '/stocks/collections/stock_board_industry_cons_em',
        'order': 32,
    },
    'stock_board_concept_cons_em': {
        'display_name': '概念板块成分股-东财',
        'description': '东方财富网-概念板块成分股',
        'route': '/stocks/collections/stock_board_concept_cons_em',
        'order': 33,
    },
    
    # ==================== 涨停跌停类 ====================
    'stock_zt_pool_em': {
        'display_name': '涨停股池-东财',
        'description': '东方财富网-涨停股池',
        'route': '/stocks/collections/stock_zt_pool_em',
        'order': 40,
    },
    'stock_zt_pool_previous_em': {
        'display_name': '昨日涨停股池-东财',
        'description': '东方财富网-昨日涨停股池',
        'route': '/stocks/collections/stock_zt_pool_previous_em',
        'order': 41,
    },
    'stock_zt_pool_strong_em': {
        'display_name': '强势股池-东财',
        'description': '东方财富网-强势股池',
        'route': '/stocks/collections/stock_zt_pool_strong_em',
        'order': 42,
    },
    'stock_zt_pool_sub_new_em': {
        'display_name': '次新股池-东财',
        'description': '东方财富网-次新股池',
        'route': '/stocks/collections/stock_zt_pool_sub_new_em',
        'order': 43,
    },
    
    # ==================== 资金流向类 ====================
    'stock_individual_fund_flow': {
        'display_name': '个股资金流',
        'description': '个股资金流向数据',
        'route': '/stocks/collections/stock_individual_fund_flow',
        'order': 50,
    },
    'stock_market_fund_flow': {
        'display_name': '大盘资金流',
        'description': '大盘资金流向数据',
        'route': '/stocks/collections/stock_market_fund_flow',
        'order': 51,
    },
    'stock_sector_fund_flow_rank': {
        'display_name': '板块资金流排名',
        'description': '板块资金流向排名数据',
        'route': '/stocks/collections/stock_sector_fund_flow_rank',
        'order': 52,
    },
    
    # ==================== 龙虎榜类 ====================
    'stock_lhb_detail_em': {
        'display_name': '龙虎榜详情-东财',
        'description': '东方财富网-龙虎榜详情数据',
        'route': '/stocks/collections/stock_lhb_detail_em',
        'order': 60,
    },
    'stock_lhb_stock_statistic_em': {
        'display_name': '个股上榜统计-东财',
        'description': '东方财富网-龙虎榜-个股上榜统计',
        'route': '/stocks/collections/stock_lhb_stock_statistic_em',
        'order': 61,
    },
    
    # ==================== 沪深港通类 ====================
    'stock_hsgt_fund_flow_summary_em': {
        'display_name': '沪深港通资金流向-东财',
        'description': '东方财富网-沪深港通资金流向汇总',
        'route': '/stocks/collections/stock_hsgt_fund_flow_summary_em',
        'order': 70,
    },
    'stock_hsgt_board_rank_em': {
        'display_name': '沪深港通板块排行-东财',
        'description': '东方财富网-沪深港通-板块排行',
        'route': '/stocks/collections/stock_hsgt_board_rank_em',
        'order': 71,
    },
    'stock_hsgt_hold_stock_em': {
        'display_name': '沪深港通持股-东财',
        'description': '东方财富网-沪深港通-持股数据',
        'route': '/stocks/collections/stock_hsgt_hold_stock_em',
        'order': 72,
    },
    
    # ==================== 财务数据类 ====================
    'stock_financial_analysis_indicator_em': {
        'display_name': '财务指标-东财',
        'description': '东方财富网-财务分析指标数据',
        'route': '/stocks/collections/stock_financial_analysis_indicator_em',
        'order': 80,
    },
    'stock_balance_sheet_by_report_em': {
        'display_name': '资产负债表-东财',
        'description': '东方财富网-资产负债表数据',
        'route': '/stocks/collections/stock_balance_sheet_by_report_em',
        'order': 81,
    },
    'stock_profit_sheet_by_report_em': {
        'display_name': '利润表-东财',
        'description': '东方财富网-利润表数据',
        'route': '/stocks/collections/stock_profit_sheet_by_report_em',
        'order': 82,
    },
    'stock_cash_flow_sheet_by_report_em': {
        'display_name': '现金流量表-东财',
        'description': '东方财富网-现金流量表数据',
        'route': '/stocks/collections/stock_cash_flow_sheet_by_report_em',
        'order': 83,
    },
    
    # ==================== 股东信息类 ====================
    'stock_gdfx_top_10_em': {
        'display_name': '十大股东-东财',
        'description': '东方财富网-十大股东数据',
        'route': '/stocks/collections/stock_gdfx_top_10_em',
        'order': 90,
    },
    'stock_gdfx_free_top_10_em': {
        'display_name': '十大流通股东-东财',
        'description': '东方财富网-十大流通股东数据',
        'route': '/stocks/collections/stock_gdfx_free_top_10_em',
        'order': 91,
    },
    
    # ==================== 业绩数据类 ====================
    'stock_yjbb_em': {
        'display_name': '业绩报表-东财',
        'description': '东方财富网-业绩报表数据',
        'route': '/stocks/collections/stock_yjbb_em',
        'order': 100,
    },
    'stock_yjkb_em': {
        'display_name': '业绩快报-东财',
        'description': '东方财富网-业绩快报数据',
        'route': '/stocks/collections/stock_yjkb_em',
        'order': 101,
    },
    'stock_yjyg_em': {
        'display_name': '业绩预告-东财',
        'description': '东方财富网-业绩预告数据',
        'route': '/stocks/collections/stock_yjyg_em',
        'order': 102,
    },
    
    # ==================== 热门排行类 ====================
    'stock_hot_rank_em': {
        'display_name': '人气榜-东财',
        'description': '东方财富网-人气排行榜',
        'route': '/stocks/collections/stock_hot_rank_em',
        'order': 110,
    },
    'stock_hot_up_em': {
        'display_name': '飙升榜-东财',
        'description': '东方财富网-飙升排行榜',
        'route': '/stocks/collections/stock_hot_up_em',
        'order': 111,
    },
    'stock_comment_em': {
        'display_name': '千股千评-东财',
        'description': '东方财富网-千股千评数据',
        'route': '/stocks/collections/stock_comment_em',
        'order': 112,
    },
    
    # ==================== 股票列表类 ====================
    'stock_info_a_code_name': {
        'display_name': 'A股股票列表',
        'description': 'A股股票代码和名称列表',
        'route': '/stocks/collections/stock_info_a_code_name',
        'order': 120,
    },
    'stock_info_sh_name_code': {
        'display_name': '上证股票列表',
        'description': '上证股票代码和名称列表',
        'route': '/stocks/collections/stock_info_sh_name_code',
        'order': 121,
    },
    'stock_info_sz_name_code': {
        'display_name': '深证股票列表',
        'description': '深证股票代码和名称列表',
        'route': '/stocks/collections/stock_info_sz_name_code',
        'order': 122,
    },
    'stock_info_bj_name_code': {
        'display_name': '北证股票列表',
        'description': '北证股票代码和名称列表',
        'route': '/stocks/collections/stock_info_bj_name_code',
        'order': 123,
    },
}


def get_collection_metadata(collection_name: str) -> Dict[str, Any]:
    """
    获取集合的元信息
    
    如果在STOCK_COLLECTION_METADATA中有定义，则返回定义的元信息
    否则返回基于集合名称自动生成的元信息
    """
    if collection_name in STOCK_COLLECTION_METADATA:
        return STOCK_COLLECTION_METADATA[collection_name].copy()
    
    # 自动生成元信息
    return {
        'display_name': _snake_to_display_name(collection_name),
        'description': f'{collection_name} 数据集合',
        'route': f'/stocks/collections/{collection_name}',
        'order': 1000,  # 未定义的集合放在最后
    }


def get_all_collection_metadata() -> Dict[str, Dict[str, Any]]:
    """获取所有已定义的集合元信息"""
    return STOCK_COLLECTION_METADATA.copy()
