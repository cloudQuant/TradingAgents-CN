"""
日度市场参与意愿数据提供者

东方财富网-数据中心-特色数据-千股千评-市场热度-日度市场参与意愿
接口: stock_comment_detail_scrd_desire_daily_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockCommentDetailScrdDesireDailyEmProvider(BaseProvider):
    """日度市场参与意愿数据提供者"""
    
    # 必填属性
    collection_name = "stock_comment_detail_scrd_desire_daily_em"
    display_name = "日度市场参与意愿"
    akshare_func = "stock_comment_detail_scrd_desire_daily_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-特色数据-千股千评-市场热度-日度市场参与意愿"
    collection_route = "/stocks/collections/stock_comment_detail_scrd_desire_daily_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol"
    }
    
    # 必填参数
    required_params = ['symbol']

    # 字段信息
    field_info = [
        {"name": "交易日", "type": "object", "description": "-"},
        {"name": "当日意愿上升", "type": "float64", "description": "-"},
        {"name": "5日平均参与意愿变化", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
