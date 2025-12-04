"""
股东增减持服务

东方财富网-数据中心-特色数据-高管持股
接口: stock_ggcg_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_ggcg_em_provider import StockGgcgEmProvider


class StockGgcgEmService(BaseService):
    """股东增减持服务"""
    
    collection_name = "stock_ggcg_em"
    provider_class = StockGgcgEmProvider
    
    # 时间字段名
    time_field = "更新时间"
