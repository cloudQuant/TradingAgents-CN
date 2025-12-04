"""
沪深港通持股-个股服务

东方财富网-数据中心-沪深港通-沪深港通持股-具体股票
接口: stock_hsgt_individual_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hsgt_individual_em_provider import StockHsgtIndividualEmProvider


class StockHsgtIndividualEmService(BaseService):
    """沪深港通持股-个股服务"""
    
    collection_name = "stock_hsgt_individual_em"
    provider_class = StockHsgtIndividualEmProvider
    
    # 时间字段名
    time_field = "更新时间"
