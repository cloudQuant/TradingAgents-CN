"""
ESG 评级数据数据提供者

新浪财经-ESG评级中心-ESG评级-ESG评级数据
接口: stock_esg_rate_sina
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockEsgRateSinaProvider(SimpleProvider):
    """ESG 评级数据数据提供者"""
    
    # 必填属性
    collection_name = "stock_esg_rate_sina"
    display_name = "ESG 评级数据"
    akshare_func = "stock_esg_rate_sina"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-ESG评级中心-ESG评级-ESG评级数据"
    collection_route = "/stocks/collections/stock_esg_rate_sina"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "成分股代码", "type": "object", "description": "-"},
        {"name": "评级机构", "type": "object", "description": "-"},
        {"name": "评级", "type": "object", "description": "-"},
        {"name": "评级季度", "type": "object", "description": "-"},
        {"name": "标识", "type": "object", "description": "-"},
        {"name": "交易市场", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
