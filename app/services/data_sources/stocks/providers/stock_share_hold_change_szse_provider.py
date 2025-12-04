"""
董监高及相关人员持股变动-深证数据提供者

深圳证券交易所-信息披露-监管信息公开-董监高人员股份变动
接口: stock_share_hold_change_szse
"""
from app.services.data_sources.base_provider import BaseProvider


class StockShareHoldChangeSzseProvider(BaseProvider):
    """董监高及相关人员持股变动-深证数据提供者"""
    
    # 必填属性
    collection_name = "stock_share_hold_change_szse"
    display_name = "董监高及相关人员持股变动-深证"
    akshare_func = "stock_share_hold_change_szse"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "深圳证券交易所-信息披露-监管信息公开-董监高人员股份变动"
    collection_route = "/stocks/collections/stock_share_hold_change_szse"
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
        {"name": "证券代码", "type": "object", "description": "-"},
        {"name": "证券简称", "type": "object", "description": "-"},
        {"name": "董监高姓名", "type": "object", "description": "-"},
        {"name": "变动日期", "type": "object", "description": "-"},
        {"name": "变动股份数量", "type": "float64", "description": "注意单位: 万股"},
        {"name": "成交均价", "type": "float64", "description": "-"},
        {"name": "变动原因", "type": "object", "description": "-"},
        {"name": "变动比例", "type": "float64", "description": "注意单位: 千分之一"},
        {"name": "当日结存股数", "type": "float64", "description": "注意单位: 万股"},
        {"name": "股份变动人姓名", "type": "object", "description": "-"},
        {"name": "职务", "type": "object", "description": "-"},
        {"name": "变动人与董监高的关系", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
