"""
公司概况-巨潮资讯数据提供者

巨潮资讯-个股-公司概况
接口: stock_profile_cninfo
"""
from app.services.data_sources.base_provider import BaseProvider


class StockProfileCninfoProvider(BaseProvider):
    """公司概况-巨潮资讯数据提供者"""
    
    # 必填属性
    collection_name = "stock_profile_cninfo"
    display_name = "公司概况-巨潮资讯"
    akshare_func = "stock_profile_cninfo"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "巨潮资讯-个股-公司概况"
    collection_route = "/stocks/collections/stock_profile_cninfo"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol"
    }
    
    # 必填参数
    required_params = ['symbol']

    # 字段信息
    field_info = [
        {"name": "曾用简称", "type": "object", "description": "-"},
        {"name": "A股代码", "type": "object", "description": "-"},
        {"name": "A股简称", "type": "object", "description": "-"},
        {"name": "B股代码", "type": "object", "description": "-"},
        {"name": "B股简称", "type": "object", "description": "-"},
        {"name": "H股代码", "type": "object", "description": "-"},
        {"name": "H股简称", "type": "object", "description": "-"},
        {"name": "入选指数", "type": "object", "description": "-"},
        {"name": "所属市场", "type": "object", "description": "-"},
        {"name": "所属行业", "type": "object", "description": "-"},
        {"name": "法人代表", "type": "object", "description": "-"},
        {"name": "注册资金", "type": "object", "description": "-"},
        {"name": "成立日期", "type": "object", "description": "-"},
        {"name": "上市日期", "type": "object", "description": "-"},
        {"name": "官方网站", "type": "object", "description": "-"},
        {"name": "电子邮箱", "type": "object", "description": "-"},
        {"name": "联系电话", "type": "object", "description": "-"},
        {"name": "传真", "type": "object", "description": "-"},
        {"name": "注册地址", "type": "object", "description": "-"},
        {"name": "办公地址", "type": "object", "description": "-"},
        {"name": "邮政编码", "type": "object", "description": "-"},
        {"name": "主营业务", "type": "object", "description": "-"},
        {"name": "经营范围", "type": "object", "description": "-"},
        {"name": "机构简介", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
