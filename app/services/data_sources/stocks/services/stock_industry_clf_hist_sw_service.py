"""
申万个股行业分类变动历史服务

申万宏源研究-行业分类-全部行业分类
接口: stock_industry_clf_hist_sw
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_industry_clf_hist_sw_provider import StockIndustryClfHistSwProvider


class StockIndustryClfHistSwService(SimpleService):
    """申万个股行业分类变动历史服务"""
    
    collection_name = "stock_industry_clf_hist_sw"
    provider_class = StockIndustryClfHistSwProvider
    
    # 时间字段名
    time_field = "更新时间"
