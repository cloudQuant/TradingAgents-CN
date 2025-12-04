"""
参考汇率-沪港通服务

沪港通-港股通信息披露-参考汇率
接口: stock_sgt_reference_exchange_rate_sse
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_sgt_reference_exchange_rate_sse_provider import StockSgtReferenceExchangeRateSseProvider


class StockSgtReferenceExchangeRateSseService(SimpleService):
    """参考汇率-沪港通服务"""
    
    collection_name = "stock_sgt_reference_exchange_rate_sse"
    provider_class = StockSgtReferenceExchangeRateSseProvider
    
    # 时间字段名
    time_field = "更新时间"
