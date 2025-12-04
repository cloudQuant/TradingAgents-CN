"""
董监高及相关人员持股变动-上证数据提供者

上海证券交易所-披露-监管信息公开-公司监管-董董监高人员股份变动
接口: stock_share_hold_change_sse
"""
from app.services.data_sources.base_provider import BaseProvider


class StockShareHoldChangeSseProvider(BaseProvider):
    """董监高及相关人员持股变动-上证数据提供者"""
    
    # 必填属性
    collection_name = "stock_share_hold_change_sse"
    display_name = "董监高及相关人员持股变动-上证"
    akshare_func = "stock_share_hold_change_sse"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "上海证券交易所-披露-监管信息公开-公司监管-董董监高人员股份变动"
    collection_route = "/stocks/collections/stock_share_hold_change_sse"
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
        {"name": "公司代码", "type": "object", "description": "-"},
        {"name": "姓名", "type": "object", "description": "-"},
        {"name": "职务", "type": "object", "description": "-"},
        {"name": "股票种类", "type": "object", "description": "-"},
        {"name": "货币种类", "type": "object", "description": "-"},
        {"name": "本次变动前持股数", "type": "int64", "description": "-"},
        {"name": "变动数", "type": "int64", "description": "-"},
        {"name": "本次变动平均价格", "type": "float64", "description": "-"},
        {"name": "变动后持股数", "type": "int64", "description": "-"},
        {"name": "变动原因", "type": "object", "description": "-"},
        {"name": "变动日期", "type": "object", "description": "-"},
        {"name": "填报日期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
