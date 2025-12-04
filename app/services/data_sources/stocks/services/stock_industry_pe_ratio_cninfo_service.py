"""
行业市盈率服务

巨潮资讯-数据中心-行业分析-行业市盈率
接口: stock_industry_pe_ratio_cninfo
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_industry_pe_ratio_cninfo_provider import StockIndustryPeRatioCninfoProvider


class StockIndustryPeRatioCninfoService(BaseService):
    """行业市盈率服务"""
    
    collection_name = "stock_industry_pe_ratio_cninfo"
    provider_class = StockIndustryPeRatioCninfoProvider
    
    # 时间字段名
    time_field = "更新时间"
