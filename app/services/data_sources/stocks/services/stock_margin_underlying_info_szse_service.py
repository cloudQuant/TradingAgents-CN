"""
标的证券信息服务

深圳证券交易所-融资融券数据-标的证券信息
接口: stock_margin_underlying_info_szse
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_margin_underlying_info_szse_provider import StockMarginUnderlyingInfoSzseProvider


class StockMarginUnderlyingInfoSzseService(BaseService):
    """标的证券信息服务"""
    
    collection_name = "stock_margin_underlying_info_szse"
    provider_class = StockMarginUnderlyingInfoSzseProvider
    
    # 时间字段名
    time_field = "更新时间"
