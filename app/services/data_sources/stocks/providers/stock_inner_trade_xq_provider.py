"""
内部交易数据提供者

雪球-行情中心-沪深股市-内部交易
接口: stock_inner_trade_xq
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockInnerTradeXqProvider(SimpleProvider):
    """内部交易数据提供者"""
    
    # 必填属性
    collection_name = "stock_inner_trade_xq"
    display_name = "内部交易"
    akshare_func = "stock_inner_trade_xq"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "雪球-行情中心-沪深股市-内部交易"
    collection_route = "/stocks/collections/stock_inner_trade_xq"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "变动日期", "type": "object", "description": "-"},
        {"name": "变动人", "type": "object", "description": "-"},
        {"name": "变动股数", "type": "int64", "description": "-"},
        {"name": "成交均价", "type": "float64", "description": "-"},
        {"name": "变动后持股数", "type": "float64", "description": "-"},
        {"name": "与董监高关系", "type": "object", "description": "-"},
        {"name": "董监高职务", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
