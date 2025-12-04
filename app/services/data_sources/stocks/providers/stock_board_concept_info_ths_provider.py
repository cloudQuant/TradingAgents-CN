"""
同花顺-概念板块简介数据提供者

同花顺-板块-概念板块-板块简介
接口: stock_board_concept_info_ths
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockBoardConceptInfoThsProvider(SimpleProvider):
    """同花顺-概念板块简介数据提供者"""
    
    # 必填属性
    collection_name = "stock_board_concept_info_ths"
    display_name = "同花顺-概念板块简介"
    akshare_func = "stock_board_concept_info_ths"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "同花顺-板块-概念板块-板块简介"
    collection_route = "/stocks/collections/stock_board_concept_info_ths"
    collection_category = "板块数据"

    # 字段信息
    field_info = [
        {"name": "项目", "type": "object", "description": "-"},
        {"name": "值", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
