"""
股权质押服务

巨潮资讯-数据中心-专题统计-公司治理-股权质押
接口: stock_cg_equity_mortgage_cninfo
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_cg_equity_mortgage_cninfo_provider import StockCgEquityMortgageCninfoProvider


class StockCgEquityMortgageCninfoService(BaseService):
    """股权质押服务"""
    
    collection_name = "stock_cg_equity_mortgage_cninfo"
    provider_class = StockCgEquityMortgageCninfoProvider
    
    # 时间字段名
    time_field = "更新时间"
