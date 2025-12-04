"""
东方财富-指数-分时服务

东方财富-沪深板块-行业板块-分时历史行情数据
接口: stock_board_industry_hist_min_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_board_industry_hist_min_em_provider import StockBoardIndustryHistMinEmProvider


class StockBoardIndustryHistMinEmService(BaseService):
    """东方财富-指数-分时服务"""
    
    collection_name = "stock_board_industry_hist_min_em"
    provider_class = StockBoardIndustryHistMinEmProvider
    
    # 时间字段名
    time_field = "更新时间"
