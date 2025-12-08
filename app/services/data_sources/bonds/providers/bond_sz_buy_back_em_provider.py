"""
深证质押式回购数据提供者（重构版）

数据集合名称: bond_sz_buy_back_em
数据唯一标识: 代码, 更新时间
"""
from app.services.data_sources.base_provider import SimpleProvider


class BondSzBuyBackEmProvider(SimpleProvider):
    """深证质押式回购数据提供者"""
    
    collection_name = "bond_sz_buy_back_em"
    display_name = "深证质押式回购"
    akshare_func = "bond_sz_buy_back_em"
    unique_keys = ["代码", "更新时间"]
    
    collection_description = "深证质押式回购数据"
    collection_route = "/bonds/collections/bond_sz_buy_back_em"
    collection_order = 20
    
    field_info = [
        {"name": "序号", "type": "int", "description": "序号"},
        {"name": "代码", "type": "string", "description": "回购代码"},
        {"name": "名称", "type": "string", "description": "回购名称"},
        {"name": "最新价", "type": "float", "description": "最新成交价"},
        {"name": "涨跌额", "type": "float", "description": "价格涨跌额"},
        {"name": "涨跌幅", "type": "float", "description": "价格涨跌幅(%)"},
        {"name": "今开", "type": "float", "description": "今日开盘价"},
        {"name": "最高", "type": "float", "description": "今日最高价"},
        {"name": "最低", "type": "float", "description": "今日最低价"},
        {"name": "昨收", "type": "float", "description": "昨日收盘价"},
        {"name": "成交量", "type": "float", "description": "成交量"},
        {"name": "成交额", "type": "float", "description": "成交额"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
