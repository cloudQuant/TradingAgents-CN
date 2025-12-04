"""
机构推荐池服务

新浪财经-机构推荐池-具体指标的数据
接口: stock_institute_recommend
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_institute_recommend_provider import StockInstituteRecommendProvider


class StockInstituteRecommendService(BaseService):
    """机构推荐池服务"""
    
    collection_name = "stock_institute_recommend"
    provider_class = StockInstituteRecommendProvider
    
    # 时间字段名
    time_field = "更新时间"
