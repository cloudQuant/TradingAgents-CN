"""
个股龙虎榜详情服务

东方财富网-数据中心-龙虎榜单-个股龙虎榜详情
接口: stock_lhb_stock_detail_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_lhb_stock_detail_em_provider import StockLhbStockDetailEmProvider


class StockLhbStockDetailEmService(BaseService):
    """个股龙虎榜详情服务"""
    
    collection_name = "stock_lhb_stock_detail_em"
    provider_class = StockLhbStockDetailEmProvider
    
    # 时间字段名
    time_field = "更新时间"
