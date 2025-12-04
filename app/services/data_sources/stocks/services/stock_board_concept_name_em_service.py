"""
东方财富-概念板块服务

东方财富网-行情中心-沪深京板块-概念板块
接口: stock_board_concept_name_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_board_concept_name_em_provider import StockBoardConceptNameEmProvider


class StockBoardConceptNameEmService(SimpleService):
    """东方财富-概念板块服务"""
    
    collection_name = "stock_board_concept_name_em"
    provider_class = StockBoardConceptNameEmProvider
    
    # 时间字段名
    time_field = "更新时间"
