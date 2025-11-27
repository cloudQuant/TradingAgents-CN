"""
基金行业配置-东财服务（重构版：继承BaseService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_portfolio_industry_allocation_em_provider import FundPortfolioIndustryAllocationEmProvider


class FundPortfolioIndustryAllocationEmService(SimpleService):
    """基金行业配置-东财服务"""
    
    collection_name = "fund_portfolio_industry_allocation_em"
    provider_class = FundPortfolioIndustryAllocationEmProvider
