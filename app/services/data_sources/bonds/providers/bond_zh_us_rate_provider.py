"""
中美国债收益率数据提供者（重构版）

数据集合名称: bond_zh_us_rate
数据唯一标识: 日期
"""
from app.services.data_sources.base_provider import SimpleProvider


class BondZhUsRateProvider(SimpleProvider):
    """中美国债收益率数据提供者"""
    
    collection_name = "bond_zh_us_rate"
    display_name = "中美国债收益率"
    akshare_func = "bond_zh_us_rate"
    unique_keys = ['日期']
    
    collection_description = "中美国债收益率数据"
    collection_route = "/bonds/collections/bond_zh_us_rate"
    collection_order = 27
    
    field_info = [
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
