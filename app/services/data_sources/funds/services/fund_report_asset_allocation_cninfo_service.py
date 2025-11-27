"""
基金报告资产配置-巨潮服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_report_asset_allocation_cninfo_provider import FundReportAssetAllocationCninfoProvider


class FundReportAssetAllocationCninfoService(SimpleService):
    """基金报告资产配置-巨潮服务"""
    
    collection_name = "fund_report_asset_allocation_cninfo"
    provider_class = FundReportAssetAllocationCninfoProvider
