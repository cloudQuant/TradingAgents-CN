"""
预约披露时间-东方财富服务

东方财富-数据中心-年报季报-预约披露时间
接口: stock_yysj_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_yysj_em_provider import StockYysjEmProvider


class StockYysjEmService(BaseService):
    """预约披露时间-东方财富服务"""
    
    collection_name = "stock_yysj_em"
    provider_class = StockYysjEmProvider
    
    # 时间字段名
    time_field = "更新时间"
