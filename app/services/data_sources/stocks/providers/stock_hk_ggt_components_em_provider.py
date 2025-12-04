"""
港股通成份股数据提供者

东方财富网-行情中心-港股市场-港股通成份股
接口: stock_hk_ggt_components_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockHkGgtComponentsEmProvider(SimpleProvider):
    """港股通成份股数据提供者"""
    
    # 必填属性
    collection_name = "stock_hk_ggt_components_em"
    display_name = "港股通成份股"
    akshare_func = "stock_hk_ggt_components_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-行情中心-港股市场-港股通成份股"
    collection_route = "/stocks/collections/stock_hk_ggt_components_em"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "注意单位: HKD"},
        {"name": "涨跌额", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "-"},
        {"name": "今开", "type": "float64", "description": "-"},
        {"name": "最高", "type": "float64", "description": "-"},
        {"name": "最低", "type": "float64", "description": "-"},
        {"name": "昨收", "type": "float64", "description": "-"},
        {"name": "成交量", "type": "float64", "description": "注意单位: 股"},
        {"name": "成交额", "type": "float64", "description": "注意单位: 港元"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
