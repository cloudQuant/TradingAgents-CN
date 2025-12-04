"""
个股资金流服务

同花顺-数据中心-资金流向-个股资金流
接口: stock_fund_flow_individual
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_fund_flow_individual_provider import StockFundFlowIndividualProvider


class StockFundFlowIndividualService(BaseService):
    """个股资金流服务"""
    
    collection_name = "stock_fund_flow_individual"
    provider_class = StockFundFlowIndividualProvider
    
    # 时间字段名
    time_field = "更新时间"
