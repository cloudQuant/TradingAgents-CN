"""
行业历史资金流服务

东方财富网-数据中心-资金流向-行业资金流-行业历史资金流
接口: stock_sector_fund_flow_hist
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_sector_fund_flow_hist_provider import StockSectorFundFlowHistProvider


class StockSectorFundFlowHistService(BaseService):
    """行业历史资金流服务"""
    
    collection_name = "stock_sector_fund_flow_hist"
    provider_class = StockSectorFundFlowHistProvider
    
    # 时间字段名
    time_field = "更新时间"
