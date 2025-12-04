"""
华证指数数据提供者

新浪财经-ESG评级中心-ESG评级-华证指数
接口: stock_esg_hz_sina
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockEsgHzSinaProvider(SimpleProvider):
    """华证指数数据提供者"""
    
    # 必填属性
    collection_name = "stock_esg_hz_sina"
    display_name = "华证指数"
    akshare_func = "stock_esg_hz_sina"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "新浪财经-ESG评级中心-ESG评级-华证指数"
    collection_route = "/stocks/collections/stock_esg_hz_sina"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "日期", "type": "object", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "交易市场", "type": "object", "description": "-"},
        {"name": "ESG评分", "type": "float64", "description": "-"},
        {"name": "ESG等级", "type": "object", "description": "-"},
        {"name": "环境", "type": "float64", "description": "-"},
        {"name": "环境等级", "type": "object", "description": "-"},
        {"name": "社会", "type": "float64", "description": "-"},
        {"name": "社会等级", "type": "object", "description": "-"},
        {"name": "公司治理", "type": "float64", "description": "-"},
        {"name": "公司治理等级", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
