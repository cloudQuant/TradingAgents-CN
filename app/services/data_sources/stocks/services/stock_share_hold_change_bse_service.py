"""
董监高及相关人员持股变动-北证服务

北京证券交易所-信息披露-监管信息-董监高及相关人员持股变动
接口: stock_share_hold_change_bse
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_share_hold_change_bse_provider import StockShareHoldChangeBseProvider


class StockShareHoldChangeBseService(BaseService):
    """董监高及相关人员持股变动-北证服务"""
    
    collection_name = "stock_share_hold_change_bse"
    provider_class = StockShareHoldChangeBseProvider
    
    # 时间字段名
    time_field = "更新时间"
