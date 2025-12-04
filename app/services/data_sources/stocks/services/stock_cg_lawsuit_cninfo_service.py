"""
公司诉讼服务

巨潮资讯-数据中心-专题统计-公司治理-公司诉讼
接口: stock_cg_lawsuit_cninfo
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_cg_lawsuit_cninfo_provider import StockCgLawsuitCninfoProvider


class StockCgLawsuitCninfoService(BaseService):
    """公司诉讼服务"""
    
    collection_name = "stock_cg_lawsuit_cninfo"
    provider_class = StockCgLawsuitCninfoProvider
    
    # 时间字段名
    time_field = "更新时间"
