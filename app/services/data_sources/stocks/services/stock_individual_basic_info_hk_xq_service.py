"""
个股信息查询-雪球服务

雪球-个股-公司概况-公司简介
接口: stock_individual_basic_info_hk_xq
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_individual_basic_info_hk_xq_provider import StockIndividualBasicInfoHkXqProvider


class StockIndividualBasicInfoHkXqService(BaseService):
    """个股信息查询-雪球服务"""
    
    collection_name = "stock_individual_basic_info_hk_xq"
    provider_class = StockIndividualBasicInfoHkXqProvider
    
    # 时间字段名
    time_field = "更新时间"
