"""
东方财富-行业板块-实时行情服务

东方财富网-沪深板块-行业板块-实时行情
接口: stock_board_industry_spot_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_board_industry_spot_em_provider import StockBoardIndustrySpotEmProvider


class StockBoardIndustrySpotEmService(BaseService):
    """东方财富-行业板块-实时行情服务"""
    
    collection_name = "stock_board_industry_spot_em"
    provider_class = StockBoardIndustrySpotEmProvider
    
    # 时间字段名
    time_field = "更新时间"
