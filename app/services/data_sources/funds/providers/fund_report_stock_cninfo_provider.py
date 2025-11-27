"""
基金报告持股-巨潮数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundReportStockCninfoProvider(SimpleProvider):
    """基金报告持股-巨潮数据提供者"""
    
    collection_name = "fund_report_stock_cninfo"
    display_name = "基金报告持股-巨潮"
    akshare_func = "fund_report_stock_cninfo"
    unique_keys = ["股票代码", "更新时间"]

    field_info = [
        {"name": "序号", "type": "int", "description": ""},
        {"name": "股票代码", "type": "string", "description": ""},
        {"name": "股票简称", "type": "string", "description": ""},
        {"name": "报告期", "type": "string", "description": ""},
        {"name": "基金覆盖家数", "type": "int", "description": ""},
        {"name": "持股总数", "type": "string", "description": ""},
        {"name": "持股总市值", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_report_stock_cninfo"},
    ]
