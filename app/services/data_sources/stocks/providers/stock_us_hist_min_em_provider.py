"""
分时数据-东财数据提供者

东方财富网-行情首页-美股-每日分时行情
接口: stock_us_hist_min_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockUsHistMinEmProvider(BaseProvider):
    """分时数据-东财数据提供者"""
    
    # 必填属性
    collection_name = "stock_us_hist_min_em"
    display_name = "分时数据-东财"
    akshare_func = "stock_us_hist_min_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-行情首页-美股-每日分时行情"
    collection_route = "/stocks/collections/stock_us_hist_min_em"
    collection_category = "历史行情"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "start_date": "start_date",
        "end_date": "end_date"
    }
    
    # 必填参数
    required_params = ['symbol']

    # 字段信息
    field_info = [
        {"name": "时间", "type": "object", "description": "-"},
        {"name": "开盘", "type": "float64", "description": "注意单位: 美元"},
        {"name": "收盘", "type": "float64", "description": "注意单位: 美元"},
        {"name": "最高", "type": "float64", "description": "注意单位: 美元"},
        {"name": "最低", "type": "float64", "description": "注意单位: 美元"},
        {"name": "成交量", "type": "float64", "description": "注意单位: 股"},
        {"name": "成交额", "type": "float64", "description": "注意单位: 美元"},
        {"name": "最新价", "type": "float64", "description": "注意单位: 美元"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
