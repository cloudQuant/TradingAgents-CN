"""
标的证券名单及保证金比例查询服务

融资融券-标的证券名单及保证金比例查询
接口: stock_margin_ratio_pa
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_margin_ratio_pa_provider import StockMarginRatioPaProvider


class StockMarginRatioPaService(BaseService):
    """标的证券名单及保证金比例查询服务"""
    
    collection_name = "stock_margin_ratio_pa"
    provider_class = StockMarginRatioPaProvider
    
    # 时间字段名
    time_field = "更新时间"
