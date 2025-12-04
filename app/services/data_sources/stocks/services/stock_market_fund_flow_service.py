"""
大盘资金流服务

东方财富网-数据中心-资金流向-大盘
接口: stock_market_fund_flow
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_market_fund_flow_provider import StockMarketFundFlowProvider


class StockMarketFundFlowService(SimpleService):
    """大盘资金流服务"""
    
    collection_name = "stock_market_fund_flow"
    provider_class = StockMarketFundFlowProvider
    
    # 时间字段名
    time_field = "更新时间"
