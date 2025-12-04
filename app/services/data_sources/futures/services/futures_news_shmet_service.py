"""期货资讯服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesNewsShmetService(SimpleService):
    """期货资讯服务"""
    collection_name = "futures_news_shmet"
