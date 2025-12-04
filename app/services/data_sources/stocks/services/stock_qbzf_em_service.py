"""
增发服务

东方财富网-数据中心-新股数据-增发-全部增发
接口: stock_qbzf_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_qbzf_em_provider import StockQbzfEmProvider


class StockQbzfEmService(SimpleService):
    """增发服务"""
    
    collection_name = "stock_qbzf_em"
    provider_class = StockQbzfEmProvider
    
    # 时间字段名
    time_field = "更新时间"
