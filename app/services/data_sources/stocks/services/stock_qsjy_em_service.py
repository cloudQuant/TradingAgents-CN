"""
券商业绩月报服务

东方财富网-数据中心-特色数据-券商业绩月报
接口: stock_qsjy_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_qsjy_em_provider import StockQsjyEmProvider


class StockQsjyEmService(BaseService):
    """券商业绩月报服务"""
    
    collection_name = "stock_qsjy_em"
    provider_class = StockQsjyEmProvider
    
    # 时间字段名
    time_field = "更新时间"
