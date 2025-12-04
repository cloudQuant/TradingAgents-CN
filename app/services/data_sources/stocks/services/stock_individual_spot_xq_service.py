"""
实时行情数据-雪球服务

雪球-行情中心-个股
接口: stock_individual_spot_xq
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_individual_spot_xq_provider import StockIndividualSpotXqProvider


class StockIndividualSpotXqService(BaseService):
    """实时行情数据-雪球服务"""
    
    collection_name = "stock_individual_spot_xq"
    provider_class = StockIndividualSpotXqProvider
    
    # 时间字段名
    time_field = "更新时间"
