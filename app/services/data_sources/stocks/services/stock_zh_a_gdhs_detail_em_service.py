"""
股东户数详情服务

东方财富网-数据中心-特色数据-股东户数详情
接口: stock_zh_a_gdhs_detail_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zh_a_gdhs_detail_em_provider import StockZhAGdhsDetailEmProvider


class StockZhAGdhsDetailEmService(BaseService):
    """股东户数详情服务"""
    
    collection_name = "stock_zh_a_gdhs_detail_em"
    provider_class = StockZhAGdhsDetailEmProvider
    
    # 时间字段名
    time_field = "更新时间"
