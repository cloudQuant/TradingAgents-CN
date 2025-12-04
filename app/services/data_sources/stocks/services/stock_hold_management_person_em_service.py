"""
人员增减持股变动明细服务

东方财富网-数据中心-特色数据-高管持股-人员增减持股变动明细
接口: stock_hold_management_person_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hold_management_person_em_provider import StockHoldManagementPersonEmProvider


class StockHoldManagementPersonEmService(BaseService):
    """人员增减持股变动明细服务"""
    
    collection_name = "stock_hold_management_person_em"
    provider_class = StockHoldManagementPersonEmProvider
    
    # 时间字段名
    time_field = "更新时间"
