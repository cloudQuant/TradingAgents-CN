"""
基金申购状态-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundPurchaseStatusProvider(SimpleProvider):
    """基金申购状态-东财数据提供者"""
    
    collection_name = "fund_purchase_status"
    display_name = "基金申购状态-东财"
    akshare_func = "fund_purchase_em"
    unique_keys = ["基金代码", "最新净值/万份收益-报告时间"]

    field_info = [
        {"name": "序号", "type": "string", "description": ""},
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "基金简称", "type": "string", "description": ""},
        {"name": "基金类型", "type": "string", "description": ""},
        {"name": "最新净值/万份收益", "type": "float", "description": ""},
        {"name": "最新净值/万份收益-报告时间", "type": "string", "description": ""},
        {"name": "申购状态", "type": "string", "description": ""},
        {"name": "赎回状态", "type": "string", "description": ""},
        {"name": "下一开放日", "type": "string", "description": ""},
        {"name": "购买起点", "type": "float", "description": ""},
        {"name": "日累计限定金额", "type": "float", "description": ""},
        {"name": "手续费", "type": "float", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_purchase_em"},
    ]
