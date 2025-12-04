"""
股本变动服务

巨潮资讯-数据中心-专题统计-股东股本-股本变动
接口: stock_hold_change_cninfo
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hold_change_cninfo_provider import StockHoldChangeCninfoProvider


class StockHoldChangeCninfoService(BaseService):
    """股本变动服务"""
    
    collection_name = "stock_hold_change_cninfo"
    provider_class = StockHoldChangeCninfoProvider
    
    # 时间字段名
    time_field = "更新时间"
