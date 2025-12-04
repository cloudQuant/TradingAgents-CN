"""
东方财富-概念板块-实时行情服务

东方财富网-行情中心-沪深京板块-概念板块-实时行情
接口: stock_board_concept_spot_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_board_concept_spot_em_provider import StockBoardConceptSpotEmProvider


class StockBoardConceptSpotEmService(SimpleService):
    """东方财富-概念板块-实时行情服务"""
    
    collection_name = "stock_board_concept_spot_em"
    provider_class = StockBoardConceptSpotEmProvider
    
    # 时间字段名
    time_field = "更新时间"
