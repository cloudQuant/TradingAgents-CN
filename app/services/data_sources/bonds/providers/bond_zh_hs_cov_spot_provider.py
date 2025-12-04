"""
可转债实时行情-沪深数据提供者（重构版：继承SimpleProvider）

需求文档: tests/bonds/requirements/05_可转债实时行情-沪深.md
数据唯一标识: 代码
"""
from app.services.data_sources.base_provider import SimpleProvider


class BondZhHsCovSpotProvider(SimpleProvider):
    """可转债实时行情-沪深数据提供者"""
    
    # 基本属性
    collection_name = "bond_zh_hs_cov_spot"
    display_name = "可转债实时行情-沪深"
    akshare_func = "bond_zh_hs_cov_spot"
    unique_keys = ["代码"]  # 以代码作为唯一标识
    
    # 元信息
    collection_description = "沪深可转债实时行情数据"
    collection_route = "/bonds/collections/bond_zh_hs_cov_spot"
    collection_order = 5
    
    # 字段信息
    field_info = [
        {"name": "代码", "type": "string", "description": "可转债代码"},
        {"name": "名称", "type": "string", "description": "可转债名称"},
        {"name": "最新价", "type": "float", "description": "最新价"},
        {"name": "涨跌幅", "type": "float", "description": "涨跌幅(%)"},
        {"name": "涨跌额", "type": "float", "description": "涨跌额"},
        {"name": "成交量", "type": "float", "description": "成交量(手)"},
        {"name": "成交额", "type": "float", "description": "成交额"},
        {"name": "今开", "type": "float", "description": "今日开盘价"},
        {"name": "昨收", "type": "float", "description": "昨日收盘价"},
        {"name": "最高", "type": "float", "description": "最高价"},
        {"name": "最低", "type": "float", "description": "最低价"},
        {"name": "申买价", "type": "float", "description": "申买价"},
        {"name": "申卖价", "type": "float", "description": "申卖价"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
