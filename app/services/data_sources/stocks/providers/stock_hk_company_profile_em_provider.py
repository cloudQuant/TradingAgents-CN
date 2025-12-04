"""
公司资料数据提供者

东方财富-港股-公司资料
接口: stock_hk_company_profile_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHkCompanyProfileEmProvider(BaseProvider):
    """公司资料数据提供者"""
    
    # 必填属性
    collection_name = "stock_hk_company_profile_em"
    display_name = "公司资料"
    akshare_func = "stock_hk_company_profile_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-港股-公司资料"
    collection_route = "/stocks/collections/stock_hk_company_profile_em"
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
        {"name": "注册地", "type": "object", "description": "-"},
        {"name": "公司成立日期", "type": "object", "description": "-"},
        {"name": "所属行业", "type": "object", "description": "-"},
        {"name": "董事长", "type": "object", "description": "-"},
        {"name": "公司秘书", "type": "object", "description": "-"},
        {"name": "员工人数", "type": "int64", "description": "-"},
        {"name": "办公地址", "type": "object", "description": "-"},
        {"name": "公司网址", "type": "object", "description": "-"},
        {"name": "E-MAIL", "type": "object", "description": "-"},
        {"name": "年结日", "type": "object", "description": "-"},
        {"name": "联系电话", "type": "object", "description": "-"},
        {"name": "核数师", "type": "object", "description": "-"},
        {"name": "传真", "type": "object", "description": "-"},
        {"name": "公司介绍", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
