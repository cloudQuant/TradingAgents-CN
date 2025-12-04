"""
达标企业数据提供者

东方财富网-数据中心-新股数据-注册制审核-达标企业
接口: stock_register_db
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockRegisterDbProvider(SimpleProvider):
    """达标企业数据提供者"""
    
    # 必填属性
    collection_name = "stock_register_db"
    display_name = "达标企业"
    akshare_func = "stock_register_db"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-新股数据-注册制审核-达标企业"
    collection_route = "/stocks/collections/stock_register_db"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int32", "description": "-"},
        {"name": "经营范围", "type": "object", "description": "-"},
        {"name": "近三年营业收入-2019", "type": "float64", "description": "注意单位: 元"},
        {"name": "近三年净利润-2019", "type": "float64", "description": "注意单位: 元"},
        {"name": "近三年研发费用-2019", "type": "object", "description": "注意单位: 元"},
        {"name": "近三年营业收入-2018", "type": "float64", "description": "注意单位: 元"},
        {"name": "近三年净利润-2018", "type": "float64", "description": "注意单位: 元"},
        {"name": "近三年研发费用-2018", "type": "object", "description": "注意单位: 元"},
        {"name": "近三年营业收入-2017", "type": "object", "description": "注意单位: 元"},
        {"name": "近三年净利润-2017", "type": "object", "description": "注意单位: 元"},
        {"name": "近三年研发费用-2017", "type": "object", "description": "注意单位: 元"},
        {"name": "近两年累计净利润", "type": "float64", "description": "注意单位: 元"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
