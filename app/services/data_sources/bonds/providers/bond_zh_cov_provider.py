"""
可转债数据一览表-东财数据提供者（重构版：继承SimpleProvider）

需求文档: tests/bonds/requirements/07_可转债数据一览表-东财.md
数据唯一标识: 债券代码
"""
from app.services.data_sources.base_provider import SimpleProvider


class BondZhCovProvider(SimpleProvider):
    """可转债数据一览表-东财数据提供者"""
    
    # 基本属性
    collection_name = "bond_zh_cov"
    display_name = "可转债数据一览表-东财"
    akshare_func = "bond_zh_cov"
    unique_keys = ["债券代码"]  # 以债券代码作为唯一标识
    
    # 元信息
    collection_description = "可转债综合数据，包括申购、转股价、溢价率等"
    collection_route = "/bonds/collections/bond_zh_cov"
    collection_order = 7
    
    # 字段信息
    field_info = [
        {"name": "债券代码", "type": "string", "description": "可转债代码"},
        {"name": "债券简称", "type": "string", "description": "可转债名称"},
        {"name": "申购日期", "type": "string", "description": "申购日期"},
        {"name": "申购代码", "type": "string", "description": "申购代码"},
        {"name": "申购上限", "type": "float", "description": "申购上限(万元)"},
        {"name": "正股代码", "type": "string", "description": "正股代码"},
        {"name": "正股简称", "type": "string", "description": "正股名称"},
        {"name": "正股价", "type": "float", "description": "正股价格"},
        {"name": "转股价", "type": "float", "description": "转股价"},
        {"name": "转股价值", "type": "float", "description": "转股价值"},
        {"name": "债现价", "type": "float", "description": "债券现价"},
        {"name": "转股溢价率", "type": "float", "description": "转股溢价率(%)"},
        {"name": "发行规模", "type": "float", "description": "发行规模(亿元)"},
        {"name": "中签率", "type": "float", "description": "中签率(%)"},
        {"name": "上市时间", "type": "string", "description": "上市时间"},
        {"name": "信用评级", "type": "string", "description": "信用评级"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
