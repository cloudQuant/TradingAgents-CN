"""
首发申报信息数据提供者

东方财富网-数据中心-新股申购-首发申报信息-首发申报企业信息
接口: stock_ipo_declare
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockIpoDeclareProvider(SimpleProvider):
    """首发申报信息数据提供者"""
    
    # 必填属性
    collection_name = "stock_ipo_declare"
    display_name = "首发申报信息"
    akshare_func = "stock_ipo_declare"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-新股申购-首发申报信息-首发申报企业信息"
    collection_route = "/stocks/collections/stock_ipo_declare"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "申报企业", "type": "object", "description": "-"},
        {"name": "拟上市地", "type": "object", "description": "-"},
        {"name": "保荐机构", "type": "object", "description": "-"},
        {"name": "会计师事务所", "type": "object", "description": "-"},
        {"name": "律师事务所", "type": "object", "description": "-"},
        {"name": "备注", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
