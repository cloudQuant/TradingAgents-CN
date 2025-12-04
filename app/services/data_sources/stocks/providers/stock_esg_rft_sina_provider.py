"""
路孚特数据提供者

新浪财经-ESG评级中心-ESG评级-路孚特
接口: stock_esg_rft_sina
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockEsgRftSinaProvider(SimpleProvider):
    """路孚特数据提供者"""
    
    # 必填属性
    collection_name = "stock_esg_rft_sina"
    display_name = "路孚特"
    akshare_func = "stock_esg_rft_sina"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "新浪财经-ESG评级中心-ESG评级-路孚特"
    collection_route = "/stocks/collections/stock_esg_rft_sina"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "ESG评分", "type": "object", "description": "-"},
        {"name": "ESG评分日期", "type": "object", "description": "-"},
        {"name": "环境总评", "type": "float64", "description": "-"},
        {"name": "环境总评日期", "type": "float64", "description": "-"},
        {"name": "社会责任总评", "type": "float64", "description": "-"},
        {"name": "社会责任总评日期", "type": "object", "description": "-"},
        {"name": "治理总评", "type": "object", "description": "-"},
        {"name": "治理总评日期", "type": "object", "description": "-"},
        {"name": "争议总评", "type": "object", "description": "-"},
        {"name": "争议总评日期", "type": "object", "description": "-"},
        {"name": "行业", "type": "object", "description": "-"},
        {"name": "交易所", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
