"""
结算汇率-深港通服务

深港通-港股通业务信息-结算汇率
接口: stock_sgt_settlement_exchange_rate_szse
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_sgt_settlement_exchange_rate_szse_provider import StockSgtSettlementExchangeRateSzseProvider


class StockSgtSettlementExchangeRateSzseService(SimpleService):
    """结算汇率-深港通服务"""
    
    collection_name = "stock_sgt_settlement_exchange_rate_szse"
    provider_class = StockSgtSettlementExchangeRateSzseProvider
    
    # 时间字段名
    time_field = "更新时间"
