"""
涨跌投票数据提供者

百度股市通- A 股或指数-股评-投票
接口: stock_zh_vote_baidu
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZhVoteBaiduProvider(BaseProvider):
    """涨跌投票数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_vote_baidu"
    display_name = "涨跌投票"
    akshare_func = "stock_zh_vote_baidu"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "百度股市通- A 股或指数-股评-投票"
    collection_route = "/stocks/collections/stock_zh_vote_baidu"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "indicator": "indicator"
    }
    
    # 必填参数
    required_params = ['symbol', 'indicator']

    # 字段信息
    field_info = [
        {"name": "周期", "type": "object", "description": "-"},
        {"name": "看涨", "type": "object", "description": "-"},
        {"name": "看跌", "type": "object", "description": "-"},
        {"name": "看涨比例", "type": "object", "description": "-"},
        {"name": "看跌比例", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
