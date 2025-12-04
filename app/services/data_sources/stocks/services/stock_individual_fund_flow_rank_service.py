"""
个股资金流排名服务

东方财富网-数据中心-资金流向-排名
接口: stock_individual_fund_flow_rank
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_individual_fund_flow_rank_provider import StockIndividualFundFlowRankProvider


class StockIndividualFundFlowRankService(BaseService):
    """个股资金流排名服务"""
    
    collection_name = "stock_individual_fund_flow_rank"
    provider_class = StockIndividualFundFlowRankProvider
    
    # 时间字段名
    time_field = "更新时间"
