"""
热搜股票数据提供者

百度股市通-热搜股票
接口: stock_hot_search_baidu
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHotSearchBaiduProvider(BaseProvider):
    """热搜股票数据提供者"""
    
    # 必填属性
    collection_name = "stock_hot_search_baidu"
    display_name = "热搜股票"
    akshare_func = "stock_hot_search_baidu"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "百度股市通-热搜股票"
    collection_route = "/stocks/collections/stock_hot_search_baidu"
    collection_category = "热门排行"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "date": "date",
        "time": "time"
    }
    
    # 必填参数
    required_params = ['symbol', 'date', 'time']

    # 字段信息
    field_info = [
        {"name": "涨跌幅", "type": "object", "description": "-"},
        {"name": "综合热度", "type": "int64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
