"""
历史行情数据数据提供者

腾讯财经-A+H 股数据
接口: stock_zh_ah_daily
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZhAhDailyProvider(BaseProvider):
    """历史行情数据数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_ah_daily"
    display_name = "历史行情数据"
    akshare_func = "stock_zh_ah_daily"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "腾讯财经-A+H 股数据"
    collection_route = "/stocks/collections/stock_zh_ah_daily"
    collection_category = "历史行情"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "start_year": "start_year",
        "end_year": "end_year",
        "adjust": "adjust"
    }
    
    # 必填参数
    required_params = ['symbol', 'start_year', 'end_year']

    # 字段信息
    field_info = [
        {"name": "日期", "type": "object", "description": "-"},
        {"name": "开盘", "type": "float64", "description": "-"},
        {"name": "收盘", "type": "float64", "description": "-"},
        {"name": "最高", "type": "float64", "description": "-"},
        {"name": "最低", "type": "float64", "description": "-"},
        {"name": "成交量", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
