"""
暂停/终止上市-上证数据提供者

上海证券交易所暂停/终止上市股票
接口: stock_info_sh_delist
"""
from app.services.data_sources.base_provider import BaseProvider


class StockInfoShDelistProvider(BaseProvider):
    """暂停/终止上市-上证数据提供者"""
    
    # 必填属性
    collection_name = "stock_info_sh_delist"
    display_name = "暂停/终止上市-上证"
    akshare_func = "stock_info_sh_delist"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "上海证券交易所暂停/终止上市股票"
    collection_route = "/stocks/collections/stock_info_sh_delist"
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
        {"name": "公司简称", "type": "object", "description": "-"},
        {"name": "上市日期", "type": "object", "description": "-"},
        {"name": "暂停上市日期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
