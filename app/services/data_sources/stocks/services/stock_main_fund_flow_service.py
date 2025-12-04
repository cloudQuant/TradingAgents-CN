"""
主力净流入排名服务

东方财富网-数据中心-资金流向-主力净流入排名
接口: stock_main_fund_flow
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_main_fund_flow_provider import StockMainFundFlowProvider


class StockMainFundFlowService(BaseService):
    """主力净流入排名服务"""
    
    collection_name = "stock_main_fund_flow"
    provider_class = StockMainFundFlowProvider
    
    # 时间字段名
    time_field = "更新时间"
