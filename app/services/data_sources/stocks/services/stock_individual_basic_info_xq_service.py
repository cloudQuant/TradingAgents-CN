"""
个股信息查询-雪球服务

雪球财经-个股-公司概况-公司简介
接口: stock_individual_basic_info_xq
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_individual_basic_info_xq_provider import StockIndividualBasicInfoXqProvider


class StockIndividualBasicInfoXqService(BaseService):
    """个股信息查询-雪球服务"""
    
    collection_name = "stock_individual_basic_info_xq"
    provider_class = StockIndividualBasicInfoXqProvider
    
    # 时间字段名
    time_field = "更新时间"
