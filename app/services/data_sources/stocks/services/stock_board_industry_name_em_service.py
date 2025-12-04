"""
东方财富-行业板块服务

东方财富-沪深京板块-行业板块
接口: stock_board_industry_name_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_board_industry_name_em_provider import StockBoardIndustryNameEmProvider


class StockBoardIndustryNameEmService(SimpleService):
    """东方财富-行业板块服务"""
    
    collection_name = "stock_board_industry_name_em"
    provider_class = StockBoardIndustryNameEmProvider
    
    # 时间字段名
    time_field = "更新时间"
