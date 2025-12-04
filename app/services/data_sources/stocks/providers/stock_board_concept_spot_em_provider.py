"""
东方财富-概念板块-实时行情数据提供者

东方财富网-行情中心-沪深京板块-概念板块-实时行情
接口: stock_board_concept_spot_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockBoardConceptSpotEmProvider(SimpleProvider):
    """东方财富-概念板块-实时行情数据提供者"""
    
    # 必填属性
    collection_name = "stock_board_concept_spot_em"
    display_name = "东方财富-概念板块-实时行情"
    akshare_func = "stock_board_concept_spot_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-行情中心-沪深京板块-概念板块-实时行情"
    collection_route = "/stocks/collections/stock_board_concept_spot_em"
    collection_category = "实时行情"

    # 字段信息
    field_info = [
        {"name": "item", "type": "object", "description": "-"},
        {"name": "value", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
