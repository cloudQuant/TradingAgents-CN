"""
标的证券信息数据提供者

深圳证券交易所-融资融券数据-标的证券信息
接口: stock_margin_underlying_info_szse
"""
from app.services.data_sources.base_provider import BaseProvider


class StockMarginUnderlyingInfoSzseProvider(BaseProvider):
    """标的证券信息数据提供者"""
    
    # 必填属性
    collection_name = "stock_margin_underlying_info_szse"
    display_name = "标的证券信息"
    akshare_func = "stock_margin_underlying_info_szse"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "深圳证券交易所-融资融券数据-标的证券信息"
    collection_route = "/stocks/collections/stock_margin_underlying_info_szse"
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
        {"name": "融资标的", "type": "object", "description": "-"},
        {"name": "融券标的", "type": "object", "description": "-"},
        {"name": "当日可融资", "type": "object", "description": "-"},
        {"name": "当日可融券", "type": "object", "description": "-"},
        {"name": "融券卖出价格限制", "type": "object", "description": "-"},
        {"name": "涨跌幅限制", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
