"""
基金经理-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundManagerEmProvider(SimpleProvider):
    """基金经理-东财数据提供者"""
    
    collection_name = "fund_manager_em"
    display_name = "基金经理-东财"
    akshare_func = "fund_manager_em"
    unique_keys = ["现任基金代码", "累计从业时间"]

    field_info = [
        {"name": "序号", "type": "int", "description": ""},
        {"name": "姓名", "type": "string", "description": ""},
        {"name": "所属公司", "type": "string", "description": ""},
        {"name": "现任基金代码", "type": "string", "description": ""},
        {"name": "现任基金", "type": "string", "description": ""},
        {"name": "累计从业时间", "type": "int", "description": "注意单位: 天"},
        {"name": "现任基金资产总规模", "type": "float", "description": "注意单位: 亿元"},
        {"name": "现任基金最佳回报", "type": "float", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_manager_em"},
    ]
