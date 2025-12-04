"""
板块详情数据提供者

新浪行业-板块行情-成份详情, 由于新浪网页提供的统计数据有误, 部分行业数量大于统计数
接口: stock_sector_detail
"""
from app.services.data_sources.base_provider import BaseProvider


class StockSectorDetailProvider(BaseProvider):
    """板块详情数据提供者"""
    
    # 必填属性
    collection_name = "stock_sector_detail"
    display_name = "板块详情"
    akshare_func = "stock_sector_detail"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪行业-板块行情-成份详情, 由于新浪网页提供的统计数据有误, 部分行业数量大于统计数"
    collection_route = "/stocks/collections/stock_sector_detail"
    collection_category = "板块数据"

    # 参数映射
    param_mapping = {
        "sector": "sector"
    }
    
    # 必填参数
    required_params = ['sector']

    # 字段信息
    field_info = [
        {"name": "symbol", "type": "object", "description": "-"},
        {"name": "code", "type": "object", "description": "-"},
        {"name": "name", "type": "object", "description": "-"},
        {"name": "trade", "type": "float64", "description": "-"},
        {"name": "pricechange", "type": "float64", "description": "-"},
        {"name": "changepercent", "type": "float64", "description": "-"},
        {"name": "buy", "type": "float64", "description": "-"},
        {"name": "sell", "type": "float64", "description": "-"},
        {"name": "settlement", "type": "float64", "description": "-"},
        {"name": "open", "type": "float64", "description": "-"},
        {"name": "high", "type": "float64", "description": "-"},
        {"name": "low", "type": "float64", "description": "-"},
        {"name": "volume", "type": "int64", "description": "-"},
        {"name": "amount", "type": "int64", "description": "-"},
        {"name": "ticktime", "type": "object", "description": "-"},
        {"name": "per", "type": "float64", "description": "-"},
        {"name": "pb", "type": "float64", "description": "-"},
        {"name": "mktcap", "type": "float64", "description": "-"},
        {"name": "nmc", "type": "float64", "description": "-"},
        {"name": "turnoverratio", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
