"""
机构持股一览表服务

新浪财经-机构持股-机构持股一览表
接口: stock_institute_hold
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_institute_hold_provider import StockInstituteHoldProvider


class StockInstituteHoldService(BaseService):
    """机构持股一览表服务"""
    
    collection_name = "stock_institute_hold"
    provider_class = StockInstituteHoldProvider
    
    # 时间字段名
    time_field = "更新时间"
