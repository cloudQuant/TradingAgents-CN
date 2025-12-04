"""
个股信息查询-东财数据提供者

东方财富-个股-股票信息
接口: stock_individual_info_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockIndividualInfoEmProvider(BaseProvider):
    """个股信息查询-东财数据提供者"""
    
    # 必填属性
    collection_name = "stock_individual_info_em"
    display_name = "个股信息查询-东财"
    akshare_func = "stock_individual_info_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-个股-股票信息"
    collection_route = "/stocks/collections/stock_individual_info_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "timeout": "timeout"
    }
    
    # 必填参数
    required_params = ['symbol']

    # 字段信息
    field_info = [
        {"name": "item", "type": "object", "description": "-"},
        {"name": "value", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
