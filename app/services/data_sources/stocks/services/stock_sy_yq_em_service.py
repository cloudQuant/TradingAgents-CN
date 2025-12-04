"""
商誉减值预期明细服务

东方财富网-数据中心-特色数据-商誉-商誉减值预期明细
接口: stock_sy_yq_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_sy_yq_em_provider import StockSyYqEmProvider


class StockSyYqEmService(BaseService):
    """商誉减值预期明细服务"""
    
    collection_name = "stock_sy_yq_em"
    provider_class = StockSyYqEmProvider
    
    # 时间字段名
    time_field = "更新时间"
