"""
板块排行服务

东方财富网-数据中心-沪深港通持股-板块排行
接口: stock_hsgt_board_rank_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hsgt_board_rank_em_provider import StockHsgtBoardRankEmProvider


class StockHsgtBoardRankEmService(BaseService):
    """板块排行服务"""
    
    collection_name = "stock_hsgt_board_rank_em"
    provider_class = StockHsgtBoardRankEmProvider
    
    # 时间字段名
    time_field = "更新时间"
