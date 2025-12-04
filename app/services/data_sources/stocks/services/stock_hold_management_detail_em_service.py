"""
董监高及相关人员持股变动明细服务

东方财富网-数据中心-特色数据-高管持股-董监高及相关人员持股变动明细
接口: stock_hold_management_detail_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_hold_management_detail_em_provider import StockHoldManagementDetailEmProvider


class StockHoldManagementDetailEmService(SimpleService):
    """董监高及相关人员持股变动明细服务"""
    
    collection_name = "stock_hold_management_detail_em"
    provider_class = StockHoldManagementDetailEmProvider
    
    # 时间字段名
    time_field = "更新时间"
