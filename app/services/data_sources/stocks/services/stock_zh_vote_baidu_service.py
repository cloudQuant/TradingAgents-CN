"""
涨跌投票服务

百度股市通- A 股或指数-股评-投票
接口: stock_zh_vote_baidu
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zh_vote_baidu_provider import StockZhVoteBaiduProvider


class StockZhVoteBaiduService(BaseService):
    """涨跌投票服务"""
    
    collection_name = "stock_zh_vote_baidu"
    provider_class = StockZhVoteBaiduProvider
    
    # 时间字段名
    time_field = "更新时间"
