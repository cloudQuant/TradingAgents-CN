"""
上市公司质押比例数据提供者

东方财富网-数据中心-特色数据-股权质押-上市公司质押比例-行业数据
接口: stock_gpzy_industry_data_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockGpzyIndustryDataEmProvider(SimpleProvider):
    """上市公司质押比例数据提供者"""
    
    # 必填属性
    collection_name = "stock_gpzy_industry_data_em"
    display_name = "上市公司质押比例"
    akshare_func = "stock_gpzy_industry_data_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-特色数据-股权质押-上市公司质押比例-行业数据"
    collection_route = "/stocks/collections/stock_gpzy_industry_data_em"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "行业", "type": "object", "description": "-"},
        {"name": "平均质押比例", "type": "float64", "description": "注意单位: %"},
        {"name": "公司家数", "type": "float64", "description": "-"},
        {"name": "质押总笔数", "type": "float64", "description": "-"},
        {"name": "质押总股本", "type": "float64", "description": "-"},
        {"name": "最新质押市值", "type": "float64", "description": "-"},
        {"name": "统计时间", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
