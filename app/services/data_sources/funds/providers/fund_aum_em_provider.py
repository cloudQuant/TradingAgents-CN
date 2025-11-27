"""
基金管理规模-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundAumEmProvider(SimpleProvider):
    """基金管理规模-东财数据提供者"""
    
    collection_name = "fund_aum_em"
    display_name = "基金管理规模-东财"
    akshare_func = "fund_aum_em"
    unique_keys = ["更新日期"]

    field_info = [
        {"name": "序号", "type": "int", "description": ""},
        {"name": "基金公司", "type": "string", "description": ""},
        {"name": "成立时间", "type": "string", "description": ""},
        {"name": "全部管理规模", "type": "float", "description": "注意单位: 亿元"},
        {"name": "全部基金数", "type": "int", "description": ""},
        {"name": "全部经理数", "type": "int", "description": ""},
        {"name": "更新日期", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_aum_em"},
    ]
