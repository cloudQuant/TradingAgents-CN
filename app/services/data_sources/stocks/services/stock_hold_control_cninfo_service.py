"""
实际控制人持股变动服务

巨潮资讯-数据中心-专题统计-股东股本-实际控制人持股变动
接口: stock_hold_control_cninfo
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hold_control_cninfo_provider import StockHoldControlCninfoProvider


class StockHoldControlCninfoService(BaseService):
    """实际控制人持股变动服务"""
    
    collection_name = "stock_hold_control_cninfo"
    provider_class = StockHoldControlCninfoProvider
    
    # 时间字段名
    time_field = "更新时间"
