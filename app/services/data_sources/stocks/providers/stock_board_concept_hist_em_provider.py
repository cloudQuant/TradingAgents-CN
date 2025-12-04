"""
东方财富-指数数据提供者

东方财富-沪深板块-概念板块-历史行情数据
接口: stock_board_concept_hist_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockBoardConceptHistEmProvider(BaseProvider):
    """东方财富-指数数据提供者"""
    
    # 必填属性
    collection_name = "stock_board_concept_hist_em"
    display_name = "东方财富-指数"
    akshare_func = "stock_board_concept_hist_em"
    unique_keys = ['日期']
    
    # 可选属性
    collection_description = "东方财富-沪深板块-概念板块-历史行情数据"
    collection_route = "/stocks/collections/stock_board_concept_hist_em"
    collection_category = "历史行情"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "period": "period",
        "start_date": "start_date",
        "end_date": "end_date",
        "adjust": "adjust"
    }
    
    # 必填参数
    required_params = ['symbol', 'period', 'start_date', 'end_date']

    # 字段信息
    field_info = [
        {"name": "日期", "type": "object", "description": "-"},
        {"name": "开盘", "type": "float64", "description": "-"},
        {"name": "收盘", "type": "float64", "description": "-"},
        {"name": "最高", "type": "float64", "description": "-"},
        {"name": "最低", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "涨跌额", "type": "float64", "description": "-"},
        {"name": "成交量", "type": "int64", "description": "-"},
        {"name": "成交额", "type": "float64", "description": "-"},
        {"name": "振幅", "type": "float64", "description": "注意单位: %"},
        {"name": "换手率", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
