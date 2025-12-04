"""
富途牛牛-美股概念-成分股数据提供者

富途牛牛-主题投资-概念板块-成分股
接口: stock_concept_cons_futu
"""
from app.services.data_sources.base_provider import BaseProvider


class StockConceptConsFutuProvider(BaseProvider):
    """富途牛牛-美股概念-成分股数据提供者"""
    
    # 必填属性
    collection_name = "stock_concept_cons_futu"
    display_name = "富途牛牛-美股概念-成分股"
    akshare_func = "stock_concept_cons_futu"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "富途牛牛-主题投资-概念板块-成分股"
    collection_route = "/stocks/collections/stock_concept_cons_futu"
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
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "涨跌额", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "object", "description": "-"},
        {"name": "成交量", "type": "object", "description": "-"},
        {"name": "成交额", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
