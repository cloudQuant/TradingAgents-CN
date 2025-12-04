"""
高管持股变动统计服务

同花顺-公司大事-高管持股变动
接口: stock_management_change_ths
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_management_change_ths_provider import StockManagementChangeThsProvider


class StockManagementChangeThsService(BaseService):
    """高管持股变动统计服务"""
    
    collection_name = "stock_management_change_ths"
    provider_class = StockManagementChangeThsProvider
    
    # 时间字段名
    time_field = "更新时间"
