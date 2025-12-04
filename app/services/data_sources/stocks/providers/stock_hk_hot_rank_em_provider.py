"""
人气榜-港股数据提供者

东方财富-个股人气榜-人气榜-港股市场
接口: stock_hk_hot_rank_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockHkHotRankEmProvider(SimpleProvider):
    """人气榜-港股数据提供者"""
    
    # 必填属性
    collection_name = "stock_hk_hot_rank_em"
    display_name = "人气榜-港股"
    akshare_func = "stock_hk_hot_rank_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-个股人气榜-人气榜-港股市场"
    collection_route = "/stocks/collections/stock_hk_hot_rank_em"
    collection_category = "热门排行"

    # 字段信息
    field_info = [
        {"name": "当前排名", "type": "int64", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
