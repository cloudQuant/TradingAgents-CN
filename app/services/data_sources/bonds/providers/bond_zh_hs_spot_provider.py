"""
沪深债券实时行情数据提供者（重构版：继承SimpleProvider）

需求文档: tests/bonds/requirements/03_沪深债券实时行情.md
数据唯一标识: 代码
"""
from app.services.data_sources.base_provider import SimpleProvider


class BondZhHsSpotProvider(SimpleProvider):
    """沪深债券实时行情数据提供者"""
    
    # 基本属性
    collection_name = "bond_zh_hs_spot"
    display_name = "沪深债券实时行情"
    akshare_func = "bond_zh_hs_spot"
    unique_keys = ["代码"]  # 以代码作为唯一标识
    
    # 元信息
    collection_description = "沪深债券实时行情数据，包括最新价、涨跌幅、成交量等"
    collection_route = "/bonds/collections/bond_zh_hs_spot"
    collection_order = 3
    
    # 字段信息
    field_info = [
        {"name": "代码", "type": "string", "description": "债券代码，如sh010107"},
        {"name": "名称", "type": "string", "description": "债券名称"},
        {"name": "最新价", "type": "float", "description": "最新成交价"},
        {"name": "涨跌额", "type": "float", "description": "涨跌额"},
        {"name": "涨跌幅", "type": "float", "description": "涨跌幅(%)"},
        {"name": "买入", "type": "float", "description": "买一价"},
        {"name": "卖出", "type": "float", "description": "卖一价"},
        {"name": "昨收", "type": "float", "description": "昨日收盘价"},
        {"name": "今开", "type": "float", "description": "今日开盘价"},
        {"name": "最高", "type": "float", "description": "今日最高价"},
        {"name": "最低", "type": "float", "description": "今日最低价"},
        {"name": "成交量", "type": "int", "description": "成交量(手)"},
        {"name": "成交额", "type": "int", "description": "成交额(万)"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
