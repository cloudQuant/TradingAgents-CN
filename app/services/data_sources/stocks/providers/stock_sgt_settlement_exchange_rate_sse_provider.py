"""
结算汇率-沪港通数据提供者

沪港通-港股通信息披露-结算汇兑
接口: stock_sgt_settlement_exchange_rate_sse
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockSgtSettlementExchangeRateSseProvider(SimpleProvider):
    """结算汇率-沪港通数据提供者"""
    
    # 必填属性
    collection_name = "stock_sgt_settlement_exchange_rate_sse"
    display_name = "结算汇率-沪港通"
    akshare_func = "stock_sgt_settlement_exchange_rate_sse"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "沪港通-港股通信息披露-结算汇兑"
    collection_route = "/stocks/collections/stock_sgt_settlement_exchange_rate_sse"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "适用日期", "type": "object", "description": "-"},
        {"name": "买入结算汇兑比率", "type": "float64", "description": "-"},
        {"name": "卖出结算汇兑比率", "type": "float64", "description": "-"},
        {"name": "货币种类", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
