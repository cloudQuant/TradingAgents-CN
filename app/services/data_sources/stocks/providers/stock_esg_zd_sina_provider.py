"""
秩鼎数据提供者

新浪财经-ESG评级中心-ESG评级-秩鼎
接口: stock_esg_zd_sina
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockEsgZdSinaProvider(SimpleProvider):
    """秩鼎数据提供者"""
    
    # 必填属性
    collection_name = "stock_esg_zd_sina"
    display_name = "秩鼎"
    akshare_func = "stock_esg_zd_sina"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "新浪财经-ESG评级中心-ESG评级-秩鼎"
    collection_route = "/stocks/collections/stock_esg_zd_sina"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "ESG评分", "type": "object", "description": "-"},
        {"name": "环境总评", "type": "object", "description": "-"},
        {"name": "社会责任总评", "type": "object", "description": "-"},
        {"name": "治理总评", "type": "object", "description": "-"},
        {"name": "评分日期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
