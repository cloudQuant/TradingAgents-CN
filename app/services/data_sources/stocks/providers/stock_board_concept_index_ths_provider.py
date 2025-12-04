"""
同花顺-概念板块指数数据提供者

同花顺-板块-概念板块-指数日频率数据
接口: stock_board_concept_index_ths
"""
from app.services.data_sources.base_provider import BaseProvider


class StockBoardConceptIndexThsProvider(BaseProvider):
    """同花顺-概念板块指数数据提供者"""
    
    # 必填属性
    collection_name = "stock_board_concept_index_ths"
    display_name = "同花顺-概念板块指数"
    akshare_func = "stock_board_concept_index_ths"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "同花顺-板块-概念板块-指数日频率数据"
    collection_route = "/stocks/collections/stock_board_concept_index_ths"
    collection_category = "板块数据"

    # 参数映射
    param_mapping = {
        "start_date": "start_date",
        "end_date": "end_date"
    }
    
    # 必填参数
    required_params = ['start_date', 'end_date']

    # 字段信息
    field_info = [
        {"name": "日期", "type": "object", "description": "-"},
        {"name": "开盘价", "type": "float64", "description": "-"},
        {"name": "最高价", "type": "float64", "description": "-"},
        {"name": "最低价", "type": "float64", "description": "-"},
        {"name": "收盘价", "type": "float64", "description": "-"},
        {"name": "成交量", "type": "int64", "description": "-"},
        {"name": "成交额", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
