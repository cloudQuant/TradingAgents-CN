"""
重要股东股权质押明细服务

东方财富网-数据中心-特色数据-股权质押-重要股东股权质押明细
接口: stock_gpzy_pledge_ratio_detail_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_gpzy_pledge_ratio_detail_em_provider import StockGpzyPledgeRatioDetailEmProvider


class StockGpzyPledgeRatioDetailEmService(SimpleService):
    """重要股东股权质押明细服务"""
    
    collection_name = "stock_gpzy_pledge_ratio_detail_em"
    provider_class = StockGpzyPledgeRatioDetailEmProvider
    
    # 时间字段名
    time_field = "更新时间"
