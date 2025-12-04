"""
东方财富-成份股服务

东方财富-沪深板块-行业板块-板块成份
接口: stock_board_industry_cons_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_board_industry_cons_em_provider import StockBoardIndustryConsEmProvider


class StockBoardIndustryConsEmService(BaseService):
    """东方财富-成份股服务"""
    
    collection_name = "stock_board_industry_cons_em"
    provider_class = StockBoardIndustryConsEmProvider
    
    # 时间字段名
    time_field = "更新时间"
