"""
相关股票数据提供者

东方财富-个股人气榜-相关股票
接口: stock_hot_rank_relate_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHotRankRelateEmProvider(BaseProvider):
    """相关股票数据提供者"""
    
    # 必填属性
    collection_name = "stock_hot_rank_relate_em"
    display_name = "相关股票"
    akshare_func = "stock_hot_rank_relate_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富-个股人气榜-相关股票"
    collection_route = "/stocks/collections/stock_hot_rank_relate_em"
    collection_category = "热门排行"

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
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "相关股票代码", "type": "object", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
