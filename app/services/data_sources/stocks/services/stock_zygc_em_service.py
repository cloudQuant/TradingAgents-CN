"""
主营构成-东财服务

东方财富网-个股-主营构成
接口: stock_zygc_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zygc_em_provider import StockZygcEmProvider


class StockZygcEmService(BaseService):
    """主营构成-东财服务"""
    
    collection_name = "stock_zygc_em"
    provider_class = StockZygcEmProvider
    
    # 时间字段名
    time_field = "更新时间"
