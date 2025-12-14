"""
上海证券交易所数据提供者

上海证券交易所-股票数据总貌
接口: stock_sse_summary
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockSseSummaryProvider(SimpleProvider):
    """上海证券交易所数据提供者"""
    
    # 必填属性
    collection_name = "stock_sse_summary"
    display_name = "上海证券交易所"
    akshare_func = "stock_sse_summary"
    unique_keys = ['项目']  # 修复：使用实际存在的字段作为唯一键
    
    # 可选属性
    collection_description = "上海证券交易所-股票数据总貌"
    collection_route = "/stocks/collections/stock_sse_summary"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "项目", "type": "object", "description": "统计项目名称"},
        {"name": "股票", "type": "object", "description": "股票数据"},
        {"name": "科创板", "type": "object", "description": "科创板数据"},
        {"name": "主板", "type": "object", "description": "主板数据"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
