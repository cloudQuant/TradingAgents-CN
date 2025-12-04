"""
机构持股详情服务

新浪财经-机构持股-机构持股详情
接口: stock_institute_hold_detail
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_institute_hold_detail_provider import StockInstituteHoldDetailProvider


class StockInstituteHoldDetailService(BaseService):
    """机构持股详情服务"""
    
    collection_name = "stock_institute_hold_detail"
    provider_class = StockInstituteHoldDetailProvider
    
    # 时间字段名
    time_field = "更新时间"
