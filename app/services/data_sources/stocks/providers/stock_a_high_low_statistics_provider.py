"""
创新高和新低的股票数量数据提供者

不同市场的创新高和新低的股票数量
接口: stock_a_high_low_statistics
"""
from app.services.data_sources.base_provider import BaseProvider


class StockAHighLowStatisticsProvider(BaseProvider):
    """创新高和新低的股票数量数据提供者"""
    
    # 必填属性
    collection_name = "stock_a_high_low_statistics"
    display_name = "创新高和新低的股票数量"
    akshare_func = "stock_a_high_low_statistics"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "不同市场的创新高和新低的股票数量"
    collection_route = "/stocks/collections/stock_a_high_low_statistics"
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
        {"name": "date", "type": "object", "description": "交易日"},
        {"name": "close", "type": "float64", "description": "相关指数收盘价"},
        {"name": "high20", "type": "int64", "description": "20日新高"},
        {"name": "low20", "type": "int64", "description": "20日新低"},
        {"name": "high60", "type": "int64", "description": "60日新高"},
        {"name": "low60", "type": "int64", "description": "60日新低"},
        {"name": "high120", "type": "int64", "description": "120日新高"},
        {"name": "low120", "type": "int64", "description": "120日新低"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
