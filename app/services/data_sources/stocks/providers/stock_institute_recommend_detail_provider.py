"""
股票评级记录数据提供者

新浪财经-机构推荐池-股票评级记录
接口: stock_institute_recommend_detail
"""
from app.services.data_sources.base_provider import BaseProvider


class StockInstituteRecommendDetailProvider(BaseProvider):
    """股票评级记录数据提供者"""
    
    # 必填属性
    collection_name = "stock_institute_recommend_detail"
    display_name = "股票评级记录"
    akshare_func = "stock_institute_recommend_detail"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "新浪财经-机构推荐池-股票评级记录"
    collection_route = "/stocks/collections/stock_institute_recommend_detail"
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
        {"name": "股票代码", "type": "str", "description": "-"},
        {"name": "目标价", "type": "str", "description": "-"},
        {"name": "最新评级", "type": "str", "description": "-"},
        {"name": "评级机构", "type": "str", "description": "-"},
        {"name": "分析师", "type": "str", "description": "-"},
        {"name": "行业", "type": "str", "description": "-"},
        {"name": "评级日期", "type": "str", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
