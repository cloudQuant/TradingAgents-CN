"""
基金报告公告-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundAnnouncementReportEmProvider(SimpleProvider):
    """基金报告公告-东财数据提供者"""
    
    collection_name = "fund_announcement_report_em"
    display_name = "基金报告公告-东财"
    akshare_func = "fund_announcement_report_em"
    unique_keys = ["基金代码", "公告日期"]

    field_info = [
        {"name": "基金代码", "type": "string", "description": "基金代码"},
        {"name": "公告标题", "type": "string", "description": ""},
        {"name": "基金名称", "type": "string", "description": "基金名称"},
        {"name": "公告日期", "type": "string", "description": "公告的发布日期"},
        {"name": "报告ID", "type": "string", "description": "获取报告详情的依据; 拼接后可以获取公告地址"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_announcement_report_em"},
    ]
