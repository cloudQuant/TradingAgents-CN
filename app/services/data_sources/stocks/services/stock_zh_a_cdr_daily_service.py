"""
历史行情数据服务

上海证券交易所-科创板-CDR
接口: stock_zh_a_cdr_daily
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zh_a_cdr_daily_provider import StockZhACdrDailyProvider


class StockZhACdrDailyService(BaseService):
    """历史行情数据服务"""
    
    collection_name = "stock_zh_a_cdr_daily"
    provider_class = StockZhACdrDailyProvider
    
    # 时间字段名
    time_field = "更新时间"
