"""
基金分红排行-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundFhRankEmProvider(SimpleProvider):
    """基金分红排行-东财数据提供者"""
    
    collection_name = "fund_fh_rank_em"
    display_name = "基金分红排行-东财"
    akshare_func = "fund_fh_rank_em"
    unique_keys = ["基金代码", "成立日期"]

    field_info = [
        {"name": "序号", "type": "int", "description": ""},
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "基金简称", "type": "string", "description": ""},
        {"name": "累计分红", "type": "float", "description": "注意单位: 元/份"},
        {"name": "累计次数", "type": "int", "description": ""},
        {"name": "成立日期", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_fh_rank_em"},
    ]
