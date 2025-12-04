"""
概念历史资金流服务

东方财富网-数据中心-资金流向-概念资金流-概念历史资金流
接口: stock_concept_fund_flow_hist
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_concept_fund_flow_hist_provider import StockConceptFundFlowHistProvider


class StockConceptFundFlowHistService(BaseService):
    """概念历史资金流服务"""
    
    collection_name = "stock_concept_fund_flow_hist"
    provider_class = StockConceptFundFlowHistProvider
    
    # 时间字段名
    time_field = "更新时间"
