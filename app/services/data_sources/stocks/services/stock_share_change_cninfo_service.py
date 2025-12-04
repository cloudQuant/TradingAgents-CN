"""
公司股本变动-巨潮资讯服务

巨潮资讯-数据-公司股本变动
接口: stock_share_change_cninfo
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_share_change_cninfo_provider import StockShareChangeCninfoProvider


class StockShareChangeCninfoService(BaseService):
    """公司股本变动-巨潮资讯服务"""
    
    collection_name = "stock_share_change_cninfo"
    provider_class = StockShareChangeCninfoProvider
    
    # 时间字段名
    time_field = "更新时间"
