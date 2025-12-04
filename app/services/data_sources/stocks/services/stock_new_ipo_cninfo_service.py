"""
新股发行服务

巨潮资讯-数据中心-新股数据-新股发行
接口: stock_new_ipo_cninfo
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_new_ipo_cninfo_provider import StockNewIpoCninfoProvider


class StockNewIpoCninfoService(SimpleService):
    """新股发行服务"""
    
    collection_name = "stock_new_ipo_cninfo"
    provider_class = StockNewIpoCninfoProvider
    
    # 时间字段名
    time_field = "更新时间"
