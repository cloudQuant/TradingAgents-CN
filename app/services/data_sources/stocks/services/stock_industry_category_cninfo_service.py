"""
行业分类数据-巨潮资讯服务

巨潮资讯-数据-行业分类数据
接口: stock_industry_category_cninfo
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_industry_category_cninfo_provider import StockIndustryCategoryCninfoProvider


class StockIndustryCategoryCninfoService(BaseService):
    """行业分类数据-巨潮资讯服务"""
    
    collection_name = "stock_industry_category_cninfo"
    provider_class = StockIndustryCategoryCninfoProvider
    
    # 时间字段名
    time_field = "更新时间"
