"""
ETF实时行情-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundEtfSpotEmProvider(SimpleProvider):
    """ETF实时行情-东财数据提供者"""
    
    collection_name = "fund_etf_spot_em"
    display_name = "ETF实时行情-东财"
    akshare_func = "fund_etf_spot_em"
    unique_keys = ["代码", "数据日期"]

    field_info = [
        {"name": "代码", "type": "string", "description": ""},
        {"name": "最新价", "type": "float", "description": ""},
        {"name": "IOPV实时估值", "type": "float", "description": ""},
        {"name": "基金折价率", "type": "float", "description": "注意单位: %"},
        {"name": "涨跌额", "type": "float", "description": ""},
        {"name": "涨跌幅", "type": "float", "description": "注意单位: %"},
        {"name": "成交量", "type": "float", "description": ""},
        {"name": "成交额", "type": "float", "description": ""},
        {"name": "开盘价", "type": "float", "description": ""},
        {"name": "最高价", "type": "float", "description": ""},
        {"name": "最低价", "type": "float", "description": ""},
        {"name": "昨收", "type": "float", "description": ""},
        {"name": "换手率", "type": "float", "description": ""},
        {"name": "量比", "type": "float", "description": ""},
        {"name": "委比", "type": "float", "description": ""},
        {"name": "外盘", "type": "float", "description": ""},
        {"name": "内盘", "type": "float", "description": ""},
        {"name": "主力净流入-净额", "type": "float", "description": ""},
        {"name": "主力净流入-净占比", "type": "float", "description": ""},
        {"name": "超大单净流入-净额", "type": "float", "description": ""},
        {"name": "超大单净流入-净占比", "type": "float", "description": ""},
        {"name": "大单净流入-净额", "type": "float", "description": ""},
        {"name": "大单净流入-净占比", "type": "float", "description": ""},
        {"name": "中单净流入-净额", "type": "float", "description": ""},
        {"name": "中单净流入-净占比", "type": "float", "description": ""},
        {"name": "小单净流入-净额", "type": "float", "description": ""},
        {"name": "小单净流入-净占比", "type": "float", "description": ""},
        {"name": "现手", "type": "float", "description": ""},
        {"name": "买一", "type": "float", "description": ""},
        {"name": "卖一", "type": "float", "description": ""},
        {"name": "最新份额", "type": "float", "description": ""},
        {"name": "流通市值", "type": "int", "description": ""},
        {"name": "总市值", "type": "int", "description": ""},
        {"name": "数据日期", "type": "string", "description": ""},
        {"name": "更新时间", "type": "string", "description": ""},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_etf_spot_em"},
    ]
