"""
分红配送-东财服务

东方财富-数据中心-年报季报-分红配送
接口: stock_fhps_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_fhps_em_provider import StockFhpsEmProvider


class StockFhpsEmService(BaseService):
    """分红配送-东财服务"""
    
    collection_name = "stock_fhps_em"
    provider_class = StockFhpsEmProvider
    
    # 时间字段名
    time_field = "更新时间"
