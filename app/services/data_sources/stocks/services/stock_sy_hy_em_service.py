"""
行业商誉服务

东方财富网-数据中心-特色数据-商誉-行业商誉
接口: stock_sy_hy_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_sy_hy_em_provider import StockSyHyEmProvider


class StockSyHyEmService(BaseService):
    """行业商誉服务"""
    
    collection_name = "stock_sy_hy_em"
    provider_class = StockSyHyEmProvider
    
    # 时间字段名
    time_field = "更新时间"
