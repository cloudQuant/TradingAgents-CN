"""
基金报告资产配置-巨潮数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundReportAssetAllocationCninfoProvider(SimpleProvider):
    """基金报告资产配置-巨潮数据提供者"""
    
    collection_name = "fund_report_asset_allocation_cninfo"
    display_name = "基金报告资产配置-巨潮"
    akshare_func = "fund_report_asset_allocation_cninfo"
    unique_keys = ["更新时间"]

    field_info = [
        {"name": "报告期", "type": "string", "description": ""},
        {"name": "基金覆盖家数", "type": "string", "description": "注意单位: 只"},
        {"name": "股票权益类占净资产比例", "type": "string", "description": "注意单位: %"},
        {"name": "债券固定收益类占净资产比例", "type": "string", "description": "注意单位: %"},
        {"name": "现金货币类占净资产比例", "type": "string", "description": "注意单位: %"},
        {"name": "基金市场净资产规模", "type": "string", "description": "注意单位: 亿元"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_report_asset_allocation_cninfo"},
    ]
