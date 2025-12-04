"""
收益率曲线历史数据数据提供者（重构版）

数据集合名称: bond_china_close_return
数据唯一标识: 曲线名称, 日期, 期限
"""
from app.services.data_sources.base_provider import BaseProvider


class BondChinaCloseReturnProvider(BaseProvider):
    """收益率曲线历史数据数据提供者"""
    
    collection_name = "bond_china_close_return"
    display_name = "收益率曲线历史数据"
    akshare_func = "bond_china_close_return"
    unique_keys = ['曲线名称', '日期', '期限']
    
    collection_description = "收益率曲线历史数据数据"
    collection_route = "/bonds/collections/bond_china_close_return"
    collection_order = 26
    
    field_info = [
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
