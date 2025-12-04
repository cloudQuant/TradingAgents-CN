"""
MSCI数据提供者

新浪财经-ESG评级中心-ESG评级-MSCI
接口: stock_esg_msci_sina
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockEsgMsciSinaProvider(SimpleProvider):
    """MSCI数据提供者"""
    
    # 必填属性
    collection_name = "stock_esg_msci_sina"
    display_name = "MSCI"
    akshare_func = "stock_esg_msci_sina"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "新浪财经-ESG评级中心-ESG评级-MSCI"
    collection_route = "/stocks/collections/stock_esg_msci_sina"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "ESG评分", "type": "object", "description": "-"},
        {"name": "环境总评", "type": "float64", "description": "-"},
        {"name": "社会责任总评", "type": "float64", "description": "-"},
        {"name": "治理总评", "type": "float64", "description": "-"},
        {"name": "评级日期", "type": "object", "description": "-"},
        {"name": "交易市场", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
