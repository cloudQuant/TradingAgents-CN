"""新加坡交易所期货-结算价服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesSettlementPriceSgxService(SimpleService):
    """新加坡交易所期货-结算价服务"""
    collection_name = "futures_settlement_price_sgx"
