"""
板块异动详情服务

东方财富-行情中心-当日板块异动详情
接口: stock_board_change_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_board_change_em_provider import StockBoardChangeEmProvider


class StockBoardChangeEmService(SimpleService):
    """板块异动详情服务"""
    
    collection_name = "stock_board_change_em"
    provider_class = StockBoardChangeEmProvider
    
    # 时间字段名
    time_field = "更新时间"
