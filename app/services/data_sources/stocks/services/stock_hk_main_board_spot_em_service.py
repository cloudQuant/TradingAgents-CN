"""
港股主板实时行情数据-东财服务

港股主板的实时行情数据; 该数据有 15 分钟延时
接口: stock_hk_main_board_spot_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_hk_main_board_spot_em_provider import StockHkMainBoardSpotEmProvider


class StockHkMainBoardSpotEmService(SimpleService):
    """港股主板实时行情数据-东财服务"""
    
    collection_name = "stock_hk_main_board_spot_em"
    provider_class = StockHkMainBoardSpotEmProvider
    
    # 时间字段名
    time_field = "更新时间"
