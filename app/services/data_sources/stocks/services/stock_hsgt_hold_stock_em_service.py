"""
个股排行服务

东方财富网-数据中心-沪深港通持股-个股排行
接口: stock_hsgt_hold_stock_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hsgt_hold_stock_em_provider import StockHsgtHoldStockEmProvider


class StockHsgtHoldStockEmService(BaseService):
    """个股排行服务"""
    
    collection_name = "stock_hsgt_hold_stock_em"
    provider_class = StockHsgtHoldStockEmProvider
    
    # 时间字段名
    time_field = "更新时间"
