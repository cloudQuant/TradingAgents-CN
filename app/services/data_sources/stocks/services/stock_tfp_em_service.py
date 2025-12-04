"""
停复牌信息服务

东方财富网-数据中心-特色数据-停复牌信息
接口: stock_tfp_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_tfp_em_provider import StockTfpEmProvider


class StockTfpEmService(BaseService):
    """停复牌信息服务"""
    
    collection_name = "stock_tfp_em"
    provider_class = StockTfpEmProvider
    
    # 时间字段名
    time_field = "更新时间"
