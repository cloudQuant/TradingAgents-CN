"""
互动易-提问服务

互动易-提问
接口: stock_irm_cninfo
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_irm_cninfo_provider import StockIrmCninfoProvider


class StockIrmCninfoService(BaseService):
    """互动易-提问服务"""
    
    collection_name = "stock_irm_cninfo"
    provider_class = StockIrmCninfoProvider
    
    # 时间字段名
    time_field = "更新时间"
