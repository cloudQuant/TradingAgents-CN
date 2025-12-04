"""
盘口异动服务

东方财富-行情中心-盘口异动数据
接口: stock_changes_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_changes_em_provider import StockChangesEmProvider


class StockChangesEmService(BaseService):
    """盘口异动服务"""
    
    collection_name = "stock_changes_em"
    provider_class = StockChangesEmProvider
    
    # 时间字段名
    time_field = "更新时间"
