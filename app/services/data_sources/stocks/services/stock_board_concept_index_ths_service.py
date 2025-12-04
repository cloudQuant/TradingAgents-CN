"""
同花顺-概念板块指数服务

同花顺-板块-概念板块-指数日频率数据
接口: stock_board_concept_index_ths
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_board_concept_index_ths_provider import StockBoardConceptIndexThsProvider


class StockBoardConceptIndexThsService(BaseService):
    """同花顺-概念板块指数服务"""
    
    collection_name = "stock_board_concept_index_ths"
    provider_class = StockBoardConceptIndexThsProvider
    
    # 时间字段名
    time_field = "更新时间"
