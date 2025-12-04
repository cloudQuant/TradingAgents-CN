"""
董监高及相关人员持股变动-上证服务

上海证券交易所-披露-监管信息公开-公司监管-董董监高人员股份变动
接口: stock_share_hold_change_sse
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_share_hold_change_sse_provider import StockShareHoldChangeSseProvider


class StockShareHoldChangeSseService(BaseService):
    """董监高及相关人员持股变动-上证服务"""
    
    collection_name = "stock_share_hold_change_sse"
    provider_class = StockShareHoldChangeSseProvider
    
    # 时间字段名
    time_field = "更新时间"
