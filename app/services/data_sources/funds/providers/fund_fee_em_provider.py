"""
基金费率-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundFeeEmProvider(SimpleProvider):
    """基金费率-东财数据提供者"""
    
    collection_name = "fund_fee_em"
    display_name = "基金费率-东财"
    akshare_func = "fund_fee_em"
    unique_keys = ["更新时间"]

    field_info = [
        {"name": "费用类型", "type": "string", "description": ""},
        {"name": "条件或名称", "type": "string", "description": ""},
        {"name": "费用", "type": "float", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_fee_em"},
    ]
