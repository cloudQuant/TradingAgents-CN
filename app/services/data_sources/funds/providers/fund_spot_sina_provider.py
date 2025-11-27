"""
基金实时行情-新浪数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundSpotSinaProvider(SimpleProvider):
    """基金实时行情-新浪数据提供者"""
    
    collection_name = "fund_spot_sina"
    display_name = "基金实时行情-新浪"
    akshare_func = "fund_spot_em"
    unique_keys = ["代码", "更新时间"]

    field_info = [
        {"name": "代码", "type": "string", "description": ""},
        {"name": "名称", "type": "string", "description": ""},
        {"name": "最新价", "type": "float", "description": ""},
        {"name": "涨跌额", "type": "float", "description": ""},
        {"name": "涨跌幅", "type": "float", "description": "注意单位: %"},
        {"name": "买入", "type": "float", "description": ""},
        {"name": "卖出", "type": "float", "description": ""},
        {"name": "昨收", "type": "float", "description": ""},
        {"name": "今开", "type": "float", "description": ""},
        {"name": "最高", "type": "float", "description": ""},
        {"name": "最低", "type": "float", "description": ""},
        {"name": "成交量", "type": "int", "description": "注意单位: 股"},
        {"name": "成交额", "type": "int", "description": "注意单位: 元"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_spot_em"},
    ]
