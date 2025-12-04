"""
高管持股变动明细服务

巨潮资讯-数据中心-专题统计-股东股本-高管持股变动明细
接口: stock_hold_management_detail_cninfo
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hold_management_detail_cninfo_provider import StockHoldManagementDetailCninfoProvider


class StockHoldManagementDetailCninfoService(BaseService):
    """高管持股变动明细服务"""
    
    collection_name = "stock_hold_management_detail_cninfo"
    provider_class = StockHoldManagementDetailCninfoProvider
    
    # 时间字段名
    time_field = "更新时间"
