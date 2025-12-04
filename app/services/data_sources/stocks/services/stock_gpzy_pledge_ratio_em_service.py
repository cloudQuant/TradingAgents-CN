"""
上市公司质押比例服务

东方财富网-数据中心-特色数据-股权质押-上市公司质押比例
接口: stock_gpzy_pledge_ratio_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_gpzy_pledge_ratio_em_provider import StockGpzyPledgeRatioEmProvider


class StockGpzyPledgeRatioEmService(BaseService):
    """上市公司质押比例服务"""
    
    collection_name = "stock_gpzy_pledge_ratio_em"
    provider_class = StockGpzyPledgeRatioEmProvider
    
    # 时间字段名
    time_field = "更新时间"
