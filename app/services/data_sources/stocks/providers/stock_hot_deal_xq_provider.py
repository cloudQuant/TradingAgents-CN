"""
交易排行榜数据提供者

雪球-沪深股市-热度排行榜-交易排行榜
接口: stock_hot_deal_xq
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHotDealXqProvider(BaseProvider):
    """交易排行榜数据提供者"""
    
    # 必填属性
    collection_name = "stock_hot_deal_xq"
    display_name = "交易排行榜"
    akshare_func = "stock_hot_deal_xq"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "雪球-沪深股市-热度排行榜-交易排行榜"
    collection_route = "/stocks/collections/stock_hot_deal_xq"
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
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "关注", "type": "float64", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "注意单位: 元"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
