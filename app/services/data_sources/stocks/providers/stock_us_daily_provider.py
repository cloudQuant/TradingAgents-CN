"""
历史行情数据-新浪数据提供者

美股历史行情数据，设定 adjust="qfq" 则返回前复权后的数据，默认 adjust="", 则返回未复权的数据，历史数据按日频率更新
接口: stock_us_daily
"""
from app.services.data_sources.base_provider import BaseProvider


class StockUsDailyProvider(BaseProvider):
    """历史行情数据-新浪数据提供者"""
    
    # 必填属性
    collection_name = "stock_us_daily"
    display_name = "历史行情数据-新浪"
    akshare_func = "stock_us_daily"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "美股历史行情数据，设定 adjust="qfq" 则返回前复权后的数据，默认 adjust="", 则返回未复权的数据，历史数据按日频率更新"
    collection_route = "/stocks/collections/stock_us_daily"
    collection_category = "历史行情"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "adjust": "adjust"
    }
    
    # 必填参数
    required_params = ['symbol']

    # 字段信息
    field_info = [
        {"name": "date", "type": "datetime64", "description": "-"},
        {"name": "open", "type": "float64", "description": "开盘价"},
        {"name": "high", "type": "float64", "description": "最高价"},
        {"name": "low", "type": "float64", "description": "最低价"},
        {"name": "close", "type": "float64", "description": "收盘价"},
        {"name": "volume", "type": "float64", "description": "成交量"},
        {"name": "date", "type": "datetime64", "description": "日期"},
        {"name": "qfq_factor", "type": "float", "description": "前复权因子"},
        {"name": "adjust", "type": "float", "description": "由于前复权会出现负值, 该值为调整因子"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
