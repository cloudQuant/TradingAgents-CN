"""
机构推荐池数据提供者

新浪财经-机构推荐池-具体指标的数据
接口: stock_institute_recommend
"""
from app.services.data_sources.base_provider import BaseProvider


class StockInstituteRecommendProvider(BaseProvider):
    """机构推荐池数据提供者"""
    
    # 必填属性
    collection_name = "stock_institute_recommend"
    display_name = "机构推荐池"
    akshare_func = "stock_institute_recommend"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-机构推荐池-具体指标的数据"
    collection_route = "/stocks/collections/stock_institute_recommend"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol"
    }
    
    # 必填参数
    required_params = ['symbol']

    # 字段信息
    field_info = [
        {"name": "-", "type": "-", "description": "根据特定 indicator 而定"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
