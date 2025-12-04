"""
实时行情数据-新浪数据提供者

新浪财经-美股; 获取的数据有 15 分钟延迟; 建议使用 ak.stock_us_spot_em() 来获取数据
接口: stock_us_spot
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockUsSpotProvider(SimpleProvider):
    """实时行情数据-新浪数据提供者"""
    
    # 必填属性
    collection_name = "stock_us_spot"
    display_name = "实时行情数据-新浪"
    akshare_func = "stock_us_spot"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-美股; 获取的数据有 15 分钟延迟; 建议使用 ak.stock_us_spot_em() 来获取数据"
    collection_route = "/stocks/collections/stock_us_spot"
    collection_category = "实时行情"

    # 字段信息
    field_info = [
        {"name": "-", "type": "-", "description": "新浪默认"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
