"""
东方财富-成份股服务

东方财富-沪深板块-概念板块-板块成份
接口: stock_board_concept_cons_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_board_concept_cons_em_provider import StockBoardConceptConsEmProvider


class StockBoardConceptConsEmService(SimpleService):
    """东方财富-成份股服务"""
    
    collection_name = "stock_board_concept_cons_em"
    provider_class = StockBoardConceptConsEmProvider
    
    # 时间字段名
    time_field = "更新时间"
