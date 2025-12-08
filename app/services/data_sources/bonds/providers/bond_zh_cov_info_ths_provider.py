"""
可转债详情-同花顺数据提供者（重构版）

数据集合名称: bond_zh_cov_info_ths
数据唯一标识: 债券代码
"""
from app.services.data_sources.base_provider import BaseProvider


class BondZhCovInfoThsProvider(BaseProvider):
    """可转债详情-同花顺数据提供者"""
    
    collection_name = "bond_zh_cov_info_ths"
    display_name = "可转债详情-同花顺"
    akshare_func = "bond_zh_cov_info_ths"
    unique_keys = ['债券代码']
    
    collection_description = "可转债详情-同花顺数据"
    collection_route = "/bonds/collections/bond_zh_cov_info_ths"
    collection_order = 16
    
    field_info = [
        {"name": "债券代码", "type": "string", "description": "可转债代码"},
        {"name": "债券简称", "type": "string", "description": "可转债简称"},
        {"name": "申购日期", "type": "string", "description": "申购日期"},
        {"name": "申购代码", "type": "string", "description": "申购代码"},
        {"name": "原股东配售码", "type": "string", "description": "原股东配售码"},
        {"name": "每股获配额", "type": "number", "description": "每股获配额"},
        {"name": "计划发行量", "type": "number", "description": "计划发行量"},
        {"name": "实际发行量", "type": "number", "description": "实际发行量"},
        {"name": "中签公布日", "type": "string", "description": "中签公布日期"},
        {"name": "中签号", "type": "string", "description": "中签号"},
        {"name": "上市日期", "type": "string", "description": "上市日期"},
        {"name": "正股代码", "type": "string", "description": "正股代码"},
        {"name": "正股简称", "type": "string", "description": "正股简称"},
        {"name": "转股价格", "type": "number", "description": "转股价格"},
        {"name": "到期时间", "type": "string", "description": "到期时间"},
        {"name": "中签率", "type": "string", "description": "中签率，单位：%"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
