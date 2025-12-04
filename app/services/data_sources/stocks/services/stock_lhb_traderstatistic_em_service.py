"""
营业部统计服务

东方财富网-数据中心-龙虎榜单-营业部统计
接口: stock_lhb_traderstatistic_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_lhb_traderstatistic_em_provider import StockLhbTraderstatisticEmProvider


class StockLhbTraderstatisticEmService(BaseService):
    """营业部统计服务"""
    
    collection_name = "stock_lhb_traderstatistic_em"
    provider_class = StockLhbTraderstatisticEmProvider
    
    # 时间字段名
    time_field = "更新时间"
