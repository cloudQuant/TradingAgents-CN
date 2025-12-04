"""
次新股数据提供者

新浪财经-行情中心-沪深股市-次新股
接口: stock_zh_a_new
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockZhANewProvider(SimpleProvider):
    """次新股数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_a_new"
    display_name = "次新股"
    akshare_func = "stock_zh_a_new"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-行情中心-沪深股市-次新股"
    collection_route = "/stocks/collections/stock_zh_a_new"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "symbol", "type": "object", "description": "新浪代码"},
        {"name": "code", "type": "object", "description": "股票代码"},
        {"name": "name", "type": "object", "description": "股票简称"},
        {"name": "open", "type": "float64", "description": "开盘价"},
        {"name": "high", "type": "float64", "description": "最高价"},
        {"name": "low", "type": "float64", "description": "最低价"},
        {"name": "volume", "type": "int64", "description": "成交量"},
        {"name": "amount", "type": "int64", "description": "成交额"},
        {"name": "mktcap", "type": "float64", "description": "市值"},
        {"name": "turnoverratio", "type": "float64", "description": "换手率"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
