"""
名称变更-深证数据提供者

深证证券交易所-市场数据-股票数据-名称变更
接口: stock_info_sz_change_name
"""
from app.services.data_sources.base_provider import BaseProvider


class StockInfoSzChangeNameProvider(BaseProvider):
    """名称变更-深证数据提供者"""
    
    # 必填属性
    collection_name = "stock_info_sz_change_name"
    display_name = "名称变更-深证"
    akshare_func = "stock_info_sz_change_name"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "深证证券交易所-市场数据-股票数据-名称变更"
    collection_route = "/stocks/collections/stock_info_sz_change_name"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol"
    }
    
    # 必填参数
    required_params = ['symbol']

    # 字段信息
    field_info = [
        {"name": "变更日期", "type": "object", "description": "-"},
        {"name": "证券代码", "type": "object", "description": "-"},
        {"name": "证券简称", "type": "object", "description": "-"},
        {"name": "变更前全称", "type": "object", "description": "-"},
        {"name": "变更后全称", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
