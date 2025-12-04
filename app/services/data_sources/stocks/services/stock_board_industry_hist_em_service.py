"""
东方财富-指数-日频服务

东方财富-沪深板块-行业板块-历史行情数据
接口: stock_board_industry_hist_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_board_industry_hist_em_provider import StockBoardIndustryHistEmProvider


class StockBoardIndustryHistEmService(BaseService):
    """东方财富-指数-日频服务"""
    
    collection_name = "stock_board_industry_hist_em"
    provider_class = StockBoardIndustryHistEmProvider
    
    # 时间字段名
    time_field = "更新时间"
