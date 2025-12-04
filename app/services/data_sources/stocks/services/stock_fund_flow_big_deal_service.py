"""
大单追踪服务

同花顺-数据中心-资金流向-大单追踪
接口: stock_fund_flow_big_deal
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_fund_flow_big_deal_provider import StockFundFlowBigDealProvider


class StockFundFlowBigDealService(SimpleService):
    """大单追踪服务"""
    
    collection_name = "stock_fund_flow_big_deal"
    provider_class = StockFundFlowBigDealProvider
    
    # 时间字段名
    time_field = "更新时间"
