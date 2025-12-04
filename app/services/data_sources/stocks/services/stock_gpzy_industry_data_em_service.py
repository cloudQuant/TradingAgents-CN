"""
上市公司质押比例服务

东方财富网-数据中心-特色数据-股权质押-上市公司质押比例-行业数据
接口: stock_gpzy_industry_data_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_gpzy_industry_data_em_provider import StockGpzyIndustryDataEmProvider


class StockGpzyIndustryDataEmService(SimpleService):
    """上市公司质押比例服务"""
    
    collection_name = "stock_gpzy_industry_data_em"
    provider_class = StockGpzyIndustryDataEmProvider
    
    # 时间字段名
    time_field = "更新时间"
