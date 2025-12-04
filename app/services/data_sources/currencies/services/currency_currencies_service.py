"""货币基础信息查询服务"""
from app.services.data_sources.base_service import SimpleService


class CurrencyCurrenciesService(SimpleService):
    """货币基础信息查询服务"""
    collection_name = "currency_currencies"
