"""
行业资金流服务

同花顺-数据中心-资金流向-行业资金流
接口: stock_fund_flow_industry
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_fund_flow_industry_provider import StockFundFlowIndustryProvider


class StockFundFlowIndustryService(BaseService):
    """行业资金流服务"""
    
    collection_name = "stock_fund_flow_industry"
    provider_class = StockFundFlowIndustryProvider
    
    # 时间字段名
    time_field = "更新时间"
