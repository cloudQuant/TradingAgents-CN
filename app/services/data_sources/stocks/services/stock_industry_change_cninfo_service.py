"""
上市公司行业归属的变动情况-巨潮资讯服务

巨潮资讯-数据-上市公司行业归属的变动情况
接口: stock_industry_change_cninfo
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_industry_change_cninfo_provider import StockIndustryChangeCninfoProvider


class StockIndustryChangeCninfoService(BaseService):
    """上市公司行业归属的变动情况-巨潮资讯服务"""
    
    collection_name = "stock_industry_change_cninfo"
    provider_class = StockIndustryChangeCninfoProvider
    
    # 时间字段名
    time_field = "更新时间"
