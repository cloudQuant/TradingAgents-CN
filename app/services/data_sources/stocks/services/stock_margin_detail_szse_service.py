"""
融资融券明细服务

深证证券交易所-融资融券数据-融资融券交易明细数据
接口: stock_margin_detail_szse
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_margin_detail_szse_provider import StockMarginDetailSzseProvider


class StockMarginDetailSzseService(BaseService):
    """融资融券明细服务"""
    
    collection_name = "stock_margin_detail_szse"
    provider_class = StockMarginDetailSzseProvider
    
    # 时间字段名
    time_field = "更新时间"
