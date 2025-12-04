"""
融资融券汇总服务

深圳证券交易所-融资融券数据-融资融券汇总数据
接口: stock_margin_szse
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_margin_szse_provider import StockMarginSzseProvider


class StockMarginSzseService(BaseService):
    """融资融券汇总服务"""
    
    collection_name = "stock_margin_szse"
    provider_class = StockMarginSzseProvider
    
    # 时间字段名
    time_field = "更新时间"
