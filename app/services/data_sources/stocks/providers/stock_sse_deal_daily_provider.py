"""
上海证券交易所-每日概况数据提供者

上海证券交易所-数据-股票数据-成交概况-股票成交概况-每日股票情况
接口: stock_sse_deal_daily
"""
from app.services.data_sources.base_provider import BaseProvider


class StockSseDealDailyProvider(BaseProvider):
    """上海证券交易所-每日概况数据提供者"""
    
    # 必填属性
    collection_name = "stock_sse_deal_daily"
    display_name = "上海证券交易所-每日概况"
    akshare_func = "stock_sse_deal_daily"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "上海证券交易所-数据-股票数据-成交概况-股票成交概况-每日股票情况"
    collection_route = "/stocks/collections/stock_sse_deal_daily"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "date": "date"
    }
    
    # 必填参数
    required_params = ['date']

    # 字段信息
    field_info = [
        {"name": "单日情况", "type": "object", "description": "包含了网页所有字段"},
        {"name": "股票", "type": "float64", "description": "-"},
        {"name": "主板A", "type": "float64", "description": "-"},
        {"name": "主板B", "type": "float64", "description": "-"},
        {"name": "科创板", "type": "float64", "description": "-"},
        {"name": "股票回购", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
