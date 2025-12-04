"""
飙升榜-A股数据提供者

东方财富-个股人气榜-飙升榜
接口: stock_hot_up_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockHotUpEmProvider(SimpleProvider):
    """飙升榜-A股数据提供者"""
    
    # 必填属性
    collection_name = "stock_hot_up_em"
    display_name = "飙升榜-A股"
    akshare_func = "stock_hot_up_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-个股人气榜-飙升榜"
    collection_route = "/stocks/collections/stock_hot_up_em"
    collection_category = "热门排行"

    # 字段信息
    field_info = [
        {"name": "排名较昨日变动", "type": "int64", "description": "-"},
        {"name": "当前排名", "type": "int64", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "涨跌额", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
