"""
股东持股变动统计-十大股东服务

东方财富网-数据中心-股东分析-股东持股变动统计-十大股东
接口: stock_gdfx_holding_change_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_gdfx_holding_change_em_provider import StockGdfxHoldingChangeEmProvider


class StockGdfxHoldingChangeEmService(BaseService):
    """股东持股变动统计-十大股东服务"""
    
    collection_name = "stock_gdfx_holding_change_em"
    provider_class = StockGdfxHoldingChangeEmProvider
    
    # 时间字段名
    time_field = "更新时间"
