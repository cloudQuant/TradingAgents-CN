"""
股东协同-十大股东服务

东方财富网-数据中心-股东分析-股东协同-十大股东
接口: stock_gdfx_holding_teamwork_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_gdfx_holding_teamwork_em_provider import StockGdfxHoldingTeamworkEmProvider


class StockGdfxHoldingTeamworkEmService(BaseService):
    """股东协同-十大股东服务"""
    
    collection_name = "stock_gdfx_holding_teamwork_em"
    provider_class = StockGdfxHoldingTeamworkEmProvider
    
    # 时间字段名
    time_field = "更新时间"
