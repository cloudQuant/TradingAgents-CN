"""
基金累计分红-新浪服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_etf_dividend_sina_provider import FundEtfDividendSinaProvider


class FundEtfDividendSinaService(SimpleService):
    """基金累计分红-新浪服务"""
    
    collection_name = "fund_etf_dividend_sina"
    provider_class = FundEtfDividendSinaProvider
