"""
分红配送详情-东财服务

东方财富网-数据中心-分红送配-分红送配详情
接口: stock_fhps_detail_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_fhps_detail_em_provider import StockFhpsDetailEmProvider


class StockFhpsDetailEmService(BaseService):
    """分红配送详情-东财服务"""
    
    collection_name = "stock_fhps_detail_em"
    provider_class = StockFhpsDetailEmProvider
    
    # 时间字段名
    time_field = "更新时间"
