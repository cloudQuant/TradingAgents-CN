"""
新股上市首日数据提供者

同花顺-数据中心-新股数据-新股上市首日
接口: stock_xgsr_ths
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockXgsrThsProvider(SimpleProvider):
    """新股上市首日数据提供者"""
    
    # 必填属性
    collection_name = "stock_xgsr_ths"
    display_name = "新股上市首日"
    akshare_func = "stock_xgsr_ths"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "同花顺-数据中心-新股数据-新股上市首日"
    collection_route = "/stocks/collections/stock_xgsr_ths"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "上市日期", "type": "object", "description": "-"},
        {"name": "发行价", "type": "float64", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "首日开盘价", "type": "float64", "description": "-"},
        {"name": "首日收盘价", "type": "float64", "description": "-"},
        {"name": "首日最高价", "type": "float64", "description": "-"},
        {"name": "首日最低价", "type": "float64", "description": "-"},
        {"name": "首日涨跌幅", "type": "float64", "description": "-"},
        {"name": "是否破发", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
