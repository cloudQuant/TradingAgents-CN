"""
A股商誉市场概况数据提供者

东方财富网-数据中心-特色数据-商誉-A股商誉市场概况
接口: stock_sy_profile_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockSyProfileEmProvider(SimpleProvider):
    """A股商誉市场概况数据提供者"""
    
    # 必填属性
    collection_name = "stock_sy_profile_em"
    display_name = "A股商誉市场概况"
    akshare_func = "stock_sy_profile_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-特色数据-商誉-A股商誉市场概况"
    collection_route = "/stocks/collections/stock_sy_profile_em"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "报告期", "type": "object", "description": "-"},
        {"name": "商誉", "type": "float64", "description": "注意单位: 元"},
        {"name": "商誉减值", "type": "float64", "description": "注意单位: 元"},
        {"name": "净资产", "type": "float64", "description": "注意单位: 元"},
        {"name": "商誉占净资产比例", "type": "float64", "description": "-"},
        {"name": "商誉减值占净资产比例", "type": "float64", "description": "-"},
        {"name": "净利润规模", "type": "float64", "description": "注意单位: 元"},
        {"name": "商誉减值占净利润比例", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
