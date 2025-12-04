"""
分析师指数排行服务

东方财富网-数据中心-研究报告-东方财富分析师指数
接口: stock_analyst_rank_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_analyst_rank_em_provider import StockAnalystRankEmProvider


class StockAnalystRankEmService(BaseService):
    """分析师指数排行服务"""
    
    collection_name = "stock_analyst_rank_em"
    provider_class = StockAnalystRankEmProvider
    
    # 时间字段名
    time_field = "更新时间"
