"""
同花顺-概念板块简介服务

同花顺-板块-概念板块-板块简介
接口: stock_board_concept_info_ths
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_board_concept_info_ths_provider import StockBoardConceptInfoThsProvider


class StockBoardConceptInfoThsService(SimpleService):
    """同花顺-概念板块简介服务"""
    
    collection_name = "stock_board_concept_info_ths"
    provider_class = StockBoardConceptInfoThsProvider
    
    # 时间字段名
    time_field = "更新时间"
