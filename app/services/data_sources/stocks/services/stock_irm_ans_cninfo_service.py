"""
互动易-回答服务

互动易-回答
接口: stock_irm_ans_cninfo
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_irm_ans_cninfo_provider import StockIrmAnsCninfoProvider


class StockIrmAnsCninfoService(BaseService):
    """互动易-回答服务"""
    
    collection_name = "stock_irm_ans_cninfo"
    provider_class = StockIrmAnsCninfoProvider
    
    # 时间字段名
    time_field = "更新时间"
