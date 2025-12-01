"""
ETF基金历史行情-新浪服务
"""
from app.services.data_sources.base_service import BaseService
from ..providers.fund_etf_hist_sina_provider import FundEtfHistSinaProvider


class FundEtfHistSinaService(BaseService):
    collection_name = "fund_etf_hist_sina"
    provider_class = FundEtfHistSinaProvider

    batch_source_collection = "fund_spot_sina"
    batch_source_field = "代码"
    batch_concurrency = 5
    incremental_check_fields = ["代码", "日期"]

    def get_batch_params(self, *args):
        """
        Args[0] = 代码（如 sh510050）
        """
        if not args:
            return {}
        symbol = args[0]
        return {"symbol": symbol}

