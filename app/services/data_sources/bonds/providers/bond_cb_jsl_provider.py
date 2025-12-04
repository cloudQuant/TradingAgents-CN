"""
可转债实时数据-集思录数据提供者（重构版）

需求文档: tests/bonds/requirements/22_可转债实时数据-集思录.md
数据唯一标识: 代码
"""
from app.services.data_sources.base_provider import SimpleProvider


class BondCbJslProvider(SimpleProvider):
    """可转债实时数据-集思录数据提供者"""
    
    collection_name = "bond_cb_jsl"
    display_name = "可转债实时数据-集思录"
    akshare_func = "bond_cb_jsl"
    unique_keys = ["代码"]
    
    collection_description = "集思录可转债实时数据，包含转股溢价率、双低等指标"
    collection_route = "/bonds/collections/bond_cb_jsl"
    collection_order = 22
    
    field_info = [
        {"name": "代码", "type": "string", "description": "可转债代码"},
        {"name": "转债名称", "type": "string", "description": "可转债名称"},
        {"name": "现价", "type": "float", "description": "可转债现价"},
        {"name": "涨跌幅", "type": "float", "description": "涨跌幅(%)"},
        {"name": "正股代码", "type": "string", "description": "正股代码"},
        {"name": "正股名称", "type": "string", "description": "正股名称"},
        {"name": "正股价", "type": "float", "description": "正股价格"},
        {"name": "转股价", "type": "float", "description": "转股价"},
        {"name": "转股价值", "type": "float", "description": "转股价值"},
        {"name": "转股溢价率", "type": "float", "description": "转股溢价率(%)"},
        {"name": "债券评级", "type": "string", "description": "债券评级"},
        {"name": "剩余年限", "type": "float", "description": "剩余年限"},
        {"name": "剩余规模", "type": "float", "description": "剩余规模(亿元)"},
        {"name": "成交额", "type": "float", "description": "成交额(万元)"},
        {"name": "双低", "type": "float", "description": "双低值"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
