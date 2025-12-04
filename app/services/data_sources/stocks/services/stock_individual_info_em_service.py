"""
个股信息查询-东财服务

东方财富-个股-股票信息
接口: stock_individual_info_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_individual_info_em_provider import StockIndividualInfoEmProvider


class StockIndividualInfoEmService(BaseService):
    """个股信息查询-东财服务"""
    
    collection_name = "stock_individual_info_em"
    provider_class = StockIndividualInfoEmProvider
    
    # 时间字段名
    time_field = "更新时间"
