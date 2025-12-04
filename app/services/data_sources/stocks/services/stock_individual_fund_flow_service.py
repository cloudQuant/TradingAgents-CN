"""
个股资金流服务

东方财富网-数据中心-个股资金流向
接口: stock_individual_fund_flow
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_individual_fund_flow_provider import StockIndividualFundFlowProvider


class StockIndividualFundFlowService(BaseService):
    """个股资金流服务"""
    
    collection_name = "stock_individual_fund_flow"
    provider_class = StockIndividualFundFlowProvider
    
    # 时间字段名
    time_field = "更新时间"
