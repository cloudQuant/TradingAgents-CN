"""
董监高及相关人员持股变动-北证数据提供者

北京证券交易所-信息披露-监管信息-董监高及相关人员持股变动
接口: stock_share_hold_change_bse
"""
from app.services.data_sources.base_provider import BaseProvider


class StockShareHoldChangeBseProvider(BaseProvider):
    """董监高及相关人员持股变动-北证数据提供者"""
    
    # 必填属性
    collection_name = "stock_share_hold_change_bse"
    display_name = "董监高及相关人员持股变动-北证"
    akshare_func = "stock_share_hold_change_bse"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "北京证券交易所-信息披露-监管信息-董监高及相关人员持股变动"
    collection_route = "/stocks/collections/stock_share_hold_change_bse"
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
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "简称", "type": "object", "description": "-"},
        {"name": "姓名", "type": "object", "description": "-"},
        {"name": "职务", "type": "object", "description": "-"},
        {"name": "变动日期", "type": "object", "description": "-"},
        {"name": "变动股数", "type": "float64", "description": "注意单位: 万股"},
        {"name": "变动前持股数", "type": "float64", "description": "注意单位: 万股"},
        {"name": "变动后持股数", "type": "float64", "description": "注意单位: 万股"},
        {"name": "变动均价", "type": "float64", "description": "注意单位: 元"},
        {"name": "变动原因", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
