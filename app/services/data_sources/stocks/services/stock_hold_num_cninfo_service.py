"""
股东人数及持股集中度服务

巨潮资讯-数据中心-专题统计-股东股本-股东人数及持股集中度
接口: stock_hold_num_cninfo
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hold_num_cninfo_provider import StockHoldNumCninfoProvider


class StockHoldNumCninfoService(BaseService):
    """股东人数及持股集中度服务"""
    
    collection_name = "stock_hold_num_cninfo"
    provider_class = StockHoldNumCninfoProvider
    
    # 时间字段名
    time_field = "更新时间"
