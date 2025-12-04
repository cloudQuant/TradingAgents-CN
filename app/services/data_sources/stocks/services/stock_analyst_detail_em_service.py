"""
分析师详情服务

东方财富网-数据中心-研究报告-东方财富分析师指数-分析师详情
接口: stock_analyst_detail_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_analyst_detail_em_provider import StockAnalystDetailEmProvider


class StockAnalystDetailEmService(BaseService):
    """分析师详情服务"""
    
    collection_name = "stock_analyst_detail_em"
    provider_class = StockAnalystDetailEmProvider
    
    # 时间字段名
    time_field = "更新时间"
