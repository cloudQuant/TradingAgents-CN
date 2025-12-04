"""
港股数据提供者

东方财富-个股人气榜-最新排名
接口: stock_hk_hot_rank_latest_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHkHotRankLatestEmProvider(BaseProvider):
    """港股数据提供者"""
    
    # 必填属性
    collection_name = "stock_hk_hot_rank_latest_em"
    display_name = "港股"
    akshare_func = "stock_hk_hot_rank_latest_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-个股人气榜-最新排名"
    collection_route = "/stocks/collections/stock_hk_hot_rank_latest_em"
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
        {"name": "item", "type": "object", "description": "-"},
        {"name": "value", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
