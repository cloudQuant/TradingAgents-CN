"""新加坡交易所期货-结算价服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_settlement_price_sgx_provider import FuturesSettlementPriceSgxProvider


class FuturesSettlementPriceSgxService(SimpleService):
    """新加坡交易所期货-结算价服务"""
    collection_name = "futures_settlement_price_sgx"
    provider_class = FuturesSettlementPriceSgxProvider
