"""生猪-成本维度服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesHogCostService(SimpleService):
    """生猪-成本维度服务"""
    collection_name = "futures_hog_cost"
