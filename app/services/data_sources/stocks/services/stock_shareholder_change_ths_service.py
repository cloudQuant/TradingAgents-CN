"""
股东持股变动统计服务

同花顺-公司大事-股东持股变动
接口: stock_shareholder_change_ths
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_shareholder_change_ths_provider import StockShareholderChangeThsProvider


class StockShareholderChangeThsService(BaseService):
    """股东持股变动统计服务"""
    
    collection_name = "stock_shareholder_change_ths"
    provider_class = StockShareholderChangeThsProvider
    
    # 时间字段名
    time_field = "更新时间"
