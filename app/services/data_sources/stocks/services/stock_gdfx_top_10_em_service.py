"""
十大股东(个股)服务

东方财富网-个股-十大股东
接口: stock_gdfx_top_10_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_gdfx_top_10_em_provider import StockGdfxTop10EmProvider


class StockGdfxTop10EmService(BaseService):
    """十大股东(个股)服务"""
    
    collection_name = "stock_gdfx_top_10_em"
    provider_class = StockGdfxTop10EmProvider
    
    # 时间字段名
    time_field = "更新时间"
