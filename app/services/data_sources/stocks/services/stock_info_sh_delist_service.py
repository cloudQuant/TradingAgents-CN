"""
暂停/终止上市-上证服务

上海证券交易所暂停/终止上市股票
接口: stock_info_sh_delist
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_info_sh_delist_provider import StockInfoShDelistProvider


class StockInfoShDelistService(BaseService):
    """暂停/终止上市-上证服务"""
    
    collection_name = "stock_info_sh_delist"
    provider_class = StockInfoShDelistProvider
    
    # 时间字段名
    time_field = "更新时间"
