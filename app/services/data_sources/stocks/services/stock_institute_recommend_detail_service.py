"""
股票评级记录服务

新浪财经-机构推荐池-股票评级记录
接口: stock_institute_recommend_detail
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_institute_recommend_detail_provider import StockInstituteRecommendDetailProvider


class StockInstituteRecommendDetailService(BaseService):
    """股票评级记录服务"""
    
    collection_name = "stock_institute_recommend_detail"
    provider_class = StockInstituteRecommendDetailProvider
    
    # 时间字段名
    time_field = "更新时间"
