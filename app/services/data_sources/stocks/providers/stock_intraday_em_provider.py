"""
日内分时数据-东财数据提供者

东方财富-分时数据
接口: stock_intraday_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockIntradayEmProvider(BaseProvider):
    """日内分时数据-东财数据提供者"""
    
    # 必填属性
    collection_name = "stock_intraday_em"
    display_name = "日内分时数据-东财"
    akshare_func = "stock_intraday_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-分时数据"
    collection_route = "/stocks/collections/stock_intraday_em"
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
        {"name": "时间", "type": "object", "description": "-"},
        {"name": "成交价", "type": "float64", "description": "-"},
        {"name": "手数", "type": "int64", "description": "-"},
        {"name": "买卖盘性质", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
