"""
沪深港通资金流向服务

东方财富网-数据中心-资金流向-沪深港通资金流向
接口: stock_hsgt_fund_flow_summary_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_hsgt_fund_flow_summary_em_provider import StockHsgtFundFlowSummaryEmProvider


class StockHsgtFundFlowSummaryEmService(SimpleService):
    """沪深港通资金流向服务"""
    
    collection_name = "stock_hsgt_fund_flow_summary_em"
    provider_class = StockHsgtFundFlowSummaryEmProvider
    
    # 时间字段名
    time_field = "更新时间"
