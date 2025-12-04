"""
参考汇率-深港通数据提供者

深港通-港股通业务信息-参考汇率
接口: stock_sgt_reference_exchange_rate_szse
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockSgtReferenceExchangeRateSzseProvider(SimpleProvider):
    """参考汇率-深港通数据提供者"""
    
    # 必填属性
    collection_name = "stock_sgt_reference_exchange_rate_szse"
    display_name = "参考汇率-深港通"
    akshare_func = "stock_sgt_reference_exchange_rate_szse"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "深港通-港股通业务信息-参考汇率"
    collection_route = "/stocks/collections/stock_sgt_reference_exchange_rate_szse"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "适用日期", "type": "object", "description": "-"},
        {"name": "参考汇率买入价", "type": "float64", "description": "-"},
        {"name": "参考汇率卖出价", "type": "float64", "description": "-"},
        {"name": "货币种类", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
