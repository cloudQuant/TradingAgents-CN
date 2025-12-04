"""
AB 股比价数据提供者

东方财富网-行情中心-沪深京个股-AB股比价-全部AB股比价
接口: stock_zh_ab_comparison_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockZhAbComparisonEmProvider(SimpleProvider):
    """AB 股比价数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_ab_comparison_em"
    display_name = "AB 股比价"
    akshare_func = "stock_zh_ab_comparison_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-行情中心-沪深京个股-AB股比价-全部AB股比价"
    collection_route = "/stocks/collections/stock_zh_ab_comparison_em"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "B股代码", "type": "object", "description": "-"},
        {"name": "最新价B", "type": "float64", "description": "-"},
        {"name": "涨跌幅B", "type": "float64", "description": "-"},
        {"name": "A股代码", "type": "object", "description": "-"},
        {"name": "最新价A", "type": "float64", "description": "-"},
        {"name": "涨跌幅A", "type": "float64", "description": "-"},
        {"name": "比价", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
