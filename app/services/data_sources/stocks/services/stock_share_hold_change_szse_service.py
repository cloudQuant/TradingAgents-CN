"""
董监高及相关人员持股变动-深证服务

深圳证券交易所-信息披露-监管信息公开-董监高人员股份变动
接口: stock_share_hold_change_szse
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_share_hold_change_szse_provider import StockShareHoldChangeSzseProvider


class StockShareHoldChangeSzseService(BaseService):
    """董监高及相关人员持股变动-深证服务"""
    
    collection_name = "stock_share_hold_change_szse"
    provider_class = StockShareHoldChangeSzseProvider
    
    # 时间字段名
    time_field = "更新时间"
