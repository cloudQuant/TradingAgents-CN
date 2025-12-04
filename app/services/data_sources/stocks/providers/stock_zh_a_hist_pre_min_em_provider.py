"""
盘前数据数据提供者

东方财富-股票行情-盘前数据
接口: stock_zh_a_hist_pre_min_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZhAHistPreMinEmProvider(BaseProvider):
    """盘前数据数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_a_hist_pre_min_em"
    display_name = "盘前数据"
    akshare_func = "stock_zh_a_hist_pre_min_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-股票行情-盘前数据"
    collection_route = "/stocks/collections/stock_zh_a_hist_pre_min_em"
    collection_category = "历史行情"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "start_time": "start_time",
        "end_time": "end_time"
    }
    
    # 必填参数
    required_params = ['symbol']

    # 字段信息
    field_info = [
        {"name": "时间", "type": "object", "description": "-"},
        {"name": "开盘", "type": "float64", "description": "-"},
        {"name": "收盘", "type": "float64", "description": "-"},
        {"name": "最高", "type": "float64", "description": "-"},
        {"name": "最低", "type": "float64", "description": "-"},
        {"name": "成交量", "type": "float64", "description": "注意单位: 手"},
        {"name": "成交额", "type": "float64", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
