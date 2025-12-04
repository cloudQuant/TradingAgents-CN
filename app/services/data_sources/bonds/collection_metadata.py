"""
债券数据集合元信息配置

定义每个集合的显示名称、描述、路由等元信息
包含34个债券数据集合
"""

from typing import Dict, Any


# 债券集合元信息（34个集合）
BOND_COLLECTION_METADATA: Dict[str, Dict[str, Any]] = {
    # ==================== 01-02 基础数据 ====================
    "bond_info_cm": {
        "display_name": "债券查询-中国外汇交易中心",
        "description": "中国外汇交易中心债券信息查询，支持按债券名称、代码、发行人、债券类型、付息方式、发行年份、承销商、评级等条件查询",
        "route": "/bonds/collections/bond_info_cm",
        "order": 1,
        "source": "中国外汇交易中心",
        "category": "基础数据",
    },
    "bond_info_detail_cm": {
        "display_name": "债券基础信息-中国外汇交易中心",
        "description": "债券详细信息，包括发行条款、评级等详细数据",
        "route": "/bonds/collections/bond_info_detail_cm",
        "order": 2,
        "source": "中国外汇交易中心",
        "category": "基础数据",
    },
    
    # ==================== 03-04 沪深债券行情 ====================
    "bond_zh_hs_spot": {
        "display_name": "沪深债券实时行情",
        "description": "沪深债券实时行情数据，包括最新价、涨跌幅、成交量等",
        "route": "/bonds/collections/bond_zh_hs_spot",
        "order": 3,
        "source": "新浪财经",
        "category": "沪深债券行情",
    },
    "bond_zh_hs_daily": {
        "display_name": "沪深债券历史行情",
        "description": "沪深债券历史行情数据（日线），支持按日期查询",
        "route": "/bonds/collections/bond_zh_hs_daily",
        "order": 4,
        "source": "新浪财经",
        "category": "沪深债券行情",
    },
    
    # ==================== 05-07 可转债行情 ====================
    "bond_zh_hs_cov_spot": {
        "display_name": "可转债实时行情-沪深",
        "description": "沪深可转债实时行情数据",
        "route": "/bonds/collections/bond_zh_hs_cov_spot",
        "order": 5,
        "source": "新浪财经",
        "category": "可转债行情",
    },
    "bond_zh_hs_cov_daily": {
        "display_name": "可转债历史行情-日频",
        "description": "沪深可转债历史行情数据（日线）",
        "route": "/bonds/collections/bond_zh_hs_cov_daily",
        "order": 6,
        "source": "新浪财经",
        "category": "可转债行情",
    },
    "bond_zh_cov": {
        "display_name": "可转债数据一览表-东财",
        "description": "可转债综合数据，包括申购、转股价、溢价率等",
        "route": "/bonds/collections/bond_zh_cov",
        "order": 7,
        "source": "东方财富网",
        "category": "可转债行情",
    },
    
    # ==================== 08-09 市场概览 ====================
    "bond_cash_summary_sse": {
        "display_name": "债券现券市场概览-上交所",
        "description": "上交所债券现券市场托管概览",
        "route": "/bonds/collections/bond_cash_summary_sse",
        "order": 8,
        "source": "上海证券交易所",
        "category": "市场概览",
    },
    "bond_deal_summary_sse": {
        "display_name": "债券成交概览-上交所",
        "description": "上交所债券成交概览",
        "route": "/bonds/collections/bond_deal_summary_sse",
        "order": 9,
        "source": "上海证券交易所",
        "category": "市场概览",
    },
    
    # ==================== 10-12 银行间市场 ====================
    "bond_debt_nafmii": {
        "display_name": "银行间市场债券发行数据",
        "description": "银行间市场债券发行基础数据",
        "route": "/bonds/collections/bond_debt_nafmii",
        "order": 10,
        "source": "中国银行间市场交易商协会",
        "category": "银行间市场",
    },
    "bond_spot_quote": {
        "display_name": "现券市场做市报价",
        "description": "银行间现券市场做市报价",
        "route": "/bonds/collections/bond_spot_quote",
        "order": 11,
        "source": "中国外汇交易中心",
        "category": "银行间市场",
    },
    "bond_spot_deal": {
        "display_name": "现券市场成交行情",
        "description": "银行间现券市场成交行情",
        "route": "/bonds/collections/bond_spot_deal",
        "order": 12,
        "source": "中国外汇交易中心",
        "category": "银行间市场",
    },
    
    # ==================== 13-14 可转债分时 ====================
    "bond_zh_hs_cov_min": {
        "display_name": "可转债分时行情",
        "description": "可转债分时行情数据，支持1分钟、5分钟、15分钟、30分钟、60分钟周期",
        "route": "/bonds/collections/bond_zh_hs_cov_min",
        "order": 13,
        "source": "东方财富网",
        "category": "可转债分时",
    },
    "bond_zh_hs_cov_pre_min": {
        "display_name": "可转债盘前分时",
        "description": "可转债盘前分时数据",
        "route": "/bonds/collections/bond_zh_hs_cov_pre_min",
        "order": 14,
        "source": "东方财富网",
        "category": "可转债分时",
    },
    
    # ==================== 15-18 可转债详细 ====================
    "bond_zh_cov_info": {
        "display_name": "可转债详情-东财",
        "description": "可转债详情（基本信息、中签号、筹资用途、重要日期）",
        "route": "/bonds/collections/bond_zh_cov_info",
        "order": 15,
        "source": "东方财富网",
        "category": "可转债详细",
    },
    "bond_zh_cov_info_ths": {
        "display_name": "可转债详情-同花顺",
        "description": "可转债详情（同花顺数据源）",
        "route": "/bonds/collections/bond_zh_cov_info_ths",
        "order": 16,
        "source": "同花顺",
        "category": "可转债详细",
    },
    "bond_cov_comparison": {
        "display_name": "可转债比价表",
        "description": "可转债与正股比价数据",
        "route": "/bonds/collections/bond_cov_comparison",
        "order": 17,
        "source": "东方财富网",
        "category": "可转债详细",
    },
    "bond_zh_cov_value_analysis": {
        "display_name": "可转债价值分析",
        "description": "可转债价值分析（纯债价值、转股价值、溢价率）历史数据",
        "route": "/bonds/collections/bond_zh_cov_value_analysis",
        "order": 18,
        "source": "东方财富网",
        "category": "可转债详细",
    },
    
    # ==================== 19-21 质押式回购 ====================
    "bond_sh_buy_back_em": {
        "display_name": "上证质押式回购",
        "description": "上证质押式回购实时行情",
        "route": "/bonds/collections/bond_sh_buy_back_em",
        "order": 19,
        "source": "东方财富网",
        "category": "质押式回购",
    },
    "bond_sz_buy_back_em": {
        "display_name": "深证质押式回购",
        "description": "深证质押式回购实时行情",
        "route": "/bonds/collections/bond_sz_buy_back_em",
        "order": 20,
        "source": "东方财富网",
        "category": "质押式回购",
    },
    "bond_buy_back_hist_em": {
        "display_name": "质押式回购历史数据",
        "description": "质押式回购历史行情数据",
        "route": "/bonds/collections/bond_buy_back_hist_em",
        "order": 21,
        "source": "东方财富网",
        "category": "质押式回购",
    },
    
    # ==================== 22-25 集思录数据 ====================
    "bond_cb_jsl": {
        "display_name": "可转债实时数据-集思录",
        "description": "集思录可转债实时数据",
        "route": "/bonds/collections/bond_cb_jsl",
        "order": 22,
        "source": "集思录",
        "category": "集思录数据",
    },
    "bond_cb_redeem_jsl": {
        "display_name": "可转债强赎-集思录",
        "description": "可转债强赎信息",
        "route": "/bonds/collections/bond_cb_redeem_jsl",
        "order": 23,
        "source": "集思录",
        "category": "集思录数据",
    },
    "bond_cb_index_jsl": {
        "display_name": "可转债等权指数-集思录",
        "description": "集思录可转债等权指数历史数据",
        "route": "/bonds/collections/bond_cb_index_jsl",
        "order": 24,
        "source": "集思录",
        "category": "集思录数据",
    },
    "bond_cb_adj_logs_jsl": {
        "display_name": "转股价调整记录-集思录",
        "description": "可转债转股价调整记录",
        "route": "/bonds/collections/bond_cb_adj_logs_jsl",
        "order": 25,
        "source": "集思录",
        "category": "集思录数据",
    },
    
    # ==================== 26-27 收益率曲线 ====================
    "bond_china_close_return": {
        "display_name": "收益率曲线历史数据",
        "description": "中国债券收益率曲线历史数据",
        "route": "/bonds/collections/bond_china_close_return",
        "order": 26,
        "source": "中国外汇交易中心",
        "category": "收益率曲线",
    },
    "bond_zh_us_rate": {
        "display_name": "中美国债收益率",
        "description": "中美国债收益率对比数据",
        "route": "/bonds/collections/bond_zh_us_rate",
        "order": 27,
        "source": "东方财富网",
        "category": "收益率曲线",
    },
    
    # ==================== 28-32 债券发行 ====================
    "bond_treasure_issue_cninfo": {
        "display_name": "国债发行",
        "description": "国债发行信息",
        "route": "/bonds/collections/bond_treasure_issue_cninfo",
        "order": 28,
        "source": "巨潮资讯",
        "category": "债券发行",
    },
    "bond_local_government_issue_cninfo": {
        "display_name": "地方债发行",
        "description": "地方债发行信息",
        "route": "/bonds/collections/bond_local_government_issue_cninfo",
        "order": 29,
        "source": "巨潮资讯",
        "category": "债券发行",
    },
    "bond_corporate_issue_cninfo": {
        "display_name": "企业债发行",
        "description": "企业债发行信息",
        "route": "/bonds/collections/bond_corporate_issue_cninfo",
        "order": 30,
        "source": "巨潮资讯",
        "category": "债券发行",
    },
    "bond_cov_issue_cninfo": {
        "display_name": "可转债发行",
        "description": "可转债发行信息",
        "route": "/bonds/collections/bond_cov_issue_cninfo",
        "order": 31,
        "source": "巨潮资讯",
        "category": "债券发行",
    },
    "bond_cov_stock_issue_cninfo": {
        "display_name": "可转债转股",
        "description": "可转债转股信息",
        "route": "/bonds/collections/bond_cov_stock_issue_cninfo",
        "order": 32,
        "source": "巨潮资讯",
        "category": "债券发行",
    },
    
    # ==================== 33-34 中债指数 ====================
    "bond_new_composite_index_cbond": {
        "display_name": "中债新综合指数",
        "description": "中债新综合指数历史数据",
        "route": "/bonds/collections/bond_new_composite_index_cbond",
        "order": 33,
        "source": "中国债券信息网",
        "category": "中债指数",
    },
    "bond_composite_index_cbond": {
        "display_name": "中债综合指数",
        "description": "中债综合指数历史数据",
        "route": "/bonds/collections/bond_composite_index_cbond",
        "order": 34,
        "source": "中国债券信息网",
        "category": "中债指数",
    },
}


def get_collection_metadata(collection_name: str) -> Dict[str, Any]:
    """获取指定集合的元信息"""
    return BOND_COLLECTION_METADATA.get(collection_name, {})


def get_all_collection_metadata() -> Dict[str, Dict[str, Any]]:
    """获取所有集合的元信息"""
    return BOND_COLLECTION_METADATA
