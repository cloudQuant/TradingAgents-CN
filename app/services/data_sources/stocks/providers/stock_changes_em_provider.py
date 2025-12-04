"""
盘口异动数据提供者

东方财富-行情中心-盘口异动数据
接口: stock_changes_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockChangesEmProvider(BaseProvider):
    """盘口异动数据提供者"""
    
    # 必填属性
    collection_name = "stock_changes_em"
    display_name = "盘口异动"
    akshare_func = "stock_changes_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-行情中心-盘口异动数据"
    collection_route = "/stocks/collections/stock_changes_em"
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
        {"name": "时间", "type": "object", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "板块", "type": "object", "description": "-"},
        {"name": "相关信息", "type": "object", "description": "注意: 不同的 symbol 的单位不同"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
