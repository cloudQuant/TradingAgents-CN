"""
东方财富-指数服务

东方财富-沪深板块-概念板块-历史行情数据
接口: stock_board_concept_hist_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_board_concept_hist_em_provider import StockBoardConceptHistEmProvider


class StockBoardConceptHistEmService(BaseService):
    """东方财富-指数服务"""
    
    collection_name = "stock_board_concept_hist_em"
    provider_class = StockBoardConceptHistEmProvider
    
    # 时间字段名
    time_field = "更新时间"
