"""
基金评级-济安金信-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundRatingJaEmProvider(SimpleProvider):
    """基金评级-济安金信-东财数据提供者"""
    
    collection_name = "fund_rating_ja_em"
    display_name = "基金评级-济安金信-东财"
    akshare_func = "fund_rating_ja_em"
    unique_keys = ["代码", "日期"]

    field_info = [
        {"name": "代码", "type": "string", "description": ""},
        {"name": "简称", "type": "string", "description": ""},
        {"name": "基金经理", "type": "string", "description": ""},
        {"name": "基金公司", "type": "string", "description": ""},
        {"name": "3年期评级-3年评级", "type": "int", "description": ""},
        {"name": "3年期评级-较上期", "type": "float", "description": ""},
        {"name": "单位净值", "type": "float", "description": ""},
        {"name": "日期", "type": "string", "description": ""},
        {"name": "日增长率", "type": "float", "description": "注意单位: %"},
        {"name": "近1年涨幅", "type": "float", "description": "注意单位: %"},
        {"name": "近3年涨幅", "type": "float", "description": "注意单位: %"},
        {"name": "近5年涨幅", "type": "float", "description": "注意单位: %"},
        {"name": "手续费", "type": "string", "description": ""},
        {"name": "类型", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_rating_ja_em"},
    ]
