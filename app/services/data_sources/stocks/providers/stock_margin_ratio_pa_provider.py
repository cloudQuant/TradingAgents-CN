"""
标的证券名单及保证金比例查询数据提供者

融资融券-标的证券名单及保证金比例查询
接口: stock_margin_ratio_pa
"""
from app.services.data_sources.base_provider import BaseProvider


class StockMarginRatioPaProvider(BaseProvider):
    """标的证券名单及保证金比例查询数据提供者"""
    
    # 必填属性
    collection_name = "stock_margin_ratio_pa"
    display_name = "标的证券名单及保证金比例查询"
    akshare_func = "stock_margin_ratio_pa"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "融资融券-标的证券名单及保证金比例查询"
    collection_route = "/stocks/collections/stock_margin_ratio_pa"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "date": "date"
    }
    
    # 必填参数
    required_params = ['date']

    # 字段信息
    field_info = [
        {"name": "证券代码", "type": "object", "description": "-"},
        {"name": "证券简称", "type": "object", "description": "-"},
        {"name": "融资比例", "type": "float64", "description": "-"},
        {"name": "融券比例", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
