"""
创业板数据提供者

东方财富网-数据中心-新股数据-IPO审核信息-创业板
接口: stock_register_cyb
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockRegisterCybProvider(SimpleProvider):
    """创业板数据提供者"""
    
    # 必填属性
    collection_name = "stock_register_cyb"
    display_name = "创业板"
    akshare_func = "stock_register_cyb"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-新股数据-IPO审核信息-创业板"
    collection_route = "/stocks/collections/stock_register_cyb"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int32", "description": "-"},
        {"name": "发行人全称", "type": "object", "description": "-"},
        {"name": "审核状态", "type": "object", "description": "-"},
        {"name": "注册地", "type": "object", "description": "-"},
        {"name": "证监会行业", "type": "object", "description": "-"},
        {"name": "保荐机构", "type": "object", "description": "-"},
        {"name": "律师事务所", "type": "object", "description": "-"},
        {"name": "会计师事务所", "type": "object", "description": "-"},
        {"name": "更新日期", "type": "object", "description": "-"},
        {"name": "受理日期", "type": "object", "description": "-"},
        {"name": "拟上市地点", "type": "object", "description": "-"},
        {"name": "招股说明书", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
