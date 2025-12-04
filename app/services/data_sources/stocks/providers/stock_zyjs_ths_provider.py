"""
主营介绍-同花顺数据提供者

同花顺-主营介绍
接口: stock_zyjs_ths
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZyjsThsProvider(BaseProvider):
    """主营介绍-同花顺数据提供者"""
    
    # 必填属性
    collection_name = "stock_zyjs_ths"
    display_name = "主营介绍-同花顺"
    akshare_func = "stock_zyjs_ths"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "同花顺-主营介绍"
    collection_route = "/stocks/collections/stock_zyjs_ths"
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
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "主营业务", "type": "object", "description": "-"},
        {"name": "产品类型", "type": "object", "description": "-"},
        {"name": "经营范围", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
