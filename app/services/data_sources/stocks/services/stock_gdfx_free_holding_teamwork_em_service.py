"""
股东协同-十大流通股东服务

东方财富网-数据中心-股东分析-股东协同-十大流通股东
接口: stock_gdfx_free_holding_teamwork_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_gdfx_free_holding_teamwork_em_provider import StockGdfxFreeHoldingTeamworkEmProvider


class StockGdfxFreeHoldingTeamworkEmService(BaseService):
    """股东协同-十大流通股东服务"""
    
    collection_name = "stock_gdfx_free_holding_teamwork_em"
    provider_class = StockGdfxFreeHoldingTeamworkEmProvider
    
    # 时间字段名
    time_field = "更新时间"
