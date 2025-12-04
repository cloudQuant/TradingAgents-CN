"""
A股数据提供者

东方财富网-股票热度-历史趋势及粉丝特征
接口: stock_hot_rank_detail_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHotRankDetailEmProvider(BaseProvider):
    """A股数据提供者"""
    
    # 必填属性
    collection_name = "stock_hot_rank_detail_em"
    display_name = "A股"
    akshare_func = "stock_hot_rank_detail_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-股票热度-历史趋势及粉丝特征"
    collection_route = "/stocks/collections/stock_hot_rank_detail_em"
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
        {"name": "排名", "type": "int64", "description": "-"},
        {"name": "证券代码", "type": "object", "description": "-"},
        {"name": "新晋粉丝", "type": "float64", "description": "-"},
        {"name": "铁杆粉丝", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
