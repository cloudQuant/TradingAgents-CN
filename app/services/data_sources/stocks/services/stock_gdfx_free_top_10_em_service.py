"""
十大流通股东(个股)服务

东方财富网-个股-十大流通股东
接口: stock_gdfx_free_top_10_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_gdfx_free_top_10_em_provider import StockGdfxFreeTop10EmProvider


class StockGdfxFreeTop10EmService(BaseService):
    """十大流通股东(个股)服务"""
    
    collection_name = "stock_gdfx_free_top_10_em"
    provider_class = StockGdfxFreeTop10EmProvider
    
    # 时间字段名
    time_field = "更新时间"
