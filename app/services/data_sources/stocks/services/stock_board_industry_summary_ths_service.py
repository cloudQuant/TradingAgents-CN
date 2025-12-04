"""
同花顺-同花顺行业一览表服务

同花顺-同花顺行业一览表
接口: stock_board_industry_summary_ths
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_board_industry_summary_ths_provider import StockBoardIndustrySummaryThsProvider


class StockBoardIndustrySummaryThsService(SimpleService):
    """同花顺-同花顺行业一览表服务"""
    
    collection_name = "stock_board_industry_summary_ths"
    provider_class = StockBoardIndustrySummaryThsProvider
    
    # 时间字段名
    time_field = "更新时间"
