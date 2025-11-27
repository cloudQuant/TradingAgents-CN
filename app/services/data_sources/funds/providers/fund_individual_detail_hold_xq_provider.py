"""
基金持仓明细-雪球数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundIndividualDetailHoldXqProvider(SimpleProvider):
    """基金持仓明细-雪球数据提供者"""
    
    collection_name = "fund_individual_detail_hold_xq"
    display_name = "基金持仓明细-雪球"
    akshare_func = "fund_individual_detail_hold_xq"
    unique_keys = ["更新时间"]

    field_info = [
        {"name": "资产类型", "type": "string", "description": ""},
        {"name": "仓位占比", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_individual_detail_hold_xq"},
    ]
