"""
基金报告行业配置-巨潮数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundReportIndustryAllocationCninfoProvider(SimpleProvider):
    """基金报告行业配置-巨潮数据提供者"""
    
    collection_name = "fund_report_industry_allocation_cninfo"
    display_name = "基金报告行业配置-巨潮"
    akshare_func = "fund_report_industry_allocation_cninfo"
    unique_keys = ["更新时间"]

    field_info = [
        {"name": "行业编码", "type": "string", "description": ""},
        {"name": "证监会行业名称", "type": "string", "description": ""},
        {"name": "报告期", "type": "string", "description": ""},
        {"name": "基金覆盖家数", "type": "int", "description": "注意单位: 只"},
        {"name": "行业规模", "type": "float", "description": "注意单位: 亿元"},
        {"name": "占净资产比例", "type": "float", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_report_industry_allocation_cninfo"},
    ]
