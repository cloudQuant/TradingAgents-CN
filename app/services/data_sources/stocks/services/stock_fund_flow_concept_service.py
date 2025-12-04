"""
概念资金流服务

同花顺-数据中心-资金流向-概念资金流
接口: stock_fund_flow_concept
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_fund_flow_concept_provider import StockFundFlowConceptProvider


class StockFundFlowConceptService(BaseService):
    """概念资金流服务"""
    
    collection_name = "stock_fund_flow_concept"
    provider_class = StockFundFlowConceptProvider
    
    # 时间字段名
    time_field = "更新时间"
