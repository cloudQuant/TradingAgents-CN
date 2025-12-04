"""
上证e互动服务

上证e互动-提问与回答
接口: stock_sns_sseinfo
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_sns_sseinfo_provider import StockSnsSseinfoProvider


class StockSnsSseinfoService(BaseService):
    """上证e互动服务"""
    
    collection_name = "stock_sns_sseinfo"
    provider_class = StockSnsSseinfoProvider
    
    # 时间字段名
    time_field = "更新时间"
