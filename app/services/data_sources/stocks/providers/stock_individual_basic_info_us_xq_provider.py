"""
个股信息查询-雪球数据提供者

雪球-个股-公司概况-公司简介
接口: stock_individual_basic_info_us_xq
"""
from app.services.data_sources.base_provider import BaseProvider


class StockIndividualBasicInfoUsXqProvider(BaseProvider):
    """个股信息查询-雪球数据提供者"""
    
    # 必填属性
    collection_name = "stock_individual_basic_info_us_xq"
    display_name = "个股信息查询-雪球"
    akshare_func = "stock_individual_basic_info_us_xq"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "雪球-个股-公司概况-公司简介"
    collection_route = "/stocks/collections/stock_individual_basic_info_us_xq"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "token": "token",
        "timeout": "timeout"
    }
    
    # 必填参数
    required_params = ['symbol', 'token']

    # 字段信息
    field_info = [
        {"name": "item", "type": "object", "description": "-"},
        {"name": "value", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
