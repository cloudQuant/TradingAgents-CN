"""
基金评级汇总-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundRatingAllEmProvider(SimpleProvider):
    """基金评级汇总-东财数据提供者"""
    
    collection_name = "fund_rating_all_em"
    display_name = "基金评级汇总-东财"
    akshare_func = "fund_rating_all_em"
    unique_keys = ["代码", "更新时间"]

    field_info = [
        {"name": "代码", "type": "string", "description": ""},
        {"name": "简称", "type": "string", "description": ""},
        {"name": "基金经理", "type": "string", "description": ""},
        {"name": "基金公司", "type": "string", "description": ""},
        {"name": "5星评级家数", "type": "int", "description": ""},
        {"name": "上海证券", "type": "float", "description": ""},
        {"name": "招商证券", "type": "float", "description": ""},
        {"name": "济安金信", "type": "float", "description": ""},
        {"name": "手续费", "type": "float", "description": ""},
        {"name": "类型", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_rating_all_em"},
    ]
