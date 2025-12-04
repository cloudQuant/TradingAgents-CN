"""
富途牛牛-美股概念-成分股服务

富途牛牛-主题投资-概念板块-成分股
接口: stock_concept_cons_futu
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_concept_cons_futu_provider import StockConceptConsFutuProvider


class StockConceptConsFutuService(BaseService):
    """富途牛牛-美股概念-成分股服务"""
    
    collection_name = "stock_concept_cons_futu"
    provider_class = StockConceptConsFutuProvider
    
    # 时间字段名
    time_field = "更新时间"
